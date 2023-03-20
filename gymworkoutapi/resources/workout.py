"""
REFERENCE: https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/
"""

import json
from flask import request, Response
from flask_restful import Resource
from jsonschema import validate, ValidationError
from werkzeug.exceptions import BadRequest, Conflict
from sqlalchemy.exc import IntegrityError
from gymworkoutapi import db
from gymworkoutapi.models import Workout, Movement

class WorkoutCollection(Resource):
    """
    Class for the WorkoutCollection resource.
    WorkoutCollection is a collection of workouts by the user
    which has GET and POST methods.
    """

    def get(self, user):
        """
        Get method for WorkoutCollection resource
        With this method, the workout collection can be fetched.
        """

        workouts = Workout.query.filter_by(user_id=user.id).all()
        response_data = []
        while workouts:
            workout = workouts.pop()
            response_data.append(workout.serialize())
        return Response(json.dumps(response_data), 200)

    def post(self, user):
        """
        Post method for WorkoutCollection resource
        With this method, the workouts can be posted.
        If trying to post not valid workout, BadRequest is raised.
        If workout name is already in use, Conflict is raised.
        """

        # validation
        try:
            validate(request.json, Workout.json_schema())
        except ValidationError as error:
            raise BadRequest(description=str(error)) from error

        # create a new workout
        workout = Workout()
        workout.deserialize(request.json)
        workout.user_id = user.id

        try:
            db.session.add(workout)
            db.session.commit()
        except IntegrityError as error:
            raise Conflict(description="Workout name already in use") from error
        return "Success", 201

class WorkoutItem(Resource):
    """
    Class for the WorkoutItem resource.
    WorkoutItem is a single workout in the user collection.
    GET, PUT, POST and DELETE methods are implemented.
    """

    def get(self, user, workout):
        """
        Get method for WorkoutItem resource.
        Workout is fetched with this.
        """

        return workout.serialize()

    def put(self, user, workout):
        """
        Put method for WorkoutItem resource
        Workout is edited with this.
        If trying to edit it incorrectly, BadRequest is raised.
        """

        # validation
        try:
            validate(request.json, Workout.json_schema())
        except ValidationError as error:
            raise BadRequest(description=str(error)) from error

        # modify existing user information
        workout.deserialize(request.json)

        try:
            db.session.commit()
        except Exception as error:
            raise BadRequest(description=str(error)) from error
        return "Workout modified successfully", 201

    def post(self, user, workout):
        """
        Post method for WorkoutItem resource.
        Workout is posted with this.
        If the workout being posted does not follow the schema,
        BadRequest is raised. If the Workout name is already in use,
        Conflict is raised.
        """

        # validation
        try:
            validate(request.json, Movement.json_schema())
        except ValidationError as error:
            raise BadRequest(description=str(error)) from error

        # create a new movement
        movement = Movement()
        movement.workout_id = workout.id
        movement.sets = request.json["sets"]
        movement.reps = request.json["reps"]
        movement.movement_name = request.json["movement_name"]

        # movement name has to be unique within the workout, else raise error
        movements_in_workout = Movement.query.filter_by(workout_id=workout.id).all()
        for item in movements_in_workout:
            if item.movement_name == request.json["movement_name"]:
                raise Conflict(description="Movement name already in use")

        db.session.add(movement)
        db.session.commit()
        return "Success", 201

    def delete(self, user, workout):
        """
        Delete method for WorkoutItem resource
        Workout is deleted with this.
        """

        workout = Workout.query.filter_by(workout_name=workout.workout_name).first()
        db.session.delete(workout)
        db.session.commit()
        return "Success", 201
