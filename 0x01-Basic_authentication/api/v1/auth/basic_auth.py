#!/usr/bin/env python3
"""Module for basic authentication
"""
from .auth import Auth


class BasicAuth(Auth):
    """Basic authentication class.

    Args:
        Auth (type): Class inherited from.
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts the Base64 part of the Authorization header.

        Args:
            authorization_header (str): The Authorization header string.

        Returns:
            str: The Base64 part of the Authorization header, or None if the
            header is invalid.
        """
        # Return None if authorization_header is None or if
        # authorization_header is not a string
        if authorization_header is None or not \
                isinstance(authorization_header, str):
            return None
        # Return None if authorization_header doesn’t start by Basic (with a
        # space at the end)
        if not authorization_header.startswith("Basic "):
            return None
        # Otherwise, return the value after Basic (after the space)
        return authorization_header.split("Basic ")[1].strip()

        # ALTERNATIVE SOLUTION
        # ===========================================================================
        # if authorization_header is None or not \
        # isinstance(authorization_header, str):
        #     return None
        # parts = authorization_header.split(" ")
        # if len(parts) != 2 or parts[0] != "Basic":
        #     return None
        # return parts[1]
