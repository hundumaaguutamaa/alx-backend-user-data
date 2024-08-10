#!/usr/bin/env python3
"""
Session Expiration Authentication module.

This module extends the SessionAuth class to include session expiration
based on a configurable duration.
"""

from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os

class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class inherits from SessionAuth and adds session expiration.

    This class manages user sessions with expiration based on a session duration.
    """

    def __init__(self):
        """
        Initializes the SessionExpAuth class with session duration.
        """
        super().__init__()
        # Set session duration from environment variable or default to 0
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates a session with an expiration timestamp.

        Args:
            user_id (str, optional): The user ID for which to create a session.

        Returns:
            str: The generated Session ID if user_id is valid, None otherwise.
        """
        # Create a session ID using the parent method
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        
        # Create a session dictionary with expiration information
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves the User ID based on a given Session ID, considering expiration.

        Args:
            session_id (str, optional): The session ID to look up.

        Returns:
            str: The User ID associated with the session ID if not expired, None otherwise.
        """
        if session_id is None:
            return None
        
        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        if self.session_duration <= 0:
            return session_dict['user_id']

        created_at = session_dict.get('created_at')
        if created_at is None:
            return None
        
        # Check if the session has expired
        if datetime.now() > created_at + timedelta(seconds=self.session_duration):
            return None
        
        return session_dict['user_id']
