from sqlalchemy.orm import Session
from typing import List
import pydantics
import sqlalchems
# User uchun CRUD funksiyalar
def create_user(db: Session, user: pydantics.UserCreate):
    db_user = sqlalchems.User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(sqlalchems.User).filter(sqlalchems.User.id == user_id).first()

# task uchun CRUD funksiyalar
def create_task(db: Session, task: pydantics.TaskCreate, user_id: int):
    task_data = task.dict(exclude={"owner_id"})
    db_task = sqlalchems.Task(**task_data, owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks_by_user(db: Session, user_id: int):
    return db.query(sqlalchems.Task).filter(sqlalchems.Task.owner_id == user_id).all()
