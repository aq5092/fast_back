from pydantic import BaseModel
from typing import List, Optional

class TaskBase(BaseModel):
    task_name: str
    

class TaskCreate(BaseModel):
    task_name: str

class Task(TaskBase):
    id: int
    #is_active: bool
    #tasks: List[Task] = []

    class Config:
        orm_mode = True
