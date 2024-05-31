from apiflask import APIBlueprint

bp = APIBlueprint('restrictions', __name__)

from app.restrictions import routes
