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


@router.get("/users/", response_model=List[UserResponse])
def get_all_users(db:Session= Depends(get_db)):
    users = crud.get_users(db)
    if not users:
        raise HTTPException(status_code=404, detail="User not found")
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/useru/{user_id}", response_model=UserResponse)
def update_user_endpoint(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    updated_user = crud.update_user(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/userd/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    deleted_user = crud.delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": f"User with ID {user_id} deleted"}





@router.post("/taskc/{user_id}", response_model=TaskResponse)
def create_task_endpoint(user_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_task(db, task, user_id)


@router.get("/tasks/", response_model=List[TaskResponse])
def get_all_tasks(db: Session= Depends(get_db)):
    tasks = crud.get_all_tasks(db)
    if not tasks:
        raise HTTPException(status_code=404, detail="Tasks not found")
    return tasks


@router.get("/users/{user_id}/tasks/", response_model=List[TaskResponse])
def get_user_tasks_endpoint(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.get_tasks_by_user(db, user_id)

@router.put("/tasku/{task_id}", response_model=TaskResponse)
def update_task_endpoint(task_id: int, task: TaskCreate, db: Session = Depends(get_db)):
    updated_task = crud.update_task(db, task_id, task)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@router.delete("/taskd/{task_id}")
def delete_task_endpoint(task_id: int, db: Session = Depends(get_db)):
    deleted_task = crud.delete_task(db, task_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": f"Task with ID {task_id} deleted"}
