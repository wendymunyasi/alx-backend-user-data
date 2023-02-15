#!/usr/bin/env python3
"""A simple end-to-end (E2E) integration test for `app.py`.
"""

import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """Test the registration of a user.

    Args:
        email (str): The user's email.
        password (str): The user's password.
    """
    url = "{}/users".format(BASE_URL)
    data = {
        "email": email,
        "password": password
    }
    # Attempt to register a new user
    response = requests.post(url, data=data)
    # print("RESPONSE.STATUSCODE: {}".format(response.status_code))
    # Assert that the response has a 200 status code
    assert response.status_code == 200
    # Assert that the response JSON payload contains the correct data
    assert response.json() == {"email": email, "message": "user created"}
    # Attempt to register the same user again
    response = requests.post(url, data=data)
    # Assert that the response has a 400 status code
    assert response.status_code == 400
    # Assert that the response JSON payload contains the correct data
    assert response.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test logging in with wrong password.

    Args:
        email (str): The email address of the user to log in.
        password (str): The user's password.
    """
    # Send a POST request to the login endpoint with the provided email
    # and an incorrect password
    url = "{}/sessions".format(BASE_URL)
    data = {
        "email": email,
        "password": password
    }
    response = requests.post(url, data=data)
    # print("RESPONSE.STATUSCODE: {}".format(response.status_code))
    # Ensure that the response status code is 401 (Unauthorized)
    assert response.status_code == 401


def profile_unlogged() -> None:
    """Tests behavior of trying to retrieve profile information
    while being logged out.
    """
    url = "{}/profile".format(BASE_URL)
    # Make a GET request to the /profile endpoint
    response = requests.get(url)
    # Assert that the response status code is 403 Forbidden
    assert response.status_code == 403


def log_in(email: str, password: str) -> str:
    """Tests logging in.

    Args:
        email (str): The email address of the user to log in.
        password (str): The user's password.
    """
    url = "{}/sessions".format(BASE_URL)
    data = {
        "email": email,
        "password": password
    }
    # Make a POST request to the login endpoint with the user's credentials
    response = requests.post(url, data=data)
    # Check if the response status code is 401 in case of invalid credentials
    if response.status_code == 401:
        return "Invalid credentials"
    # Check if the response status code is 200 in case of valid credentials
    assert response.status_code == 200
    # Check if email & message keys are present in the response JSON payload
    response_json = response.json()
    assert "email" in response_json
    assert "message" in response_json
    # Check if email in response JSON payload matches the email in the request
    assert response_json["email"] == email
    # Return the session ID from the response cookie
    return response.cookies.get("session_id")


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    # session_id = log_in(EMAIL, PASSWD)
    # profile_logged(session_id)
    # log_out(session_id)
    # reset_token = reset_password_token(EMAIL)
    # update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
