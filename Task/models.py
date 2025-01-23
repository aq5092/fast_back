from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    turi = Column(String)
    email = Column(String, unique=True)
    #is_active = Column(Boolean, default=True)

    #posts = relationship('Post', back_populates='author')

#class Post(Base):
#   __tablename__ = 'posts'

#    id = Column(Integer, primary_key=True)
#    title = Column(String)
#    content = Column(String)
#    user_id = Column(Integer, ForeignKey('users.id'))

#   author = relationship('User', back_populates='posts')