#!/usr/bin/env python3
"""Module for Users.
"""


from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """A class representing a user in the system.

    Attributes:
        __tablename__ (str): The name of the table in the database where
        user records are stored.
        id (int): The unique identifier of the user.
        email (str): The email address of the user.
        hashed_password (str): The hashed password of the user.
        session_id (str): The session ID of the user, used to maintain
        user sessions.
        reset_token (str): The reset token of the user, used for password
        resets.
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
