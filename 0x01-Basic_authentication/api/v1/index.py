#!/usr/bin/env python3
""" index """

from flask import abort, jsonify
from api.v1.views import app_views

@app_views.route('/api/v1/unauthorized', methods=['GET'])
def unauthorized_route():
    """ Route to trigger a 401 error for testing """
    abort(401)
