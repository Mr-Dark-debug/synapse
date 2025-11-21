from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from db.session import get_db
from db.models import User, ChatSession, ChatMessage
from api.deps import get_current_user
from services.gemini_service import get_gemini_response
import datetime

router = APIRouter(prefix="/chat", tags=["chat"])

# Pydantic Models
class ChatSessionCreate(BaseModel):
    title: str

class MessageCreate(BaseModel):
    message: str
    paper_ids: List[str] = []

class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class ChatSessionResponse(BaseModel):
    id: int
    title: str
    updated_at: datetime.datetime
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True

# Endpoints

@router.post("/sessions", response_model=ChatSessionResponse)
async def create_session(
    session: ChatSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_session = ChatSession(
        user_id=current_user.id,
        title=session.title
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.get("/sessions", response_model=List[ChatSessionResponse])
async def get_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sessions = db.query(ChatSession).filter(
        ChatSession.user_id == current_user.id
    ).order_by(ChatSession.updated_at.desc()).all()
    return sessions

@router.get("/sessions/{session_id}", response_model=ChatSessionResponse)
async def get_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.delete("/sessions/{session_id}")
async def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    db.delete(session)
    db.commit()
    return {"message": "Session deleted"}

@router.post("/sessions/{session_id}/message")
async def send_message(
    session_id: int,
    message_data: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    import logging
    logger = logging.getLogger(__name__)
    
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Validate API key before proceeding
    if not current_user.profile or not current_user.profile.gemini_api_key:
        raise HTTPException(
            status_code=400,
            detail="Gemini API key not configured. Please add it in Settings."
        )
    
    # Save user message
    user_msg = ChatMessage(
        session_id=session_id,
        role="user",
        content=message_data.message
    )
    db.add(user_msg)
    db.commit()
    
    try:
        # Get context from previous messages (last 10)
        history = db.query(ChatMessage).filter(
            ChatMessage.session_id == session_id
        ).order_by(ChatMessage.created_at.desc()).limit(10).all()
        
        # Reverse to get chronological order
        history = history[::-1]
        
        # Format history for Gemini (exclude the message we just added)
        chat_history = []
        for msg in history[:-1]:  # Exclude the last message (current user message)
            chat_history.append({"role": msg.role, "parts": [msg.content]})
        
        logger.info(f"Sending message to Gemini for session {session_id}")
        
        # Get AI response - this now raises HTTPException on errors
        ai_response_text = await get_gemini_response(
            message_data.message,
            current_user.profile.gemini_api_key,
            model=current_user.profile.preferred_model,
            history=chat_history,
            context=""  # Context can be added from paper_ids if needed
        )
        
        # Save AI message
        ai_msg = ChatMessage(
            session_id=session_id,
            role="assistant",
            content=ai_response_text
        )
        db.add(ai_msg)
        
        # Update session timestamp
        session.updated_at = datetime.datetime.now()
        
        db.commit()
        
        logger.info(f"Successfully generated response for session {session_id}")
        return {"response": ai_response_text}
        
    except HTTPException:
        # Roll back the transaction if there's an error
        db.rollback()
        # Re-raise the HTTP exception (already has proper status code and detail)
        raise
    except Exception as e:
        # Roll back the transaction
        db.rollback()
        logger.error(f"Unexpected error in send_message: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while generating the response"
        )

