from test.conftest import client
from test.testdata import users, urls
from test.conftest import get_token

####
## Test URL Routes
####
def test_get_urls(client):
    token = get_token(users[0]['auth0_id'], [])
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.get('/api/urls/', headers=headers)
    assert response.status_code == 200
    assert len(response.json) == 2

    
def test_create_url(client):
    token = get_token(users[0]['auth0_id'], [])
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "original_url": "https://www.myurl.com",
        "short_url": "mylink"
    }
    response = client.post('/api/urls/', json=data, headers=headers)
    assert response.status_code == 200
    assert response.json['short_url'] == 'mylink'

def test_create_invalid_url(client):
    token = get_token(users[0]['auth0_id'], [])
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "original_url": "ftp://www.myur2l.com",
        "short_url": "invurl"
    }
    response = client.post('/api/urls/', json=data, headers=headers)
    assert response.status_code == 400

def test_create_blacklisted_url(client):
    token = get_token(users[0]['auth0_id'], [])
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "original_url": "https://evil.com",
        "short_url": "evil"
    }
    response = client.post('/api/urls/', json=data, headers=headers)
    assert response.status_code == 400

def test_create_sameshort(client):
    token = get_token(users[0]['auth0_id'], [])
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "original_url": "https://www.myurl.com",
        "short_url": "myurl"
    }
    response = client.post('/api/urls/', json=data, headers=headers)
    assert response.status_code == 200
    assert response.json['short_url'] == 'myurl'
    
    data = {
        "original_url": "https://www.myurl.com",
        "short_url": "myurl"
    }
    response = client.post('/api/urls/', json=data, headers=headers)
    assert response.status_code == 400

def test_create_premium_url(client):
    token = get_token(users[0]['auth0_id'], [])
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "original_url": "https://www.myurl.com",
        "short_url": "ZYZ"
    }
    response = client.post('/api/urls/', json=data, headers=headers)
    assert response.status_code == 400
    
def test_share_url(client):
    token = get_token(users[0]['auth0_id'], [])
    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "original_url": "https://www.myurl.com",
        "short_url": "share2you"
    }
    response = client.post('/api/urls/', json=data, headers=headers)
    assert response.status_code == 200
    assert response.json['short_url'] == 'share2you'
    url_id = response.json['id']  # Extract the id from the response

    data = {
        "username": "share1"
    }
    response = client.post(f'/api/urls/{url_id}/share', json=data, headers=headers)  # Use the id in the share request
    assert response.status_code == 200

    token_share = get_token(users[2]['auth0_id'], [])
    headers_share = {
        "Authorization": f"Bearer {token_share}"
    }
    response = client.get('/api/urls/', headers=headers_share)
    assert response.status_code == 200
    assert any(url['short_url'] == 'share2you' for url in response.json)
    
def test_delete_url(client):
    token = get_token(users[1]['auth0_id'], [])
    headers = {
        "Authorization": f"Bearer {token}"
    }
    get_id = client.get('/api/urls/', headers=headers)
    id = get_id.json[0]['id']
    short_url = get_id.json[0]['short_url']
    
    response = client.delete(f'/api/urls/{id}', headers=headers)
    assert response.status_code == 204
    
    response = client.get('/api/urls/', headers=headers)
    assert response.status_code == 200
    assert not any(url['short_url'] == short_url for url in response.json)

def test_patch_url(client):
    token = get_token(users[0]['auth0_id'], [])
    headers = {
        "Authorization": f"Bearer {token}"
    }
    get_id = client.get('/api/urls/', headers=headers)
    assert get_id.status_code == 200
    assert len(get_id.json) > 0
    id = get_id.json[0]['id']
    data = {
        "short_url": "newshort"
    } 
    response = client.patch(f'/api/urls/{id}', json=data, headers=headers)
    assert response.status_code == 200

    # Make a GET request to verify the short_url was updated
    response = client.get(f'/api/urls/{id}', headers=headers)
    assert response.status_code == 200
    assert response.json['short_url'] == data['short_url']