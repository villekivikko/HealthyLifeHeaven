"""
REFERENCE: https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/
"""

import json
from flask import request, Response
from flask_restful import Resource
from jsonschema import validate, ValidationError, draft7_format_checker
from werkzeug.exceptions import NotFound, BadRequest, Conflict, UnsupportedMediaType, InternalServerError
from sqlalchemy.exc import IntegrityError
from gymworkoutapi import db
from gymworkoutapi.models import Workout, Movement

class WorkoutCollection(Resource):
    def get(self, user):
        workouts = Workout.query.filter_by(user_id=user.id).all() 
        response_data = []
        while workouts:
            workout = workouts.pop()
            response_data.append(workout.serialize())
        return Response(json.dumps(response_data), 200)

    def post(self, user):
        if not request.json:
            raise UnsupportedMediaType(description="Wrong media type, use JSON")
        
        # validation
        try:
            validate(request.json, Workout.json_schema(), format_checker=draft7_format_checker)
        except ValidationError as e:
            raise BadRequest(description=str(e))
        
        # create a new workout
        workout = Workout()
        workout.deserialize(request.json)
        workout.user_id = user.id

        try:
            db.session.add(workout)
            db.session.commit()
        except IntegrityError:
            raise Conflict(description="Workout name already in use")
        return "Success", 201 

class WorkoutItem(Resource):
    def get(self, user, workout):
        return workout.serialize()
    
    def put(self, user, workout):
        if not workout:
            raise NotFound(description="The workout not found")
        if not request.json:
            raise UnsupportedMediaType(description="Wrong media type, use JSON")
        
        # validation
        try:
            validate(request.json, Workout.json_schema(), format_checker=draft7_format_checker)
        except ValidationError as e:
            raise BadRequest(description=str(e))
        
        # modify existing user information
        workout.deserialize(request.json)

        try:
            db.session.commit()
        except Exception as e:
            raise BadRequest(description=str(e))
        return "Success", 201 

    def post(self, user, workout):
        if not request.json:
            raise UnsupportedMediaType(description="Wrong media type, use JSON")
    
        # validation
        try:
            validate(request.json, Movement.json_schema(), format_checker=draft7_format_checker)
        except ValidationError as e:
            raise BadRequest(description=str(e))

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

        try:
            db.session.add(movement)
            db.session.commit()
        except Exception as e:
            raise BadRequest(description=str(e))
        
        return "Success", 201

    def delete(self, user, workout):
        workout = Workout.query.filter_by(workout_name=workout.workout_name).first()
        if not workout:
            raise NotFound(description="The workout not found")

        try:
            db.session.delete(workout)
            db.session.commit()
        except Exception as e:
            raise BadRequest(description=str(e))
        
        return "Success", 201
