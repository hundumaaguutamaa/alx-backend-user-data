#!/usr/bin/env python3
"""
Auth module for managing user authentication.
"""

import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """Hashes a password using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def register_user(self, email: str, password: str) -> User:
        """Registers a new user and returns the User object.
        
        Raises:
            ValueError: If the user already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user login credentials.

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            bool: True if the credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)
        except (NoResultFound, AttributeError):
            return False

    def _generate_uuid(self) -> str:
        """Generates a new UUID and returns it as a string.

        Returns:
            str: The string representation of the UUID.
        """
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """Creates a session for a user and returns the session ID.

        Args:
            email (str): The user's email address.

        Returns:
            str: The session ID as a string.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        
        session_id = self._generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        
        return session_id

    def get_reset_password_token(self, email: str) -> str:
        """Generates a reset password token for a user and returns it.

        Args:
            email (str): The user's email address.

        Returns:
            str: The reset password token as a string.

        Raises:
            ValueError: If the user with the given email does not exist.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError(f"User with email {email} not found")
        
        reset_token = self._generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates the password for a user identified by the reset token.

        Args:
            reset_token (str): The reset token associated with the user.
            password (str): The new password to set.

        Raises:
            ValueError: If no user with the given reset token is found.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError(f"Invalid reset token: {reset_token}")

        hashed_password = self._hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_password, reset_token=None)
