#!/usr/bin/env python3
"""
Session database authentication module.
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
import uuid

class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class for managing user sessions stored in a database.
    """

    def create_session(self, user_id=None) -> str:
        """
        Create a session ID for the user and store it in the database.

        Args:
            user_id (str, optional): The user ID for which to create a session.

        Returns:
            str: The created session ID or None if user_id is invalid.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # Create a new UserSession instance
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()  # Save to file-based database

        return session_id

    def user_id_for_session_id(self, session_id=None) -> str:
        """
        Retrieve the User ID associated with the given session ID.

        Args:
            session_id (str, optional): The session ID to look up.

        Returns:
            str: The User ID or None if session ID is invalid or expired.
        """
        if session_id is None:
            return None

        # Retrieve session from database
        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return None

        # Ensure session is not expired
        user_id = super().user_id_for_session_id(session_id)
        if user_id is None:
            return None

        return user_session[0].user_id

    def destroy_session(self, request=None) -> bool:
        """
        Destroy the session based on the session ID from the request cookie.

        Args:
            request (flask.Request, optional): The request object.

        Returns:
            bool: True if the session was destroyed, False otherwise.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        # Retrieve session from database
        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return False

        # Delete session from database
        user_session[0].remove()

        return True
