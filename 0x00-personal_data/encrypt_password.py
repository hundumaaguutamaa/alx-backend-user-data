#!/usr/bin/env python3
"""A module for encrypting and verifying passwords.
"""

import bcrypt

def hash_password(password: str) -> bytes:
    """
    Hashes a password with a salt using bcrypt.

    Args:
        password (str): The plain text password to hash.

    Returns:
        bytes: The salted and hashed password.
    """
    # Hash the password with a new salt
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Verifies if the provided password matches the hashed password.

    Args:
        hashed_password (bytes): The hashed password to check against.
        password (str): The plain text password to verify.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    # Check if the password matches the hashed password
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
