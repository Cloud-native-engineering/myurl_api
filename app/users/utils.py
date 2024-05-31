from app.models.user import User
from app.utils import json_abort

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
    if user is None:
        json_abort(404, {"error": "User not found", "identifier": auth0_id})
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
