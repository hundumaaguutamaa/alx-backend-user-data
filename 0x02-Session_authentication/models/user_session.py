#!/usr/bin/env python3
"""User session module.

This module defines the UserSession class, which represents a user session
in the system. The class provides attributes for user ID and session ID.
"""

from models.base import Base


class UserSession(Base):
    """User session class.

    This class represents a user session, storing the user ID and session ID
    associated with a particular session.
    """

    def __init__(self, *args: list, **kwargs: dict):
        """Initializes a UserSession instance.

        Args:
            *args (list): Positional arguments to pass to the base class.
            **kwargs (dict): Keyword arguments, including 'user_id' and
            'session_id', to initialize the user session.
        """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
