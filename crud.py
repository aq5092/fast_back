from sqlalchemy.orm import Session
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import FileResponse
import shutil
import os
from typing import List
import pydantics
import sqlalchems
from sqlalchemy.orm import joinedload, subqueryload



# User uchun CRUD funksiyalar
def create_user(db: Session, user: pydantics.UserCreate):
    db_user = sqlalchems.User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# User ma'lumotlarini yangilash
def update_user(db: Session, user_id: int, user_update: pydantics.UserUpdate):
    db_user = db.query(sqlalchems.User).filter(sqlalchems.User.id == user_id).first()
    if not db_user:
        return None  # User topilmasa, None qaytaradi

    # Yangilash uchun qiymatlarni o'rnatish
    db_user.username = user_update.username or db_user.username
    db_user.email = user_update.email or db_user.email

    db.commit()
    db.refresh(db_user)
    return db_user

# Userni o'chirish
def delete_user(db: Session, user_id: int):
    db_user = db.query(sqlalchems.User).filter(sqlalchems.User.id == user_id).first()
    if not db_user:
        return None  # User topilmasa, None qaytaradi

    db.delete(db_user)
    db.commit()
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(sqlalchems.User).filter(sqlalchems.User.id == user_id).first()

def get_users(db: Session):
    return db.query(sqlalchems.User).all()

def get_pdfs(db: Session):
    return db.query(sqlalchems.AsosPdf).all()

# task uchun CRUD funksiyalar
def create_task(db: Session, task: pydantics.TaskCreate, user_id: int):

    task_data = task.dict(exclude={"owner_id"})  # Exclude 'owner_id'

    db_task = sqlalchems.Task(**task_data, owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task




def get_tasks_by_user(db: Session, user_id: int):
    return db.query(sqlalchems.Task).filter(sqlalchems.Task.owner_id == user_id).all()

def get_all_tasks(db: Session):
    return db.query(sqlalchems.Task).options(subqueryload(sqlalchems.Task.owner)).all()


def get_task_by_id(db: Session, task_id: int):
    return db.query(sqlalchems.Task).filter(sqlalchems.Task.id == task_id).first()
# Post ma'lumotlarini yangilash
def update_task(db: Session, task_id: int, task_update: pydantics.TaskUpdate):
    db_task = db.query(sqlalchems.Task).filter(sqlalchems.Task.id == task_id).first()
    if not db_task:
        return None  # Post topilmasa, None qaytaradi
    
    db_task.hujjat_id = task_update.hujjat_id or db_task.hujjat_id
    db_task.hujjat_turi = task_update.hujjat_turi or db_task.hujjat_turi
    db_task.buyruq_pdf = task_update.buyruq_pdf or db_task.buyruq_pdf
    db_task.created_at = task_update.created_at or db_task.created_at
    db_task.mazmuni = task_update.mazmuni or db_task.mazmuni
    db_task.xodim_soni = task_update.xodim_soni or db_task.xodim_soni
    db_task.status = task_update.status or db_task.status
    db_task.izoh = task_update.izoh or db_task.izoh
    db_task.filename = task_update.filename or db_task.filename
    db_task.owner_id = task_update.owner_id or db_task.owner_id

    db.commit()
    db.refresh(db_task)
    return db_task

# Postni o'chirish
def delete_task(db: Session, task_id: int):
    db_task = db.query(sqlalchems.Task).filter(sqlalchems.Task.id == task_id).first()
    if not db_task:
        return None  # Post topilmasa, None qaytaradi

    db.delete(db_task)
    db.commit()
    return db_task

# Userni o'chirish
def delete_pdf(db: Session, filename: str):
    db_pdf = db.query(sqlalchems.AsosPdf).filter(sqlalchems.AsosPdf.filename == filename).first()
    if not db_pdf:
        return None  # User topilmasa, None qaytaradi

    db.delete(db_pdf)
    db.commit()
    return db_pdf