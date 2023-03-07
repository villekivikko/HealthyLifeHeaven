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
        except ValidationError as error:
            raise BadRequest(description=str(error))

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
        except ValidationError as error:
            raise BadRequest(description=str(error))

        # modify existing user information
        user.deserialize(request.json)

        try:
            db.session.commit()
        except Exception as error:
            raise BadRequest(description=str(error))
        return "User modified successfully", 201

    def delete(self, user):
        user = User.query.filter_by(username=user.username).first()
        db.session.delete(user)
        db.session.commit()
        return "Success", 201
