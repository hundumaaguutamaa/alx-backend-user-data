#!/usr/bin/env python3
"""
Flask app for user registration.
"""

from flask import Flask, request, jsonify
from auth import Auth

app = Flask(__name__)
AUTH = Auth()

@app.route('/users', methods=['POST'])
def register_user():
    """POST /users
    Registers a new user with the provided email and password.
    Returns:
        JSON response with a success or error message.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
