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
    """
    Class for the UserCollection resource.
    UserCollection is a collection of users.
    GET and POST methods are implemented.
    """

    def get(self):
        """
        Get method for UserCollection resource.
        UserCollection is fetched with this.
        """
        users = User.query.all()
        response_data = []
        while users:
            user = users.pop()
            response_data.append(user.serialize())
        return Response(json.dumps(response_data), 200)

    def post(self):
        """
        Post method for UserCollection resource
        Users is posted with this. If trying to post
        User that does not follow the schema, BadRequest is raised.
        If username is already in use, Conflict is raised.
        """

        # validation
        try:
            validate(request.json, User.json_schema())
        except ValidationError as error:
            raise BadRequest(description=str(error)) from error

        # create a new user
        user = User()
        user.deserialize(request.json)

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as error:
            raise Conflict(description="Username already in use") from error
        return "Success", 201


class UserItem(Resource):
    """
    Class for the UserItem resource
    UserItem is an individual user.
    GET, PUT and DELETE methods are implemented.
    """
    def get(self, user):
        """
        Get method for UserItem resource.
        User gets fetched with this method.
        """

        return user.serialize()

    def put(self, user):
        """
        Put method for UserItem resource.
        User is edited with this.
        If the schema is not followed, BadRequest is raised.
        """

        # validation
        try:
            validate(request.json, User.json_schema())
        except ValidationError as error:
            raise BadRequest(description=str(error)) from error

        # modify existing user information
        user.deserialize(request.json)

        try:
            db.session.commit()
        except Exception as error:
            raise BadRequest(description=str(error)) from error
        return "User modified successfully", 201

    def delete(self, user):
        """
        Delete method for UserItem resource
        User is deleted with this. 
        """

        user = User.query.filter_by(username=user.username).first()
        db.session.delete(user)
        db.session.commit()
        return "Success", 201
