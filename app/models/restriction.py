from apiflask import Schema
from apiflask.fields import Integer, Boolean, String, List
from sqlalchemy.orm import validates

from app.extensions import db


####
## Schemas for OpenAPI and validation
####
class RestrictionIn(Schema):
    short_url = String()
    domain = String()
    is_premium = Boolean(load_default=False)
    is_blacklisted = Boolean(load_default=True)

class RestrictionOut(Schema):
    id = Integer()
    short_url = String()
    domain = String()
    is_premium = Boolean()
    is_blacklisted = Boolean()
    
class RestrictionBlacklistOut(Schema):
    short_urls= List(String())
    domains= List(String())

class RestrictionPremiumOut(Schema):
    short_urls= List(String())

 
####
## Database model
####
class Restriction(db.Model):
    __tablename__ = 'restrictions'
    id = db.Column(db.Integer, primary_key=True)
    short_url = db.Column(db.String(50))
    domain = db.Column(db.String(254))
    is_premium = db.Column(db.Boolean, default=False)
    is_blacklisted = db.Column(db.Boolean, default=True)

    @validates('is_premium', 'is_blacklisted')
    def validate_status(self, key, value):
        if key == 'is_premium' and value is False and self.is_blacklisted is False:
            raise ValueError("At least one of 'is_premium' or 'is_blacklisted' must be True")
        if key == 'is_blacklisted' and value is False and self.is_premium is False:
            raise ValueError("At least one of 'is_premium' or 'is_blacklisted' must be True")
        return value