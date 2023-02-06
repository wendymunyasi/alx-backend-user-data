#!/usr/bin/env python3
"""Module for basic authentication
"""
import base64

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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decodes the Base64 string `base64_authorization_header` and
        returns the decoded value as a UTF8 string.

        Args:
            base64_authorization_header (str): A Base64 encoded string to be
            decoded.

        Returns:
            str: The decoded value as a UTF8 string.
        """
        # Return None if base64_authorization_header is None
        if base64_authorization_header is None:
            return None
        # Return None if base64_authorization_header is not a string
        if not isinstance(base64_authorization_header, str):
            return None
        # Return None if base64_authorization_header is not a valid Base64
        # Attempt to decode the base64 string & return None if an error occurs
        try:
            decoded = base64.b64decode(base64_authorization_header)
        except Exception:
            return None
        # Otherwise, return the decoded value as UTF8 string
        # you can use decode('utf-8')
        return decoded.decode('utf-8')
