#!/usr/bin/env python3
"""Module for session database authentication
"""
from datetime import datetime, timedelta

from models.user_session import UserSession

from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """Session authentication class with database storage & expiration support.
    """

    def create_session(self, user_id: str) -> str:
        """Creates and stores a session id for the user.

        Args:
            user_id (str): User id to be associated with the session.

        Returns:
            str: Session id.
        """
        # Call the parent method to create a session id
        session_id = super().create_session(user_id)

        # Check if a session id is returned
        if isinstance(session_id, str):
            # Create a new UserSession instance and store it
            kwargs = {
                'user_id': user_id,
                'session_id': session_id,
            }
            user_session = UserSession(**kwargs)
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id: str) -> str:
        """Retrieves the user id of the user associated with given session id.

        Args:
            session_id (str): Session id.

        Returns:
            str: User id associated with the session id.
        """
        try:
            # Try to retrieve the UserSession instance from the database
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            # Return None in case of an error
            return None
        if len(sessions) <= 0:
            # Return None if the session id is not found
            return None
        # Check the expiration time of the session
        cur_time = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        exp_time = sessions[0].created_at + time_span
        if exp_time < cur_time:
            # Return None if the session has already expired
            return None
        # Return the user id associated with the session
        return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        """Destroys an authenticated session.

        Args:
            request (Request): Request object.

        Returns:
            bool: Indicates if the session was destroyed successfully.
        """
        # Get the session id from the request cookie
        session_id = self.session_cookie(request)
        try:
            # Try to retrieve the UserSession instance from the database
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            # Return False in case of an error
            return False
        if len(sessions) <= 0:
            # Return False if the session id is not found
            return False
        # Remove the UserSession instance from the database
        sessions[0].remove()
        return True
