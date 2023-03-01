from flask_restful import Resource
from werkzeug.exceptions import NotFound, BadRequest
from gymworkoutapi import db
from gymworkoutapi.models import Movement

class MovementItem(Resource):
    def get(self, user, workout, movement):
        movement = Movement.query.filter_by(movement_name=movement, workout_id=workout.id).first()
        if not movement:
            raise NotFound(description="The movement not found")
        return movement.serialize()
    
    def delete(self, user, workout, movement):
        
        movement = Movement.query.filter_by(movement_name=movement, workout_id=workout.id).first()
        if not movement:
            raise NotFound(description="The movement not found")

        try:
            db.session.delete(movement)
            db.session.commit()
        except Exception as e:
            raise BadRequest(description=str(e))
        
        return "Success", 201
