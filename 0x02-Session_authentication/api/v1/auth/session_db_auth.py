#!/usr/bin/env python3
"""
Session database authentication module.
"""

from datetime import datetime, timedelta
from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth

class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class for managing user sessions stored in a database.
    """

    def create_session(self, user_id=None) -> str:
        """
        Creates and stores a session ID for the user in the database.

        Args:
            user_id (str, optional): The user ID for which to create a session.

        Returns:
            str: The created session ID, or None if user_id is invalid.
        """
        session_id = super().create_session(user_id)
        if session_id is None or not isinstance(session_id, str):
            return None

        # Create and save the UserSession instance
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """
        Retrieves the User ID associated with the given session ID.

        Args:
            session_id (str, optional): The session ID to look up.

        Returns:
            str: The User ID, or None if session ID is invalid or expired.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        try:
            # Retrieve session from database
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None

        if not sessions:
            return None

        # Check if session is expired
        session = sessions[0]
        if self.session_duration > 0:
            cur_time = datetime.now()
            exp_time = session.created_at + timedelta(seconds=self.session_duration)
            if exp_time < cur_time:
                return None

        return session.user_id

    def destroy_session(self, request=None) -> bool:
        """
        Destroys the session based on the session ID from the request cookie.

        Args:
            request (flask.Request, optional): The request object.

        Returns:
            bool: True if the session was destroyed, False otherwise.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if session_id is None or not isinstance(session_id, str):
            return False

        try:
            # Retrieve session from database
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False

        if not sessions:
            return False

        # Remove the session from the database
        sessions[0].remove()

        return True
