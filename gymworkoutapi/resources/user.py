import json
from flask import request, Response
from flask_restful import Resource
from jsonschema import validate, ValidationError
from werkzeug.exceptions import NotFound, BadRequest, Conflict, UnsupportedMediaType
from sqlalchemy.exc import IntegrityError
from gymworkoutapi import db
from gymworkoutapi.models import User

class UserCollection(Resource):
    def get(self):
        users = User.query.all() 
        response_data = []
        while users:
            user = users.pop()
            response_data.append(user.serialize())
        return Response(json.dumps(response_data), 200)

    def post(self):
    
        # validation
        try:
            validate(request.json, User.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))

        # create a new user
        user = User()
        user.deserialize(request.json)

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            raise Conflict(description="Username already in use")
        return "Success", 201


class UserItem(Resource):
    def get(self, user):
        return user.serialize()

    def put(self, user):

        # validation
        try:
            validate(request.json, User.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        
        # modify existing user information
        user.deserialize(request.json)
        
        try:
            db.session.commit()
        except Exception as e:
            raise BadRequest(description=str(e))
        
        return "Success", 201

    def delete(self, user):
        user = User.query.filter_by(username=user.username).first()
        db.session.delete(user)
        db.session.commit()
        return "Success", 201
