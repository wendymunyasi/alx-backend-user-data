#!/usr/bin/env python3
"""Module for basic authentication
"""
import base64
import binascii
from typing import Tuple, TypeVar

from models.user import User

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
            decoded = base64.b64decode(
                base64_authorization_header,
                validate=True
            )
            # Return the decoded value as UTF8 string
            # you can use decode('utf-8')
            return decoded.decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self, decoded_header: str) -> Tuple[str, str]:
        """Extract the user email and password from the decoded header string.

        Args:
            decoded_header (str): A decoded header string.

        Returns:
            Tuple[str, str]: Tuple containing the user email and password.
        """
        # Return None, None if decoded_header is None or
        # not a string
        if decoded_header is None or not isinstance(decoded_header, str):
            return None, None
        # Attempt to split email and password by first ':'
        try:
            email, password = decoded_header.split(':', 1)
        except ValueError:
            return None, None
        # Return the user email and the user password
        return email, password

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Returns the User instance based on the email and password.

        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's password.

        Returns:
            User: The User instance or None if the user is not found or the
            password is invalid.
        """
        # Return None if user_email or user_pwd is None or not a string
        if not all(map(lambda x: isinstance(x, str), (user_email, user_pwd))):
            return None
        try:
            # Search for the user in the database
            user = User.search(attributes={'email': user_email})
        except Exception:
            return None
        # Return None if there is no user in the database with the given email
        if not user:
            return None
        # Get the first user from the search results
        user = user[0]
        # Return None if the password is invalid
        if not user.is_valid_password(user_pwd):
            return None
        # Return the user instance
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the User instance for a request.

        Args:
            request (:obj:`Request`, optional): The request object. Defaults
            to None.

        Returns:
            User: The User instance based on the request.
        """
        # Get the authorization header from the request
        auth_header = self.authorization_header(request)
        # Extract the Base64 encoded string from the authorization header
        b64_auth_header = self.extract_base64_authorization_header(auth_header)
        # Decode the Base64 encoded string
        dec_header = self.decode_base64_authorization_header(b64_auth_header)
        # Extract the user email and password from the decoded Base64 string
        user_email, user_pwd = self.extract_user_credentials(dec_header)
        # Return the User instance based on the user email and password
        return self.user_object_from_credentials(user_email, user_pwd)
