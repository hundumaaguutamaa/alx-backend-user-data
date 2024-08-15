#!/usr/bin/env python3
"""DB module for interacting with the database using SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User

class DB:
    """DB class for managing database operations.
    """

    def __init__(self) -> None:
        """Initialize a new DB instance with a SQLite database."""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object.

        Returns:
            Session: SQLAlchemy session object.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database.

        Args:
            email (str): The user's email address.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The newly created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by arbitrary keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments for filtering.

        Returns:
            User: The User object matching the provided filters.

        Raises:
            InvalidRequestError: If no arguments are provided.
            NoResultFound: If no matching user is found.
        """
        if not kwargs:
            raise InvalidRequestError("No arguments provided.")
        
        user = self._session.query(User).filter_by(**kwargs).first()
        if user is None:
            raise NoResultFound("No user found with the provided filters.")
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user's attributes.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: The attributes to update.

        Raises:
            ValueError: If an attribute to update is not found on the User model.
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"Attribute {key} not found on User.")
            setattr(user, key, value)

        self._session.commit()
