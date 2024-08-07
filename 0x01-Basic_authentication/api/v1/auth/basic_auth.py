#!/usr/bin/env python3
"""
Basic Authentication module.

This module contains the BasicAuth class which implements basic authentication.
"""

from api.v1.auth.auth import Auth

class BasicAuth(Auth):
    """
    BasicAuth class inherits from Auth.

    This class uses basic authentication to handle authorization headers. 
    It includes a method to extract the Base64 encoded part of the authorization header.
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header for Basic Authentication.

        Args:
            authorization_header (str): The Authorization header string.

        Returns:
            str: The Base64 encoded part of the header if valid, otherwise None.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]
