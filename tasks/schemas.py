from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional
from users.schemas import UserBase
class Base(DeclarativeBase):
    pass 

class TaskBase(Base):
    __tablename__ = "otntask"

    id: Mapped[int] = mapped_column(primary_key=True)
    task_name: Mapped[str] = mapped_column(String(30))
    user_id: Mapped[int] = mapped_column(ForeignKey("UserBase.user_account.id"))
    user: Mapped["UserBase"] = relationship(back_populates="tasks")
    tasks: Mapped[List["TaskTypeBase"]]= relationship(back_populates="task_types", cascade="all, delete_orphan")




class TaskTypeBase(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    task_type_name: Mapped[str] = mapped_column(String(30))
    task_id: Mapped[int] = mapped_column(ForeignKey("otntask.id"))
    task_types: Mapped["TaskBase"] = relationship(back_populates="tasks")
    

"""
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
"""