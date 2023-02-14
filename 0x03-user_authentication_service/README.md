# Simple User authentication service


## Files

- `user.py`: user model
- `app.py`: entry point of the API
- `auth.py`: authentication model


## Run

```
$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m app
```

## Routes

- `GET /`: returns the JSON payload with homepage content
- `POST /users`: returns JSON payload of the form containing various user info
- `POST /sessions`: returns JSON payload of the form containing login info
- `DELETE /sessions`: deletes a user session based on the ID
- `GET /profile`: returns A JSON payload containing the email if successful
- `POST /reset_password`: returns A JSON payload containing the email & reset token if successful
- `PUT /reset_password`: returns A JSON payload containing the email & message `Password updated` if successful