#!/usr/bin/env python3
"""Module for session expiration
"""


import os
from datetime import datetime as dt, timedelta

from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth is a class that extends the functionality of the
    SessionAuth class.
    It adds session expiration to the authentication mechanism.
    """

    def __init__(self):
        """
        Constructor for the SessionExpAuth class.
        Initializes the session_duration attribute.
        """
        # Call the superclass's constructor
        super().__init__()

        # Get the value of the SESSION_DURATION environment variable
        # Convert it to an integer and assign it to session_duration attribute
        # If the environment variable does not exist or cannot be converted to
        # an integer, set session_duration to 0
        self.session_duration = int(os.environ.get("SESSION_DURATION", 0))

    def create_session(self, user_id: int) -> str:
        """Creates a new session for a user and assigns a session ID.

        The session ID is stored in the user_id_by_session_id dictionary with
        the user_id and creation time as values.
        The session has an expiration time defined by the session_duration
        attribute.

        Args:
            user_id (int): The id of the user to create a session for

        Returns:
            str: The session ID if the session was successfully created, None
        otherwise
        """
        # Call the create_session method of the superclass
        # This will create a session ID and store the user_id to session_id
        # mapping in the user_id_by_session_id dictionary
        sessn_id = super().create_session(user_id)
        # If the session was not created, return None
        if sessn_id is None:
            return None
        # Add the created_at key to the session dictionary
        # The value of this key is the current time
        self.user_id_by_session_id[sessn_id] = {
            'user_id': user_id,
            'created_at': dt.now()
        }
        # Return the session ID
        return sessn_id

    def user_id_for_session_id(self, session_id: str) -> int:
        """Gets the user_id associated with a session ID.

        The session is considered valid if it was created within the
        session_duration time.

        Args:
            session_id (str): The session ID to get the user_id for

        Returns:
            int: The user_id associated with the session ID if the session is
        valid, None otherwise
        """
        # If the session_id is None, return None
        if session_id is None:
            return None
        # If the user_id_by_session_id dictionary does not contain the
        # session_id, return None
        if session_id not in self.user_id_by_session_id:
            return None
        # Get the session info from the user_id_by_session_id dictionary
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None
        # If the session_duration is 0 or less, return the user_id
        if self.session_duration <= 0:
            return session_dict.get("user_id")
        # Get created_at from session info
        created_at = session_dict.get('created_at')
        # If the created_at key does not exist in the session dictionary,
        # return None
        if created_at is None:
            return None
        # Check if the session has expired
        now = dt.now()
        if created_at + timedelta(seconds=self.session_duration) < now:
            return None
        # Calculate the session expiration date
        expires_at = session_dict["created_at"] + \
            timedelta(seconds=self.session_duration)
        # Return None if the current time is past the expiration date
        if expires_at < dt.now():
            return None
        # Return the user_id from the session dictionary if the session
        # has not expired
        return session_dict.get("user_id", None)
