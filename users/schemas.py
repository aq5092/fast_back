from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from typing import List, Optional

class Base(DeclarativeBase):
    pass

class UserBase(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(30))
    tasks: Mapped[List["Tasks"]] = relationship(back_populates="user", cascade="all, delete-orphan")



class UserCreate(Base):
    name: str
    email: str 


""" class UserBase(BaseModel)
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    #is_active: bool
    #tasks: List[Task] = []

    class Config:
        orm_mode = True
 """