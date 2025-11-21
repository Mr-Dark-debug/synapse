from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from db.session import get_db
from db import models
from api.deps import get_current_user

router = APIRouter(prefix="/user", tags=["user"])

class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    preferred_model: Optional[str] = None
    profile_image: Optional[str] = None

class PromptTemplateCreate(BaseModel):
    name: str
    type: str
    content: str
    model: Optional[str] = None

class PromptTemplateUpdate(BaseModel):
    name: Optional[str] = None
    content: Optional[str] = None
    model: Optional[str] = None
    is_active: Optional[bool] = None

class PromptTemplateResponse(BaseModel):
    id: int
    name: str
    type: str
    content: str
    model: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True

@router.get("/me")
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.profile.full_name if current_user.profile else None,
        "profile_image": current_user.profile.profile_image if current_user.profile else None,
        "preferred_model": current_user.profile.preferred_model if current_user.profile else "gemini-1.5-flash",
        "api_key_set": bool(current_user.profile.gemini_api_key) if current_user.profile and current_user.profile.gemini_api_key else False
    }

@router.patch("/profile")
def update_profile(profile_data: ProfileUpdate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.profile:
        profile = models.Profile(user_id=current_user.id)
        db.add(profile)
    else:
        profile = current_user.profile
    
    if profile_data.full_name is not None:
        profile.full_name = profile_data.full_name
    if profile_data.preferred_model is not None:
        profile.preferred_model = profile_data.preferred_model
    if profile_data.profile_image is not None:
        profile.profile_image = profile_data.profile_image
        
    db.commit()
    return {"message": "Profile updated successfully"}

@router.post("/api-key")
def update_api_key(api_key: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.profile:
        profile = models.Profile(user_id=current_user.id)
        db.add(profile)
    else:
        profile = current_user.profile
    
    profile.gemini_api_key = api_key
    db.commit()
    return {"message": "API Key updated successfully"}

@router.get("/models")
def list_models(current_user: models.User = Depends(get_current_user)):
    if not current_user.profile or not current_user.profile.gemini_api_key:
        return []
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=current_user.profile.gemini_api_key)
        models_list = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                models_list.append({"name": m.name, "displayName": m.display_name})
        return models_list
    except Exception as e:
        print(f"Error fetching models: {e}")
        return []

# Prompt Template Endpoints
@router.get("/prompts", response_model=List[PromptTemplateResponse])
def get_prompts(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.PromptTemplate).filter(models.PromptTemplate.user_id == current_user.id).all()

@router.post("/prompts", response_model=PromptTemplateResponse)
def create_prompt(prompt: PromptTemplateCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_prompt = models.PromptTemplate(**prompt.dict(), user_id=current_user.id)
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

@router.put("/prompts/{prompt_id}")
def update_prompt(prompt_id: int, prompt_data: PromptTemplateUpdate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_prompt = db.query(models.PromptTemplate).filter(models.PromptTemplate.id == prompt_id, models.PromptTemplate.user_id == current_user.id).first()
    if not db_prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    if prompt_data.name is not None:
        db_prompt.name = prompt_data.name
    if prompt_data.content is not None:
        db_prompt.content = prompt_data.content
    if prompt_data.model is not None:
        db_prompt.model = prompt_data.model
    if prompt_data.is_active is not None:
        # If setting to active, deactivate others of same type
        if prompt_data.is_active:
            db.query(models.PromptTemplate).filter(
                models.PromptTemplate.user_id == current_user.id,
                models.PromptTemplate.type == db_prompt.type
            ).update({"is_active": False})
        db_prompt.is_active = prompt_data.is_active
        
    db.commit()
    return {"message": "Prompt updated"}

@router.delete("/prompts/{prompt_id}")
def delete_prompt(prompt_id: int, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    db_prompt = db.query(models.PromptTemplate).filter(models.PromptTemplate.id == prompt_id, models.PromptTemplate.user_id == current_user.id).first()
    if not db_prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    db.delete(db_prompt)
    db.commit()
    return {"message": "Prompt deleted"}
