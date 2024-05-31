from http import HTTPStatus
import jwt
from app.utils import json_abort
import traceback


class Auth0Service:
    """Perform JSON Web Token (JWT) validation using PyJWT"""

    def __init__(self):
        self.issuer_url = None
        self.audience = None
        self.algorithm = None
        self.jwks_uri = None


    def initialize(self, jwks_uri, jwt_audience, issuer_url, algorithm):
        self.jwks_uri = jwks_uri
        self.audience = jwt_audience
        self.issuer_url = issuer_url
        self.algorithm = algorithm
        

    def get_signing_key(self, token):
        try:
            jwks_client = jwt.PyJWKClient(self.jwks_uri)

            return jwks_client.get_signing_key_from_jwt(token).key
        except Exception as error:
            json_abort(HTTPStatus.INTERNAL_SERVER_ERROR, {
                "error": "signing_key_unavailable",
                "error_description": error.__str__(),
                "message": "Unable to verify credentials"
            })

    def validate_jwt(self, token):
        try:
            jwt_signing_key = self.get_signing_key(token)
            payload = jwt.decode(token, jwt_signing_key, algorithms=self.algorithm, audience=self.audience, issuer=self.issuer_url)
            return payload
        except jwt.DecodeError:
            return {"error": "invalid_token", "error_description": "Failed to decode token"}
        except jwt.ExpiredSignatureError:
            return {"error": "invalid_token", "error_description": "Token has expired"}
        except Exception as e:
            print(f"Exception type: {type(e)}")
            print("Exception traceback:")
            traceback.print_exc()
            return {"error": "invalid_token", "error_description": f"Unknown error: {str(e)}"}
    
auth0_service = Auth0Service()