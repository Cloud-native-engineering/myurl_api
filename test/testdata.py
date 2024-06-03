from app.extensions import db
from app.models.user import User
from app.models.url import Url
from app.models.manage import Manage
from app.models.restriction import Restriction

####
## Test data
####
users = [
    {'auth0_id': '123456789123456789123456789@testcorp', 'username': 'user1'},
    {'auth0_id': '223456789123456789123456789@testcorp', 'username': 'user2'},
    {'auth0_id': '323456789123456789123456789@testcorp', 'username': 'share1'},
    {'auth0_id': '423456789123456789123456789@testcorp', 'username': 'share21'},
    {'auth0_id': '523456789123456789123456789@testcorp', 'username': 'admin1'},
    {'auth0_id': '623456789123456789123456789@testcorp', 'username': 'admin2'}
]

urls = [
    {'original_url': 'https://www.testcorp.com', 'short_url': 'test1'},
    {'original_url': 'https://www.testcorp.com', 'short_url': 'test2'},
    {'original_url': 'https://www.testcorp.com', 'short_url': 'test3'},
    {'original_url': 'https://www.testcorp.com', 'short_url': 'test4'},
    {'original_url': 'https://www.testcorp.com', 'short_url': 'test5'},
    {'original_url': 'https://www.testcorp.com', 'short_url': 'test6'}
]

manages = [
    {'url_id': '1', 'user_id': '1', 'is_owner': True},
    {'url_id': '2', 'user_id': '1', 'is_owner': True},
    {'url_id': '3', 'user_id': '2', 'is_owner': True},
    {'url_id': '4', 'user_id': '2', 'is_owner': True},
    {'url_id': '1', 'user_id': '2', 'is_owner': False}
]

restrictions = [
    {'short_url': 'XYZ', 'is_blacklisted': True},
    {'short_url': 'ZYZ', 'is_premium': True, 'is_blacklisted': False},
    {'domain': 'evil.com', 'is_blacklisted': True},
    {'domain': 'unsecure.com', 'is_blacklisted': True}
]


####
## generate test data
####
def create_test_data():
    db.drop_all()  # dieser Befehl löscht alle vorhandenen Datenbankeintraege und Tabellen
    db.create_all()

    # create users
    for user_data in users:
        user = User(**user_data)
        db.session.add(user)

    # create urls
    for url_data in urls:
        url = Url(**url_data)
        db.session.add(url)

    # create mappings
    for manage_data in manages:
        manage = Manage(**manage_data)
        db.session.add(manage)

    # create restrictions
    for restriction_data in restrictions:
        restriction = Restriction(**restriction_data)
        db.session.add(restriction)
    db.session.commit()
