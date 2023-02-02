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
