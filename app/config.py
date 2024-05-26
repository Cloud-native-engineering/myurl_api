import os
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ISSUER_URL = os.environ.get('JWT_ISSUER_URL')
    JWT_AUDIENCE = os.environ.get('JWT_AUDIENCE')
    JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM') or 'RS256'
    JWKS_URI = os.environ.get('JWKS_URI')
    SQS_QUEUE_URL = os.environ.get('SQS_QUEUE_URL')

    
class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ISSUER_URL = 'https://mock-issuer/'
    JWT_AUDIENCE =  'mock-audience'
    JWT_ALGORITHM = 'HS256'
    JWT_SECRET = 'mock-secret'
    SQS_QUEUE_URL = 'http://mock-queue'
