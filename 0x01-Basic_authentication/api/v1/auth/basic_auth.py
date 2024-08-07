#!/usr/bin/env python3
"""
Basic Authentication module.
"""

from api.v1.auth.auth import Auth

class BasicAuth(Auth):
    """
    BasicAuth class inherits from Auth.
    This class will use basic authentication, but is empty for now.
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]
        
