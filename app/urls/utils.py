from app.models.url import Url
from app.models.restriction import Restriction
from app.models.manage import Manage
from app.users.utils import is_user
from app.utils import json_abort
import re
import tldextract
import boto3

####
## Utility Functions about URLs
####
def get_domain(url):
    extracted = tldextract.extract(url)
    return f"{extracted.domain}.{extracted.suffix}"

def is_manager(auth0_id, url_id):
    # Check if the user exists
    user = is_user(auth0_id)

    # Check if the user is a manager
    manage = Manage.query.filter_by(user_id=user.id, url_id=url_id).first()
    if manage is None:
        json_abort(404, {"error": "User is not a manager of the URL", "url_id": url_id})

    return user

def is_not_manager(auth0_id, url_id):
    try:
        # Try to check if the user is a manager
        is_manager(auth0_id, url_id)
    except:
        # If an error is raised, the user is not a manager
        return True

    # If no error is raised, the user is a manager
    json_abort(400, {"error": "User is already a manager of the URL", "url_id": url_id})

def is_url(url_id: int):
    url = Url.query.get(url_id)
    if url is None:
        json_abort(404, {"error": "URL not found", "url_id": url_id})

    return url

def is_valid_short_url(short_url):
    if not re.match('^[a-zA-Z0-9]*$', short_url):
        json_abort(400, {"error": "Short_URL contains invalid characters", "short_url": short_url})

    # If the short_url is in the database and is premium or is blacklisted, return False
    restriction_record = Restriction.query.filter(Restriction.short_url.like(f"%{short_url}%")).first()
    if restriction_record is not None:
        if restriction_record.is_premium or restriction_record.is_blacklisted:
            json_abort(400, {"error": "Short_URL is premium or blacklisted", "short_url": short_url})

    # If there is more than one short_url in the database, return False
    urls = Url.query.filter_by(short_url=short_url).all()

    if len(urls) > 0:
        json_abort(400, {"error": "Short_URL is already used", "short_url": short_url})  

    # If the short_url is in the database, is not premium, and is not blacklisted, return True
    if not urls:
        return True

    
def is_valid_url(url):
    # Define the regex for a valid URL
    url_regex = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    # Check if the original_url is a valid URL and its length is less than or equal to 254
    if re.match(url_regex, url) and len(url) <= 254:
        return True
    else:
       json_abort(400, {"error": "Invalid URL", "url": url}) 

    
def domain_verified(url):
    # Parse the URL to domain
    domain = get_domain(url)
    
    # Query the restriction database for the domain
    restriction = Restriction.query.filter(Restriction.domain.like(f"%{domain}")).first()

    # If the domain is not in the database, return False
    if restriction is None:
        return False

    # If the domain is in the database and is premium and not blacklisted, return True
    if restriction.is_premium or restriction.is_blacklisted:
       json_abort(400, {"error": "URL is premium or blacklisted", "url": url}) 

        # If the domain is in the database and is verified, return True
    if restriction.is_verified:
        return True

    # If the domain is in the database but is not premium or is blacklisted, return False
    return False

def short_url_exists(short_url):
    url = Url.query.filter_by(short_url=short_url).first()
    if url is not None:
        json_abort(404, {"error": "Short URL already exists", "short_url": short_url})

    return True

    

