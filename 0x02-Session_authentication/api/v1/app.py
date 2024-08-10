#!/usr/bin/env python3
"""
Route module for the API.

This module sets up the Flask application, registers the API views,
configures CORS, and manages authentication based on environment variables.
It also defines error handlers and a before_request function to filter requests.
"""

from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS
import os

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize the auth variable
auth = None

# Load the appropriate auth class based on the environment variable
AUTH_TYPE = getenv("AUTH_TYPE")

if AUTH_TYPE:
    if AUTH_TYPE == "basic_auth":
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    elif AUTH_TYPE == "auth":
        from api.v1.auth.auth import Auth
        auth = Auth()

@app.errorhandler(404)
def not_found(error) -> str:
    """
    Handler for 404 errors.

    Args:
        error: The error object.

    Returns:
        str: A JSON response with error message and status code 404.
    """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Handler for 401 errors.

    Args:
        error: The error object.

    Returns:
        str: A JSON response with error message and status code 401.
    """
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Handler for 403 errors.

    Args:
        error: The error object.

    Returns:
        str: A JSON response with error message and status code 403.
    """
    return jsonify({"error": "Forbidden"}), 403

@app.before_request
def before_request():
    """
    Filters requests to handle authentication before processing the request.
    
    If authentication is required:
    - Checks if the Authorization header is present and valid.
    - Checks if the current user is authenticated.
    Raises:
        401: If the Authorization header is missing.
        403: If the current user is not authenticated.
    """
    if auth is None:
        return

    # List of paths that do not require authentication
    excluded_paths = ['/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']
    
    # Check if the request path requires authentication
    if not auth.require_auth(request.path, excluded_paths):
        return

    # Check for the Authorization header
    if auth.authorization_header(request) is None:
        abort(401)

    # Check the current user
    if auth.current_user(request) is None:
        abort(403)

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
