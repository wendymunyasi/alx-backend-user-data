#!/usr/bin/env python3
"""Module for authentication.
"""


import logging

import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User

logging.disable(logging.WARNING)


def _hash_password(password: str) -> bytes:
    """Hashes a password and returns bytes.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The hashed password.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user with the given email and password.

        Args:
            email (str): The email of the new user.
            password (str): The password of the new user.

        Returns:
            User: A User object representing the newly created user.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            # Search for the user by email
            self._db.find_user_by(email=email)
            # If a user already exist with the passed email, raise a ValueError
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass
        # If not, hash the password with _hash_password
        hashed_password = _hash_password(password)
        # Save the user to the database using self._db
        user = self._db.add_user(email, hashed_password)
        # Return the User object
        return user