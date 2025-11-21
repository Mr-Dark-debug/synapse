from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from db.session import get_db
from db.models import User, Collection, CollectionItem
from api.deps import get_current_user

router = APIRouter(prefix="/collections", tags=["collections"])

from datetime import datetime

# Pydantic Models
class CollectionCreate(BaseModel):
    name: str
    description: Optional[str] = None

class CollectionItemCreate(BaseModel):
    paper_id: str
    paper_title: str
    paper_summary: str

class CollectionItemResponse(BaseModel):
    id: int
    paper_id: str
    paper_title: str
    paper_summary: str
    added_at: datetime

    class Config:
        from_attributes = True

class CollectionResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    items: List[CollectionItemResponse] = []

    class Config:
        from_attributes = True

# Endpoints

@router.post("/", response_model=CollectionResponse)
async def create_collection(
    collection: CollectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_collection = Collection(
        user_id=current_user.id,
        name=collection.name,
        description=collection.description
    )
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    return db_collection

@router.get("/", response_model=List[CollectionResponse])
async def get_collections(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return current_user.collections

@router.get("/{collection_id}", response_model=CollectionResponse)
async def get_collection(
    collection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    collection = db.query(Collection).filter(
        Collection.id == collection_id,
        Collection.user_id == current_user.id
    ).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection

@router.delete("/{collection_id}")
async def delete_collection(
    collection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    collection = db.query(Collection).filter(
        Collection.id == collection_id,
        Collection.user_id == current_user.id
    ).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    db.delete(collection)
    db.commit()
    return {"message": "Collection deleted"}

@router.post("/{collection_id}/items", response_model=CollectionItemResponse)
async def add_item_to_collection(
    collection_id: int,
    item: CollectionItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    collection = db.query(Collection).filter(
        Collection.id == collection_id,
        Collection.user_id == current_user.id
    ).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    # Check if already exists
    existing = db.query(CollectionItem).filter(
        CollectionItem.collection_id == collection_id,
        CollectionItem.paper_id == item.paper_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Paper already in collection")

    db_item = CollectionItem(
        collection_id=collection_id,
        paper_id=item.paper_id,
        paper_title=item.paper_title,
        paper_summary=item.paper_summary
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{collection_id}/items/{paper_id}")
async def remove_item_from_collection(
    collection_id: int,
    paper_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    collection = db.query(Collection).filter(
        Collection.id == collection_id,
        Collection.user_id == current_user.id
    ).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    item = db.query(CollectionItem).filter(
        CollectionItem.collection_id == collection_id,
        CollectionItem.paper_id == paper_id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in collection")
    
    db.delete(item)
    db.commit()
    return {"message": "Item removed from collection"}
