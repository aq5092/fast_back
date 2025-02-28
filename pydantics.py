from pydantic import BaseModel
from typing import List, Optional
from datetime import date, datetime
# Task uchun Pydantic model
class TaskBase(BaseModel):
    hujjat_id: int
    hujjat_turi: str
    buyruq_pdf: str
    created_at: datetime
    mazmuni: str 
    xodim_soni:int
    status: str 
    izoh:str 
    filename: str
    owner_id: int 



class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    pass


class AsosPdfBase(BaseModel):
    id: int 
    filename: str   

class TaskResponse(TaskBase):
    id: int
    owner_id: int
    # username: str

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
