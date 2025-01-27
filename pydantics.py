from pydantic import BaseModel
from typing import List, Optional

# Post uchun Pydantic model
class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

# User uchun Pydantic model
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    posts: List[PostResponse] = []  # Relational ma'lumot

    class Config:
        orm_mode = True
