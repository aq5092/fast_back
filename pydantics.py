from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
# Task uchun Pydantic model
class TaskBase(BaseModel):
    turi: str
    asos: str
    buyruq: str
    created_at: datetime
    updated_at: datetime
    asos: str 
    buyruq_raqami: str
    xodim_soni:int
    status: str 
    izoh:str 
    link:str 
    link_kimda: str 
    owner_id: str 



class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass


class TaskResponse(TaskBase):
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

class UserUpdate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    tasks: List[TaskResponse] = []  # Relational ma'lumot

    class Config:
        orm_mode = True
