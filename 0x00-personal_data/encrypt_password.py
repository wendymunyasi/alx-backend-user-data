#!/usr/bin/env python3
"""Module for encrypting passwords.
"""


import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using salt.

    Use the bcrypt package to perform the hashing (with hashpw).

    Args:
        password (str): Password to be hashed.

    Returns:
        bytes: byte string of the hashed password.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validate that the provided password matches the hashed password.

    Args:
        hashed_password (bytes): Hashed password.
        password (str): Password to be hashed. LOL.

    Returns:
        bool: True if the hashed password was formed from the given password,
        otherwise False.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
