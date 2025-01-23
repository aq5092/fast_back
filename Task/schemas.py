from pydantic import BaseModel
from typing import List, Optional

class TaskBase(BaseModel):
    name: str
    



class User(UserBase):
    id: int
    #is_active: bool
    #posts: List[Post] = []

    class Config:
        orm_mode = True
