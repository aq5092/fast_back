from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create a connection to the database
engine = create_engine('sqlite:///database.db')
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

###############################################################################

# import asyncio
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# from sqlalchemy import Column, Integer, String

# # Define the database models
# Base = declarative_base()

# # Set up the async engine and session
# DATABASE_URL = "sqlite+aiosqlite:///example.db"
# engine = create_async_engine(DATABASE_URL, echo=True)

# # Create an async session factory
# async_session = sessionmaker(
#     bind=engine,
#     expire_on_commit=False,
#     class_=AsyncSession
# )

