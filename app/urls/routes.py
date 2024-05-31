from app.urls import bp
from app.extensions import db, QueueFeed
from app.models.url import Url, UrlIn, UrlOut, ShareUrlIn
from app.models.user import User
from app.models.manage import Manage
from app.security.guards import authorization_guard, permissions_guard, admin_permissions
from app.security.payload_reader import read_payload
from app.users.utils import is_user
from app.urls.utils import is_valid_short_url, is_valid_url, domain_verified, is_manager, is_not_manager, is_url
from app.utils import json_abort
from flask import current_app



####
## view functions
####
@bp.get('/<int:url_id>')
@bp.output(UrlOut)
@bp.doc(security='bearerAuth')
@authorization_guard
def get_url(url_id: int):
    payload = read_payload()

    # Check Access Control
    is_manager(payload.get('sub'), url_id)

    # Get the specific URL by its ID
    url = is_url(url_id)

    # Return the specific URL
    return url

@bp.get('/')
@bp.output(UrlOut(many=True))
@bp.doc(security='bearerAuth')
@authorization_guard
def get_urls():
    # Read the payload using the read_payload function
    payload = read_payload()
    user = User.query.filter_by(auth0_id=payload.get('sub')).first_or_404()
    return user.urls

@bp.post('/')
@bp.input(UrlIn)
@bp.output(UrlOut)
@bp.doc(security='bearerAuth')
@authorization_guard
def create_url(json_data: dict):
    # Read the payload using the read_payload function
    payload = read_payload()

    # Get the sub from the payload
    auth0_id = payload.get('sub') 

    # Use the is_user function to get the user from the database
    user = is_user(auth0_id)

    # Check if the URL is valid
    is_valid_url(json_data['original_url'])

    # Check if Domain is blacklisted or premium
    domain_verified(json_data['original_url'])

    # Check if the URL is valid
    is_valid_short_url(json_data['short_url'])

    # Create the URL
    url = Url(**json_data)
    db.session.add(url)
    db.session.commit()

    # Create a Manage record linking the User to the Url
    manage = Manage(user_id=user.id, url_id=url.id, is_owner=True)
    db.session.add(manage)
    db.session.commit()
    
    current_app.queue_feed.send_message('create', url.original_url, url.short_url)

    return url

@bp.patch('/<int:url_id>')
@bp.input(UrlIn(partial=True))
@bp.output(UrlOut)
@bp.output(UrlOut)
@bp.doc(security='bearerAuth')
def update_url(url_id: int, json_data: dict):
    # Read the payload using the read_payload function
    payload = read_payload()

    # Get the sub from the payload
    auth0_id = payload.get('sub')

    # Get the user from the database using the auth0_id
    user = is_user(auth0_id)

    # Check if the user is a manager of the URL
    is_manager(user.id, url_id)

    # Get the URL
    url = is_url(url_id)
    
    # Check if the short_url is valid
    if 'short_url' in json_data:
        is_valid_short_url(json_data['short_url'])    

    # Check if the original_url is valid
    if 'original_url' in json_data:
        is_valid_url(json_data['original_url'])
        domain_verified(json_data['original_url']) 

    # Update the URL
    for attr, value in json_data.items():
        setattr(url, attr, value)
    db.session.commit()

    current_app.queue_feed.send_message('update', url.original_url, url.short_url)
    
    return url

@bp.delete('/<int:url_id>')
@bp.output({}, status_code=204)
@bp.doc(security='bearerAuth')
@authorization_guard
def delete_url(url_id: int):
    # Read the payload using the read_payload function
    payload = read_payload()

    # Check if the user is the owner of the URL or if the URL is shared with the user
    user = is_manager(payload.get('sub'), url_id)

    # Get the URL
    url = is_url(url_id)
    
    db.session.delete(url)
    db.session.commit()
    
    current_app.queue_feed.send_message('delete', url.original_url, url.short_url)
    return None

# Share URL with another user
@bp.post('/<int:url_id>/share')
@bp.input(ShareUrlIn)
@bp.doc(security='bearerAuth')
@authorization_guard
def post_share(url_id: int, json_data: dict):
    # Read the payload using the read_payload function
    payload = read_payload()

    # Get the sub from the payload
    requestor = is_manager(payload.get('sub'), url_id)

    # Get the user to share the URL with
    share_user = is_user(json_data['username'])

    # Get the URL
    url = is_url(url_id)
    
    is_not_manager(share_user.id, url_id) 
        
    # Create a Manage record linking the share_user to the Url
    manage = Manage(user_id=share_user.id, url_id=url.id, is_owner=False)
    db.session.add(manage)
    db.session.commit()

    return ''

