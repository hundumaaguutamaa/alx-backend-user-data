#!/usr/bin/env python3
"""
Module for initializing Flask Blueprints.

This module sets up the Flask Blueprint for the API version 1, including
the routes and views for the application. It also loads user data from
a file.
"""

from flask import Blueprint

# Create a Blueprint instance for API version 1
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import views to register with the Blueprint
from api.v1.views.index import *
from api.v1.views.users import *
from api.v1.views.session_auth import *

# Load user data from a file
User.load_from_file()
