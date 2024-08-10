#!/usr/bin/env python3
"""
Session Database Authentication module.

This module extends SessionExpAuth to store session data in a database.
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth class inherits from SessionExpAuth and uses database storage for sessions.
    """

    def __init__(self):
        """
        Initializes the SessionDBAuth class.
        """
        super().__init__()
        # Setup database connection
        db_url = os.getenv('DB_URL')
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def create_session(self, user_id=None):
        """
        Creates and stores a session in the database.

        Args:
            user_id (str, optional): The user ID for which to create a session.

        Returns:
            str: The generated Session ID if user_id is valid, None otherwise.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # Store the session in the database
        try:
            with self.Session() as session:
                new_session = UserSession(user_id=user_id, session_id=session_id)
                session.add(new_session)
                session.commit()
        except SQLAlchemyError:
            return None

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves the User ID based on a given Session ID from the database.

        Args:
            session_id (str, optional): The session ID to look up.

        Returns:
            str: The User ID associated with the session ID if not expired, None otherwise.
        """
        if session_id is None:
            return None

        try:
            with self.Session() as session:
                user_session = session.query(UserSession).filter_by(session_id=session_id).first()
                if user_session:
                    return super().user_id_for_session_id(session_id)
        except SQLAlchemyError:
            return None

        return None

    def destroy_session(self, request=None):
        """
        Destroys the UserSession based on the Session ID from the request cookie.

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
        
        try:
            with self.Session() as session:
                session.query(UserSession).filter_by(session_id=session_cookie).delete()
                session.commit()
        except SQLAlchemyError:
            return False
        
        return super().destroy_session(request)

