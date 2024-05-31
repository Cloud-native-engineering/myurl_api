from apiflask import Schema
from apiflask.fields import Integer, Boolean

from app.extensions import db


####
## Schemas for OpenAPI and validation
####
class ManageUserIn(Schema):
    user_id = Integer(required=True)
    is_owner = Boolean(required=True)
    
class ManageUrlIn(Schema):
    url_id = Integer(required=True)

class UserUrlOut(Schema):
    id = Integer()
    user_id = Integer()
    is_owner = Boolean()


####
## Database model
####
class Manage(db.Model):
    __tablename__ = 'manages'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    url_id = db.Column(db.Integer, db.ForeignKey('urls.id'), nullable=False)
    is_owner = db.Column(db.Boolean, default=False)
