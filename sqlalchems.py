from sqlalchemy import Column, Integer, String, ForeignKey,  DateTime

from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)

    tasks = relationship("Task", back_populates="owner")  # One-to-Many aloqasi

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    turi = Column(String, nullable=False)
    asos = Column(String)
    buyruq = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)  # Automatically set on creation
    # updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)  # Automatically updated
    mazmuni = Column(String(length=20), nullable=False)
    buyruq_raqami = Column(String(length=20))
    xodim_soni = Column(Integer)
    status = Column(String, nullable=False)
    izoh = Column(String(length=100))
    link = Column(String(length=100))
    link_kimda = Column(String(length=20))
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="tasks")  # Aloqani tasvirlash

class PDFFile(Base):
    __tablename__ = "pdf"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)

