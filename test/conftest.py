# conftest.py

import pytest
from app import create_app
from app.config import TestConfig
import jwt
from datetime import datetime, timedelta, timezone
from test.testdata import create_test_data
from pytest_mock import mocker
from datetime import datetime

# ------
# Mock Services

@pytest.fixture(autouse=True)
def mock_jwks(mocker):
    
    # Mock the get_signing_key function to return the public key object
    mocker.patch('app.security.auth0_service.Auth0Service.get_signing_key', return_value=TestConfig.JWT_SECRET)

@pytest.fixture(autouse=True)
def mock_queue_feed(mocker):
    mocker.patch('app.extensions.QueueFeed.send_message', return_value='mock-message-id')

# Token generation
def get_token(sub, permissions):
    zurich_offset = timedelta(hours=1)
    zurich_tz = timezone(zurich_offset)
    kid = "mock-key-id"
    aud = "mock-audience"
    payload = {
        "sub": sub,
        "iss": 'https://mock-issuer/',
        "aud": 'mock-audience',
        "iat": datetime.now(zurich_tz),
        "exp": datetime.now(zurich_tz) + timedelta(hours=1),
        "permissions": permissions
    }

    # Ensure the signing algorithm matches the expected algorithm for verification (likely RS512 for your key size)
    return jwt.encode(
        payload=payload,
        key=TestConfig.JWT_SECRET,
        algorithm='HS256',
        headers={
            'kid': kid,
            "typ": "JWT",
        }
    )

# ------
# Start Tests
@pytest.fixture
def client():
    app = create_app(config_class=TestConfig)
    app.config.update({
        "TESTING": True,
    })

    with app.app_context():
        create_test_data()

    return app.test_client()
