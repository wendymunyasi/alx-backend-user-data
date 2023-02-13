#!/usr/bin/env python3
"""Session authentication module for the API.
"""


from uuid import uuid4

from .auth import Auth


class SessionAuth(Auth):
    """Session authentication class that inherits from Auth class.

    Args:
        Auth (type): Class inherited from.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a user_id.

        Args:
            user_id (str, optional): The ID of user to create a session for.
            Defaults to None.

        Returns:
            str: The session ID if the user ID is valid, None otherwise.
        """
        # If user_id is not None and is of type str
        if type(user_id) is str:
            # Generate a session ID using the uuid module's uuid4() function
            session_id = str(uuid4())
            # Store the mapping of session ID to user ID in the dictionary,
            # Use this Session ID as key of dictionary user_id_by_session_id,
            # the value for this key must be user_id
            self.user_id_by_session_id[session_id] = user_id
            # Return the session ID
            return session_id
