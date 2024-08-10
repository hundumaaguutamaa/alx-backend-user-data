#!/usr/bin/env python3
"""
Session Expiration Authentication module.

This module extends session-based authentication by adding expiration
dates to session IDs.
"""

from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os

class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class inherits from SessionAuth and manages user sessions
    with expiration dates.
    """

    def __init__(self):
        """
        Initialize the SessionExpAuth instance.

        Sets the session duration from the environment variable SESSION_DURATION.
        """
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a given user ID with an expiration date.

        Args:
            user_id (str, optional): The user ID for which to create a session.

        Returns:
            str: The generated Session ID if user_id is valid, None otherwise.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves the User ID based on a given Session ID, considering expiration.

        Args:
            session_id (str, optional): The session ID to look up.

        Returns:
            str: The User ID associated with the session ID, or None if not found or expired.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        created_at = session_dict.get('created_at')
        if created_at is None:
            return None

        if datetime.now() > created_at + timedelta(seconds=self.session_duration):
            return None

        return session_dict.get('user_id')
