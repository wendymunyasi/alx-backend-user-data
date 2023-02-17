#!/usr/bin/env python3
"""DB module
"""
import logging
from typing import Dict

from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User

logging.disable(logging.WARNING)


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a new user to the db with the given email and hashed password.

        Args:
            email (str): The email address of the new user.
            hashed_password (str): The hashed password of the new user.

        Returns:
            User: A User object representing the new user.
        """
        # Create new user
        new_user = User(email=email, hashed_password=hashed_password)
        try:
            self._session.add(new_user)
            self._session.commit()
        except Exception as e:
            print(f"Error adding user to database: {e}")
            self._session.rollback()
            raise
        return new_user

    def find_user_by(self, **kwargs: Dict[str, str]) -> User:
        """Find a user by specified attributes.

        Raises:
            error: NoResultFound: When no results are found.
            error: InvalidRequestError: When invalid query arguments are passed

        Returns:
            User: First row found in the `users` table.
        """
        session = self._session
        try:
            user = session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound()
        except InvalidRequestError:
            raise InvalidRequestError()
        # print("Type of user: {}".format(type(user)))
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Updates a user's attributes by user ID and arbitrary keyword
        arguments.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Keyword arguments representing the user's attributes to
            update.

        Raises:
            ValueError: If an invalid attribute is passed in kwargs.

        Returns:
            None
        """
        try:
            # Find the user with the given user ID
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError("User with id {} not found".format(user_id))

        # Update user's attributes
        for key, value in kwargs.items():
            if not hasattr(user, key):
                # Raise error if an argument that does not correspond to a user
                # attribute is passed
                raise ValueError("User has no attribute {}".format(key))
            setattr(user, key, value)

        try:
            # Commit changes to the database
            self._session.commit()
        except InvalidRequestError:
            # Raise error if an invalid request is made
            raise ValueError("Invalid request")
