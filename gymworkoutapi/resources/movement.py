"""
REFERENCE: https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/
"""
from flask_restful import Resource
from werkzeug.exceptions import NotFound, BadRequest
from gymworkoutapi import db
from gymworkoutapi.models import Movement

class MovementItem(Resource):
    """
    Class for the MovementItem resource
    MovementItem is a single movement in the workout
    which has GET and DELETE methods.
    """

    def get(self, user, workout, movement):
        """
        Get method for MovementItem resource
        With this method, the movements can be fetched.
        If the movement does not exist, NotFound is raised.
        """
        movement = Movement.query.filter_by(movement_name=movement, workout_id=workout.id).first()
        if not movement:
            raise NotFound(description="The movement not found")
        return movement.serialize()

    def delete(self, user, workout, movement):
        """
        Delete method for MovementItem resource
        With this method, the movements can be deleted.
        If the movement does not exist, BadRequest is raised.
        """
        movement = Movement.query.filter_by(movement_name=movement, workout_id=workout.id).first()

        try:
            db.session.delete(movement)
            db.session.commit()
        except Exception as error:
            raise BadRequest(description=str(error)) from error

        return "Success", 201
