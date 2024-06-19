from app.models.user import User
from app.utils import json_abort
from random_username.generate import generate_username
from app.extensions import db

####
## Utility Functions about Users
####
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if user is None:
        json_abort(404, {"error": "User not found", "identifier": user_id})
    return user

def get_user_by_auth0_id(auth0_id):
    user = User.query.filter_by(auth0_id=auth0_id).first()
        # If the user doesn't exist, create a new one
    if user is None:
        # Generate random username
        username = generate_username()[0]
        
        # Try to get the user by username
        while User.query.filter_by(username=username).first() is not None:
            # If the username already exists, generate a new one
            username = generate_username()[0]

        user = User(auth0_id=auth0_id, username=username)
        db.session.add(user)
        db.session.commit()

    return user

def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        json_abort(404, {"error": "User not found", "identifier": username})
    return user

def is_user(identifier):
    if isinstance(identifier, int):
        return get_user_by_id(identifier)
    elif isinstance(identifier, str) and len(identifier) > 25:
        return get_user_by_auth0_id(identifier)
    else:
        return get_user_by_username(identifier)

def username_exists(username):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        json_abort(409, {"error": "Username already exists", "username": username})
    return True
