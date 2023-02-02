#!/usr/bin/env python3
"""Module for encrypting passwords.
"""


import logging
import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes the provided password using bcrypt.

    Use the bcrypt package to perform the hashing (with hashpw).

    Args:
        password (str): Password to be hashed.

    Returns:
        bytes: A salted, hashed password in byte string format.
    """
    # Salt and hash the password using the bcrypt package
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates that the provided password matches the hashed password.

    Args:
        hashed_password (bytes): Hashed password.
        password (str): Password to be validated.

    Returns:
        bool: True if the hashed password was formed from the given password,
        otherwise False.
    """
    # Try to match the hashed password with the given password
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    # If there is an exception in the process, log the error message
    except Exception as e:
        logging.error("Error in password validation: {}".format(e))
        return False
