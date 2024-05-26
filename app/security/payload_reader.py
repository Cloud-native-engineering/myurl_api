from flask import request
from app.security.auth0_service import auth0_service

def read_payload():
    # Get the token from the request headers
    token = request.headers.get('Authorization').split()[1]

    # Validate the token and get the payload
    payload = auth0_service.validate_jwt(token)

    return payload