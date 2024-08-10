#!/usr/bin/env python3
"""
Session Authentication module.
"""

from api.v1.auth.auth import Auth
import uuid

class SessionAuth(Auth):
    """
    SessionAuth class inherits from Auth and manages user sessions.
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user_id.

        Args:
            user_id (str): The user ID for which to create a session.

        Returns:
            str: The generated Session ID if user_id is valid, None otherwise.
        """
        if user_id is None:
            return None

        if not isinstance(user_id, str):
            return None

        # Generate a new session ID using uuid4()
        session_id = str(uuid.uuid4())

        # Store the session ID in the dictionary with the user_id as the value
        self.user_id_by_session_id[session_id] = user_id

        return session_id
