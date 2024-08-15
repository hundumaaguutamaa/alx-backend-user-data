#!/usr/bin/env python3
"""DB module.
This module provides a class to interact with the database using SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User
from typing import Optional, Dict, Any


class DB:
    """DB class.
    A class used to interact with the database for User-related operations.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance.
        Creates a new engine and session for the database.
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session: Optional[Session] = None

    @property
    def _session(self) -> Session:
        """Memoized session object.
        Returns a session object to interact with the database.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database.

        Args:
            email (str): The email of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The newly created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs: Dict[str, Any]) -> User:
        """Find a user in the database by arbitrary keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments to filter the query.

        Returns:
            User: The first User object that matches the filter criteria.

        Raises:
            NoResultFound: If no user matches the criteria.
            InvalidRequestError: If the query is invalid.
        """
        if not kwargs:
            raise InvalidRequestError("No arguments provided")

        query = self._session.query(User)
        for key, value in kwargs.items():
            if not hasattr(User, key):
                raise InvalidRequestError(f"Invalid attribute: {key}")
            query = query.filter(getattr(User, key) == value)
        
        result = query.first()
        
        if result is None:
            raise NoResultFound("No result found for the given criteria")

        return result

    def update_user(self, user_id: int, **kwargs: Dict[str, Any]) -> None:
        """Update a user in the database with the provided attributes.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments representing the attributes to update.

        Raises:
            ValueError: If an attribute does not correspond to a valid User attribute.
        """
        # Locate the user by ID
        user = self.find_user_by(id=user_id)
        
        # Update user attributes
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, value)
        
        # Commit the changes
        self._session.commit()
