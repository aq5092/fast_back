from fastapi import APIRouter
from fastapi import FastAPI, HTTPException, Depends, status, HTTPException
from sqlalchemy.orm import Session
from users import crud, schemas, models
from database import SessionLocal, engine
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import asyncio

models.Base.metadata.create_all(bind=engine)
# dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.post('/userc/', response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    return crud.create_user(db=db, user=user)

@router.get('/users/', response_model=List[schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@router.get('/users/{user_id}', response_model=schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user

@router.put('/useru/{user_id}', response_model=schemas.User)
async def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return crud.update_user(db=db, user=user, user_id=user_id)

@router.delete('/userd/{user_id}', response_model=schemas.User)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return crud.delete_user(db=db, user_id=user_id)


