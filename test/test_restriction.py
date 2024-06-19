from test.conftest import client
from test.testdata import users, restrictions
from test.conftest import get_token

####
## Test Restrictions Routes
####
def test_get_restrictions(client):
    token = get_token(users[0]['auth0_id'], ['read:admin', ])
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.get('/api/restrictions/', headers=headers)
    assert response.status_code == 200

def test_get_restrictions_negative(client):
    token = get_token(users[0]['auth0_id'], [])
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.get('/api/restrictions/', headers=headers)
    assert response.status_code == 403
    
def test_create_restriction(client):
    token = get_token(users[0]['auth0_id'], ['write:admin', ])
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "domain": "mybaddomain.com",
        "is_blacklisted": True
    }  
    response = client.post('/api/restrictions/', json=data, headers=headers)
    assert response.status_code == 200
    assert response.json['domain'] == data['domain']
    assert response.json['is_blacklisted'] == data['is_blacklisted']
    assert response.json['is_premium'] == False

def test_blacklisted(client):
    token = get_token(users[0]['auth0_id'], [])
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.get('/api/restrictions/blacklisted', headers=headers)
    assert response.status_code == 200
    assert 'evil.com' in response.json['domains']
    assert 'XYZ' in response.json['short_urls']

def test_premium(client):
    token = get_token(users[0]['auth0_id'], [])
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.get('/api/restrictions/premium', headers=headers)
    assert response.status_code == 200
    assert 'ZYZ' in response.json['short_urls']
    
def test_delete_restriction(client):
    token = get_token(users[0]['auth0_id'], ['write:admin', ])
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.delete('/api/restrictions/1', headers=headers)
    assert response.status_code == 204
    
def test_delete_restriction_negative(client):
    token = get_token(users[0]['auth0_id'], [])
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.delete('/api/restrictions/1', headers=headers)
    assert response.status_code == 403

def test_get_restrictions_id(client):
    token = get_token(users[0]['auth0_id'], ['read:admin', ])
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.get('/api/restrictions/2', headers=headers)
    assert response.status_code == 200
    assert response.json['short_url'] == restrictions[1]['short_url']

def test_patch_restriction(client):
    token = get_token(users[0]['auth0_id'], ['write:admin', ])
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "is_blacklisted": False
    }
    response = client.patch('/api/restrictions/2', json=data, headers=headers)
    assert response.status_code == 200
    assert response.json['is_blacklisted'] == False
 