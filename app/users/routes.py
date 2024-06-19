from app.users import bp
from app.extensions import db
from app.models.user import User, UserIn, UserOut
from app.models.url import UrlOut
from app.security.guards import authorization_guard, permissions_guard, admin_permissions
from app.security.payload_reader import read_payload
from app.users.utils import get_user_by_id, get_user_by_auth0_id, get_user_by_username, username_exists, is_user
from flask import request


####
## view functions
####
@bp.get('/<int:user_id>')
@bp.output(UserOut)
@bp.doc(security='bearerAuth')
@authorization_guard
@permissions_guard([admin_permissions.read])
def get_user(user_id: int):
    return get_user_by_id(user_id)

@bp.get('/')
@bp.output(UserOut(many=True))
@bp.doc(security='bearerAuth')
@authorization_guard
@permissions_guard([admin_permissions.read])
def get_users():
    return User.query.all()

@bp.post('/')
@bp.input(UserIn)
@bp.output(UserOut)
@bp.doc(security='bearerAuth')
@authorization_guard
@permissions_guard([admin_permissions.write])
def create_user(json_data: dict):
    if 'username' in json_data:
        username_exists(json_data['username'])

    user = User(**json_data)
    db.session.add(user)
    db.session.commit()
    return user

@bp.patch('/<int:user_id>')
@bp.input(UserIn(partial=True))
@bp.output(UserOut)
@bp.doc(security='bearerAuth')
@authorization_guard
@permissions_guard([admin_permissions.write])
def update_user(user_id: int, json_data: dict):
    user = db.get_or_404(User, user_id)
    for attr, value in json_data.items():
        setattr(user, attr, value)
    db.session.commit()
    return user

@bp.delete('/<int:user_id>')
@bp.output({}, status_code=204)
@bp.doc(security='bearerAuth')
@authorization_guard
@permissions_guard([admin_permissions.write])
def delete_user(user_id: int):
    user = get_user_by_id(user_id)
    db.session.delete(user)
    db.session.commit()
    return None

@bp.get('/<int:user_id>/urls')
@bp.output(UrlOut(many=True))
@bp.doc(security='bearerAuth')
@authorization_guard
@permissions_guard([admin_permissions.read])
def get_user_urls(user_id: int):
    user = db.get_or_404(User, user_id)
    return user.urls

@bp.get('/me')
@bp.output(UserOut)
@bp.doc(security='bearerAuth')
@authorization_guard
def get_me():
     # Read the payload using the read_payload function
    payload = read_payload()
     
    return is_user(payload.get('sub'))

@bp.patch('/me')
@bp.input(UserIn(partial=True))
@bp.output(UserOut)
@bp.doc(security='bearerAuth')
@authorization_guard
def patch_me(json_data: dict):
    payload = read_payload()

    user = get_user_by_auth0_id(payload.get('sub'))

    if 'username' in json_data:
      username_exists(json_data['username']) 

    for key, value in json_data.items():
        if hasattr(user, key):
            setattr(user, key, value)

    db.session.commit()
    return user
    
@bp.delete('/me')
@bp.output({}, status_code=204)
@bp.doc(security='bearerAuth')
def delete_me():
    payload = read_payload()
    user = get_user_by_auth0_id(payload.get('sub'))
    for url in list(user.urls):  # create a copy of user.urls
        if len(url.users) == 1:
            user.urls.remove(url)
            if len(url.users) == 0:  # check if the url is not associated with any user
                db.session.delete(url)
    db.session.delete(user)
    db.session.commit()
    return None