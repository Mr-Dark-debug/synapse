from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from services.arxiv_service import search_arxiv, get_random_paper
from services.gemini_service import get_gemini_response
from services.pdf_service import extract_text_from_pdf
from api.deps import get_current_user
from db import models

router = APIRouter(tags=["research"])

class ChatRequest(BaseModel):
    papers_context: str
    user_query: str

class ELI5Request(BaseModel):
    text: str

@router.get("/search")
async def search(query: str, start: int = 0, max_results: int = 10, sort_by: str = "submittedDate", sort_order: str = "descending"):
    try:
        results = await search_arxiv(query, start, max_results, sort_by, sort_order)
        return results
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/random")
async def random_paper():
    try:
        paper = await get_random_paper()
        if not paper:
            raise HTTPException(status_code=404, detail="No paper found")
        return paper
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from sqlalchemy.orm import Session
from db.session import get_db

@router.post("/chat")
async def chat(request: ChatRequest, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        # Get User Config
        api_key = current_user.profile.gemini_api_key if current_user.profile else None
        model_name = current_user.profile.preferred_model if current_user.profile else "gemini-1.5-flash"
        
        # Get Active Prompt
        active_prompt = db.query(models.PromptTemplate).filter(
            models.PromptTemplate.user_id == current_user.id,
            models.PromptTemplate.type == "chat",
            models.PromptTemplate.is_active == True
        ).first()
        
        system_instruction = active_prompt.content if active_prompt else None

        response = await get_gemini_response(
            request.user_query, 
            api_key=api_key, 
            model=model_name, 
            context=request.papers_context,
            system_instruction=system_instruction
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/extract")
async def extract(pdf_url: str):
    try:
        text = await extract_text_from_pdf(pdf_url)
        return {"text": text[:10000]} # Limit for now
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/eli5")
async def eli5(request: ELI5Request, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        api_key = current_user.profile.gemini_api_key if current_user.profile else None
        model_name = current_user.profile.preferred_model if current_user.profile else "gemini-1.5-flash"
        
        active_prompt = db.query(models.PromptTemplate).filter(
            models.PromptTemplate.user_id == current_user.id,
            models.PromptTemplate.type == "eli5",
            models.PromptTemplate.is_active == True
        ).first()
        
        system_instruction = active_prompt.content if active_prompt else None
        
        # Fallback prompt if no template
        if not system_instruction:
            prompt = f"Explain the following text like I'm 5 years old. Keep it simple, fun, and use analogies if possible:\n\n{request.text}"
            response = await get_gemini_response(prompt, api_key=api_key, model=model_name)
        else:
            # Use template
            response = await get_gemini_response(request.text, api_key=api_key, model=model_name, system_instruction=system_instruction)
            
        return response
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"ELI5 error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/summarize")
async def summarize(request: ELI5Request, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        api_key = current_user.profile.gemini_api_key if current_user.profile else None
        model_name = current_user.profile.preferred_model if current_user.profile else "gemini-1.5-flash"
        
        active_prompt = db.query(models.PromptTemplate).filter(
            models.PromptTemplate.user_id == current_user.id,
            models.PromptTemplate.type == "summarize",
            models.PromptTemplate.is_active == True
        ).first()
        
        system_instruction = active_prompt.content if active_prompt else None
        
        if not system_instruction:
            prompt = f"Provide a comprehensive, professional academic summary of the following text. Highlight key findings, methodology, and implications:\n\n{request.text}"
            response = await get_gemini_response(prompt, api_key=api_key, model=model_name)
        else:
            response = await get_gemini_response(request.text, api_key=api_key, model=model_name, system_instruction=system_instruction)
            
        return response
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Summarize error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
