#!/usr/bin/env python3
"""
Session Authentication module.

This module provides session-based authentication using unique session IDs
associated with user IDs. It supports creating sessions, retrieving user
IDs based on session IDs, and destroying sessions.
"""

from api.v1.auth.auth import Auth
from models.user import User
import uuid

class SessionAuth(Auth):
    """
    SessionAuth class inherits from Auth and manages user sessions.

    This class handles the creation of sessions, retrieval of user IDs
    based on session IDs, and destruction of sessions.
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a given user ID.

        Args:
            user_id (str, optional): The user ID for which to create a session.

        Returns:
            str: The generated Session ID if user_id is valid, None otherwise.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        # Generate a new session ID using uuid4
        session_id = str(uuid.uuid4())

        # Store the session ID in the dictionary with the user ID as the value
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves the User ID based on a given Session ID.

        Args:
            session_id (str, optional): The session ID to look up.

        Returns:
            str: The User ID associated with the session ID, or None if not found.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

        # Retrieve the user ID from the dictionary using session_id
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Returns the current user based on the request.

        Args:
            request: The Flask request object.

        Returns:
            User: The current user or None if no user is found.
        """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """
        Destroys the session for the current user based on the request.

        Args:
            request: The Flask request object.

        Returns:
            bool: True if the session was successfully destroyed, False otherwise.
        """
        if request is None:
            return False
        
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        
        # Remove the session ID from the dictionary
        del self.user_id_by_session_id[session_cookie]
        return True
