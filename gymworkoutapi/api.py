"""
REFERENCE: https://github.com/enkwolf/pwp-course-sensorhub-api-example/blob/master/sensorhub/api.py
"""

from flask import Blueprint
from flask_restful import Api

from gymworkoutapi.resources.user import UserItem, UserCollection
from gymworkoutapi.resources.workout import WorkoutCollection, WorkoutItem
from gymworkoutapi.resources.movement import MovementItem

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)

api.add_resource(UserCollection, "/users/")
api.add_resource(UserItem, "/users/<user:user>/")
api.add_resource(WorkoutCollection, "/users/<user:user>/workouts/")
api.add_resource(WorkoutItem, "/users/<user:user>/workouts/<workout:workout>/")
api.add_resource(MovementItem, "/users/<user:user>/workouts/<workout:workout>/<movement>/")
