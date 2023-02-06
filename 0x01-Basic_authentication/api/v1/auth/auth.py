#!/usr/bin/env python3
"""
Module for authentication
"""
from typing import List, TypeVar
from flask import request


class Auth():
    """Template for all authentication system implemented in this app.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """This function takes a path and a list of excluded paths as arguments
        and returns a boolean value. The purpose of the function and the way
        it uses the `path` and `excluded_paths` arguments will be determined
        later.
        For now, it simply returns False.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """This function takes a request object as an optional argument
        (defaults to None) and returns a string. The purpose and how the
        request object is used will be determined later.
        For now, it simply returns None.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """This function takes a request object as an optional argument
        (defaults to None) and returns a value of type 'User'. The purpose
        and how the request object is used will be determined later.
        For now, it simply returns None.
        """
        return None
