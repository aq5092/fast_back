from pydantic import BaseModel
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    #is_active: bool
    #posts: List[Post] = []

    class Config:
        orm_mode = True
