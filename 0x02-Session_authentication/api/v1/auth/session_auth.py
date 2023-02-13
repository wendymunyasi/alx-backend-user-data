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

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves the user ID for a given session ID.

        Args:
            session_id (str, optional): The session ID to retrieve the user
            ID for.
            Defaults to None.

        Return None if session_id is None.
        Return None if session_id is not a string.
        Return the value (the User ID) for the key session_id in the dictionary
        user_id_by_session_id.

        Returns:
            str: The user ID if the session ID is valid, None otherwise.
        """
        # If session_id is not None or is a string
        if type(session_id) is str:
            # Return the value (user ID) for the key session_id in dictionary
            # user_id_by_session_id
            return self.user_id_by_session_id.get(session_id)
