#!/usr/bin/env python3
"""Module for authentication.
"""


import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes a password and returns bytes.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The hashed password.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
