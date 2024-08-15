#!/usr/bin/env python3
"""End-to-end integration test for the authentication system."""

import requests

BASE_URL = "http://localhost:5000"

def register_user(email: str, password: str) -> None:
    """Register a new user."""
    url = f"{BASE_URL}/users"
    payload = {"email": email, "password": password}
    response = requests.post(url, data=payload)
    assert response.status_code == 200, "User registration failed"
    assert response.json() == {"email": email, "message": "user created"}, "Unexpected response payload"


def log_in_wrong_password(email: str, password: str) -> None:
    """Attempt to log in with the wrong password."""
    url = f"{BASE_URL}/sessions"
    payload = {"email": email, "password": password}
    response = requests.post(url, data=payload)
    assert response.status_code == 401, "Login with wrong password should fail"


def log_in(email: str, password: str) -> str:
    """Log in with correct credentials and return the session ID."""
    url = f"{BASE_URL}/sessions"
    payload = {"email": email, "password": password}
    response = requests.post(url, data=payload)
    assert response.status_code == 200, "Login failed"
    session_id = response.cookies.get("session_id")
    assert session_id is not None, "Session ID not returned"
    return session_id


def profile_unlogged() -> None:
    """Access profile without being logged in."""
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert response.status_code == 403, "Profile access without login should fail"


def profile_logged(session_id: str) -> None:
    """Access profile while logged in."""
    url = f"{BASE_URL}/profile"
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200, "Profile access while logged in failed"
    assert "email" in response.json(), "Email not found in profile response"


def log_out(session_id: str) -> None:
    """Log out and invalidate the session ID."""
    url = f"{BASE_URL}/sessions"
    cookies = {"session_id": session_id}
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 200, "Logout failed"


def reset_password_token(email: str) -> str:
    """Request a password reset token."""
    url = f"{BASE_URL}/reset_password"
    payload = {"email": email}
    response = requests.post(url, data=payload)
    assert response.status_code == 200, "Password reset token request failed"
    reset_token = response.json().get("reset_token")
    assert reset_token is not None, "Reset token not returned"
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update the user's password using the reset token."""
    url = f"{BASE_URL}/reset_password"
    payload = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put(url, data=payload)
    assert response.status_code == 200, "Password update failed"
    assert response.json() == {"email": email, "message": "Password updated"}, "Unexpected response payload"


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
