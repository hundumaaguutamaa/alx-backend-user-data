#!/usr/bin/env python3
"""
This module defines the User model for the users table using SQLAlchemy.
"""


from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    """
    SQLAlchemy model for the users table.
    
    Attributes:
        id (int): The primary key.
        email (str): The user's email (non-nullable).
        hashed_password (str): The user's hashed password (non-nullable).
        session_id (str): The user's session ID (nullable).
        reset_token (str): The user's reset token (nullable).
    """
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(128), nullable=False)
    hashed_password = Column(String(128), nullable=False)
    session_id = Column(String(128), nullable=True)
    reset_token = Column(String(128), nullable=True)

