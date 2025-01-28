from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from database import get_db  # SQLAlchemy sessiyasini olish uchun yordamchi
from pydantics import UserBase, UserCreate, UserResponse,TaskBase,TaskCreate, TaskResponse
from typing import List, Optional
import crud


router = APIRouter()

@router.post("/userc/", response_model=UserResponse)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/userc/{user_id}/tasks/", response_model=TaskResponse)
def create_task_endpoint(user_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_task(db, task, user_id)

@router.get("/users/{user_id}/tasks/", response_model=List[TaskResponse])
def get_user_tasks_endpoint(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_tasks_by_user(db, user_id)
