from apiflask import APIBlueprint

bp = APIBlueprint('urls', __name__)

from app.urls import routes
