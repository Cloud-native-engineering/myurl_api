from apiflask import Schema
from apiflask.fields import Integer, Boolean, String
from apiflask.validators import Length

from app.extensions import db
from app.models.manage import Manage


####
## Schemas for OpenAPI and validation
####
class UrlIn(Schema):
    original_url = String(required=True, validate=Length(min=1, max=50))
    short_url = String(required=True, validate=Length(min=1, max=50))

class UrlOut(Schema):
    id = Integer()
    short_url = String()
    original_url = String()
    created_at = String()
    updated_at = String()
    expires_at = String()
    enabled = Boolean()
    verified = Boolean()

class ShareUrlIn(Schema):
    username = String(required=True, validate=Length(min=1, max=50))

####
## Database model
####
class Url(db.Model):
    __tablename__ = 'urls'
    id = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(db.String(50), unique=True, nullable=False)
    original_url = db.Column(db.String(254), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
    expires_at = db.Column(db.DateTime)
    enabled = db.Column(db.Boolean, default=True)
    verified = db.Column(db.Boolean, default=False)

    users = db.relationship('User', secondary='manages', back_populates='urls', cascade="all, delete", passive_deletes=True)
