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
    return db.query(User).filter(User.id == user_id).first()

# Post uchun CRUD funksiyalar
def create_post(db: Session, post: pydantics.PostCreate, user_id: int):
    db_post = sqlalchems.Post(**post.dict(), owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_posts_by_user(db: Session, user_id: int):
    return db.query(Post).filter(Post.owner_id == user_id).all()
