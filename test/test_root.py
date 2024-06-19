from test.conftest import client
from test.testdata import users
from test.conftest import get_token

####
## Test Root Routes
####
def test_validate_jwt(client):
    token = get_token(users[0]['auth0_id'], [])
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.get('/api/', headers=headers)
    assert response.status_code == 200
    assert response.json == {'message': 'MyURLs API', 'version': '1.0.0'}

def test_validate_jwt_negative(client):
    token = get_token('notValidSub', [])
    headers = headers = {
        "Authorization": f"Bearer not_a_valid_token"
    }
    response = client.get('/api/', headers=headers)
    assert response.status_code == 401
