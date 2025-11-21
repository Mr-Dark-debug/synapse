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
    session = db.query(ChatSession).filter(
        ChatSession.id == session_id,
        ChatSession.user_id == current_user.id
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Save user message
    user_msg = ChatMessage(
        session_id=session_id,
        role="user",
        content=message_data.message
    )
    db.add(user_msg)
    
    # Get context from previous messages (last 10)
    history = db.query(ChatMessage).filter(
        ChatMessage.session_id == session_id
    ).order_by(ChatMessage.created_at.desc()).limit(10).all()
    
    # Reverse to get chronological order
    history = history[::-1]
    
    # Format history for Gemini
    chat_history = []
    for msg in history:
        chat_history.append({"role": msg.role, "parts": [msg.content]})
    
    # Get AI response
    # Note: We need to fetch paper content if paper_ids are provided.
    # For now, we assume the frontend sends the context or we fetch it here.
    # To keep it simple and fast, we'll rely on the existing research service logic 
    # but adapted for history.
    
    # Actually, the existing research router handles context fetching. 
    # We should probably reuse that logic or import the service.
    # Let's assume get_gemini_response can handle history + new message + context.
    
    # Construct context string from papers (this part is tricky without the paper content)
    # The frontend should probably send the paper content or we need to fetch it from arXiv/Semantic Scholar again?
    # Or we store paper content in DB? We don't store full text in DB yet.
    # For this iteration, we will assume the user provides the context in the message 
    # OR we just chat without specific paper context if not provided.
    
    # Wait, the previous implementation sent context in the prompt.
    # Let's look at research.py to see how it does it.
    
    ai_response_text = await get_gemini_response(
        message_data.message,
        current_user.profile.gemini_api_key,
        model=current_user.profile.preferred_model,
        history=chat_history,
        context="" # We need to figure out context passing
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
    
    return {"response": ai_response_text}
