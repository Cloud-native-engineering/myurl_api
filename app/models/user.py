from apiflask import Schema
from apiflask.fields import Integer, String, Boolean
from apiflask.validators import Length

from app.extensions import db
from app.models.manage import Manage


####
## Schemas for OpenAPI and validation
####
class UserIn(Schema):
    username = String(required=False, validate=Length(min=1, max=25))
    enabled = Boolean(load_default=True)

class UserOut(Schema):
    id = Integer()
    username = String()
    auth0_id = String()
    enabled = Boolean()


####
## Database model
####
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    auth0_id = db.Column(db.String(254), unique=True, nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    enabled = db.Column(db.Boolean, default=True)

    urls = db.relationship('Url', secondary='manages', back_populates='users')
