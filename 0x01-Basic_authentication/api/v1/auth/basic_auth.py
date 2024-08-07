#!/usr/bin/env python3
"""
Basic Authentication module.

This module contains the BasicAuth class which implements basic authentication.
"""

import base64
from api.v1.auth.auth import Auth
from typing import TypeVar, Optional

# Define the User type variable; replace with actual User class import if available
User = TypeVar('User')

class BasicAuth(Auth):
    """
    BasicAuth class inherits from Auth.

    This class uses basic authentication to handle authorization headers. 
    It includes methods to extract the Base64 encoded part of the authorization header,
    decode the Base64 string, extract user credentials, and find a User instance based on credentials.
    """

    def extract_base64_authorization_header(self, authorization_header: str) -> Optional[str]:
        """
        Extracts the Base64 part of the Authorization header for Basic Authentication.

        Args:
            authorization_header (str): The Authorization header string.

        Returns:
            Optional[str]: The Base64 encoded part of the header if valid, otherwise None.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]
    
    def decode_base64_authorization_header(self, base64_authorization_header: str) -> Optional[str]:
        """
        Decodes a Base64 encoded string into a UTF-8 string.

        Args:
            base64_authorization_header (str): The Base64 encoded string.

        Returns:
            Optional[str]: The decoded UTF-8 string if valid, otherwise None.
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            return decoded_bytes.decode('utf-8')
        except (TypeError, base64.binascii.Error, UnicodeDecodeError):
            return None
    
    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (Optional[str], Optional[str]):
        """
        Extracts user email and password from the Base64 decoded value.

        Args:
            decoded_base64_authorization_header (str): The decoded Base64 string containing email and password.

        Returns:
            tuple: A tuple (email, password) if valid, otherwise (None, None).
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        
        # Split on the first ':' to ensure that the password can contain ':'
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> Optional[User]:
        """
        Retrieves a User instance based on email and password credentials.

        Args:
            user_email (str): The user's email address.
            user_pwd (str): The user's password.

        Returns:
            Optional[User]: The User instance if credentials are valid, otherwise None.
        """
        if not isinstance(user_email, str) or user_email is None:
            return None
        if not isinstance(user_pwd, str) or user_pwd is None:
            return None

        # Assuming User class has a class method `search` to find users by email
        users = User.search(user_email)
        if not users:
            return None
        
        user = users[0]  # Assume that `search` returns a list of users, and we take the first one
        if not user.is_valid_password(user_pwd):
            return None
        
        return user

    def current_user(self, request=None) -> Optional[User]:
        """
        Retrieves the current User instance based on the request's authorization header.

        Args:
            request: The request object containing the authorization header.

        Returns:
            Optional[User]: The User instance if credentials are valid, otherwise None.
        """
        if request is None:
            return None
        
        authorization_header = request.headers.get('Authorization')
        if authorization_header is None:
            return None
        
        base64_authorization_header = self.extract_base64_authorization_header(authorization_header)
        if base64_authorization_header is None:
            return None
        
        decoded_base64_authorization_header = self.decode_base64_authorization_header(base64_authorization_header)
        if decoded_base64_authorization_header is None:
            return None
        
        user_email, user_pwd = self.extract_user_credentials(decoded_base64_authorization_header)
        if user_email is None or user_pwd is None:
            return None
        
        return self.user_object_from_credentials(user_email, user_pwd)
    
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
