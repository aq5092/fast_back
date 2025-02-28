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
 
 # buyruq_pdf = Column(String)
    # created_at = Column(DateTime, default=datetime.utcnow, nullable=False)  # Automatically set on creation
    # mazmuni = Column(String(length=20), nullable=False)
    # xodim_soni = Column(Integer)
    # status = Column(String, nullable=False)
    # izoh = Column(String(length=100))
    
class Task(Base):
    __tablename__ = "tasks2"

    id = Column(Integer, primary_key=True, index=True)
    hujjat_id = Column(Integer, nullable=False)
    hujjat_turi = Column(String, nullable=False)
    buyruq_pdf = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)  # Automatically set on creation
    mazmuni = Column(String(length=20), nullable=False)
    xodim_soni = Column(Integer)
    status = Column(String, nullable=False)
    izoh = Column(String(length=100))
    filename = Column(String, ForeignKey("asos.filename"))
    asos = relationship("AsosPdf", back_populates="asos_pdf")
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")  # Aloqani tasvirlash


class AsosPdf(Base):
    __tablename__ = "asos"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    asos_pdf = relationship("Task", back_populates="asos")  # One-to-Many aloqasi

# class PDFFile(Base):
#     __tablename__ = "pdf"
#     id = Column(Integer, primary_key=True, index=True)
#     filename = Column(String, unique=True, index=True)

