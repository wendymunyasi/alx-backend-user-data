#!/usr/bin/env python3
"""
Route module for the API
"""


import os
from os import getenv
from typing import Tuple

from flask import Flask, abort, jsonify, request
from flask_cors import CORS, cross_origin

from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
# Create a variable auth initialized to None after the CORS definition
auth = None


# Update api/v1/app.py for using BasicAuth class instead of Auth depending
# on the value of the environment variable AUTH_TYPE, If AUTH_TYPE is equal
# to basic_auth:
#   import BasicAuth from api.v1.auth.basic_auth
#   create an instance of BasicAuth and assign it to the variable auth
# Otherwise, keep the previous mechanism with auth an instance of Auth.
auth_type = getenv('AUTH_TYPE', 'default')
if auth_type == "basic_auth":
    auth = BasicAuth()
else:
    auth = Auth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error: Exception) -> Tuple[jsonify, int]:
    """Error handler for unauthorized requests.

    Args:
        error (Exception): The error raised.

    Returns:
        Tuple[jsonify, int]: JSON response with the error message and a 401
        status code.
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error: Exception) -> Tuple[jsonify, int]:
    """Error handler for unauthorized requests.

    Args:
        error (Exception): The error raised.

    Returns:
        Tuple[jsonify, int]: JSON response with the error message and a 401
        status code.
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def handle_request():
    """
    Handle the request by checking for authentication and authorization.
    """
    # If auth is None, do nothing
    if auth is None:
        return
    # Create list of excluded paths
    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/']
    # if request.path is not part of the list above, do nothing
    # You must use the method require_auth from the auth instance
    if not auth.require_auth(request.path, excluded_paths):
        return
    # If auth.authorization_header(request) returns None, raise the error
    # 401 - you must use abort
    auth_header = auth.authorization_header(request)
    if auth_header is None:
        abort(401)
    # If auth.current_user(request) returns None, raise the error 403 - you
    # must use abort
    user = auth.current_user(request)
    if user is None:
        abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
