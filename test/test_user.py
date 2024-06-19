from test.conftest import client
from test.testdata import users
from test.conftest import get_token

####
## Test User Routes
####
def test_get_user(client):
    token = get_token(users[0]['auth0_id'], ['read:admin',])
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.get('/api/users/', headers=headers)
    assert response.status_code == 200
    assert any(user['auth0_id'] == users[0]['auth0_id'] for user in response.json)
    
def test_me(client):
    token = get_token(users[0]['auth0_id'], [])
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.get('/api/users/me', headers=headers)
    assert response.status_code == 200
    assert response.json['auth0_id'] == users[0]['auth0_id']
