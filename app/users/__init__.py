from apiflask import APIBlueprint

bp = APIBlueprint('users', __name__)

from app.users import routes
