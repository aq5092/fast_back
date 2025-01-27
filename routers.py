from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from database import get_db  # SQLAlchemy sessiyasini olish uchun yordamchi
from pydantics import UserBase, UserCreate, UserResponse,PostBase,PostCreate, PostResponse
from typing import List, Optional
import crud


router = APIRouter()

@router.post("/users/", response_model=UserResponse)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/userc/{user_id}/posts/", response_model=PostResponse)
def create_post_endpoint(user_id: int, post: PostCreate, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return create_post(db, post, user_id)

@router.get("/users/{user_id}/posts/", response_model=List[PostResponse])
def get_user_posts_endpoint(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return get_posts_by_user(db, user_id)
