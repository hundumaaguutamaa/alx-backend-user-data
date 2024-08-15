#!/usr/bin/env python3
"""Auth module.
This module provides authentication-related functionalities, including user registration.
"""

from db import DB
from user import User
import bcrypt
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initialize an Auth instance."""
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """Hashes a password using bcrypt.

        Args:
            password (str): The password to hash.

        Returns:
            bytes: The salted hash of the password.
        """
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with the provided email and password.

        Args:
            email (str): The email of the user to register.
            password (str): The password of the user to register.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            # Check if a user with the provided email already exists
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # If no user exists, create a new one
            hashed_password = self._hash_password(password)
            user = self._db.add_user(email=email, hashed_password=hashed_password)
            return user
