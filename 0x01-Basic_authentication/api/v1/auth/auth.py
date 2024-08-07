#!/usr/bin/env python3
"""
Authentication module.
"""

from flask import request
from typing import List, TypeVar

class Auth:
    """
    Auth class to manage the API authentication.
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if a given path requires authentication.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths that are excluded from authentication.

        Returns:
            bool: True if the path requires authentication, False otherwise.
        """
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        # Ensure the path ends with a slash for comparison
        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            # Check for wildcard patterns
            if excluded_path.endswith('*'):
                pattern = excluded_path.rstrip('*')
                if path.startswith(pattern):
                    return False
            elif path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the value of the Authorization header from the request.

        Args:
            request: The Flask request object.

        Returns:
            str: The value of the Authorization header if present, None otherwise.
        """
        if request is None:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns the current user based on the request.

        Args:
            request: The Flask request object.

        Returns:
            TypeVar('User'): None, as no user is identified for now.
        """
        return None
