"""
REFERENCE: 
https://github.com/enkwolf/pwp-course-sensorhub-api-example/blob/master/sensorhub/utils.py
"""

from werkzeug.routing import BaseConverter
from werkzeug.exceptions import NotFound
from gymworkoutapi.models import User, Workout

class UserConverter(BaseConverter):

    def to_python(self, value):
        user = User.query.filter_by(username=value).first()
        if user is None:
            raise NotFound
        return user

    def to_url(self, value):
        if type(value) != User:
            raise NotFound
        return value.username

class WorkoutConverter(BaseConverter):

    def to_python(self, value):
        workout = Workout.query.filter_by(workout_name=value).first()
        if workout is None:
            raise NotFound
        return workout

    def to_url(self, value):
        if type(value) != Workout:
            raise NotFound
        return value.workout_name
