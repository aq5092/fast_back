from database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer)
    category = Column(String)
    description = Column(String)
    date = Column(String)
    is_income = Column(Boolean)
    #account_id = Column(Integer, ForeignKey('accounts.id'))
    #account = relationship('Account', back_populates='transactions')
