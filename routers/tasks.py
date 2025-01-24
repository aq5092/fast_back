from fastapi import APIRouter
from fastapi import FastAPI, HTTPException, Depends, status, HTTPException
from sqlalchemy.orm import Session
from tasks import crud, schemas, models
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
###### to create 
@router.post('/taskc/', response_model=schemas.Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = crud.create_task(db, task=task)
    if db_task:
        raise HTTPException(status_code=201, detail='Task created successfully')
    return crud.create_task(db=db, task=task)

###### to read all
@router.get('/tasks/', response_model=List[schemas.Task])
async def read_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks
##### to read id

@router.get('/tasks/{task_id}', response_model=schemas.Task)
async def read_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_task

@router.put('/tasku/{task_id}', response_model=schemas.Task)
async def update_task(task_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    return crud.update_task(db=db, task=task, task_id=task_id)

@router.delete('/taskd/{task_id}', response_model=schemas.Task)
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail='Task not found')
    return crud.delete_task(db=db, task_id=task_id)


