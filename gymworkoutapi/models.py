"""
REFERENCE: https://github.com/enkwolf/pwp-course-sensorhub-api-example/blob/master/sensorhub/models.py
"""
from gymworkoutapi import db
import click
from flask.cli import with_appcontext

class User(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), nullable = False, unique=True)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=True)
    mean_bmi = db.Column(db.Float, nullable=True)
    
    workout = db.relationship('Workout', cascade="all,delete", back_populates='user')
    
    def serialize(self):
        return {
            "username": self.username,
            "height": self.height,
            "weight": self.weight,
            "bmi": self.bmi,
            "mean_bmi": self.mean_bmi
        }
    
    def deserialize(self, doc):
        self.username = doc.get("username")
        self.height = doc.get("height")
        self.weight = doc.get("weight")

        #calculate bmi for the user
        self.bmi = self.weight/((self.height/100)**2)

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["username", "height", "weight"]
        }
        props = schema["properties"] = {}
        props["username"] = {
            "description": "User's username",
            "type": "string"
        }
        props["height"] = {
            "description": "Height of the user",
            "type": "number"
        }
        props["weight"] = {
            "description": "Weight of the user",
            "type": "number"
        }
        return schema
    
class Workout(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    workout_name = db.Column(db.String(64), unique=True, nullable=False)
    favorite = db.Column(db.Boolean, nullable=False)

    movement = db.relationship('Movement', cascade="all,delete", back_populates='workout')
    user = db.relationship('User', back_populates='workout')
    
    def serialize(self):
        return {
            "user_id": self.user_id,
            "workout_name": self.workout_name,
            "favorite": self.favorite
        }
    
    def deserialize(self, doc):
        self.workout_name = doc.get("workout_name")
        self.favorite = doc.get("favorite")

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["workout_name", "favorite"]
        }
        props = schema["properties"] = {}
        props["workout_name"] = {
            "description": "Name of the workout",
            "type": "string"
        }
        props["favorite"] = {
            "description": "Workout is either user's favorite or not",
            "type": "boolean"
        }
        return schema
    
class Movement(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable = False)
    movement_name = db.Column(db.String(64), nullable=False)
    sets = db.Column(db.Float, nullable=False)
    reps = db.Column(db.Float, nullable=False)

    workout = db.relationship('Workout', back_populates='movement')
    
    def serialize(self):
        return {
            "workout_id": self.workout_id,
            "movement_name": self.movement_name,
            "sets": self.sets,
            "reps": self.reps
        }
    
    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["movement_name", "sets", "reps"]
        }
        props = schema["properties"] = {}
        props["movement_name"] = {
            "description": "Name of the movement",
            "type": "string"
        }
        props["sets"] = {
            "description": "The number of sets",
            "type": "integer"
        }
        props["reps"] = {
            "description": "The number of repetitions",
            "type": "integer"
        }
        return schema



@click.command("init_db")
@with_appcontext
def init_db_command():

    import os
    file_path = "instance/development.db"
    if os.path.isfile(file_path):
      os.remove(file_path)
      print("Previous database file has been deleted, new created successfully")
    else:
      print("Previous database file does not exist, new created successfully")
    db.create_all()


@click.command("test_db")
@with_appcontext
def db_test():

    # Create test data
    u1 = User(
        username="test_user1",
        height=175,
        weight=80
    )
    u2 = User(
        username="test_user2",
        height=169,
        weight=69
    )  
    w1 = Workout(
        user_id = 1,
        workout_name="test-workout1",
        favorite=True
    )
    w2 = Workout(
        user_id = 1,
        workout_name="test-workout2",
        favorite=False
    )
    w3 = Workout(
        user_id = 1,
        workout_name="test-workout3",
        favorite=False
    )
    m1 = Movement(
        movement_name="test-movement1",
        workout_id=1,
        sets=4,
        reps=6
    )
    m2 = Movement(
        movement_name="test-movement2",
        workout_id=2,
        sets=2,
        reps=12
    )
    m3 = Movement(
        movement_name="test-movement3",
        workout_id=2,
        sets=10,
        reps=3
    )
    
    db.session.add(u1)
    db.session.add(u2)
    db.session.add(w1)
    db.session.add(w2)
    db.session.add(w3)
    db.session.add(m1)
    db.session.add(m2)   
    db.session.add(m3)
    db.session.commit()
   
    # Check that everything exists
    assert Workout.query.count() == 3
    assert User.query.count() == 2
    assert Movement.query.count() == 3
   
    # Check that auto-incrementing is functioning correctly
    assert User.query.filter_by(username="test_user1").first().id == 1 # id = 1
    assert User.query.filter_by(username="test_user2").first().id == 2 # id = 2
    assert Workout.query.filter_by(workout_name="test-workout1").first().id == 1 # id = 1
    assert Workout.query.filter_by(workout_name="test-workout2").first().id == 2 # id = 2
    assert Movement.query.filter_by(movement_name="test-movement1").first().id == 1 # id = 1
    assert Movement.query.filter_by(movement_name="test-movement2").first().id == 2 # id = 2
     
    # Check relationships
    db_user = User.query.first()
    db_movement = Movement.query.first()
    db_workout = Workout.query.first()
    assert db_workout.user == db_user
    assert db_movement.workout == db_workout
    assert db_movement in db_workout.movement
    assert db_workout in db_user.workout

    # Check that ONDELETE updates/deletes the pointed value correctly
    assert Workout.query.filter_by(workout_name="test-workout1").first().id == 1 # 1 before deleting Movement 1
    db.session.delete(m2)
    db.session.commit()
    assert Workout.query.filter_by(workout_name="test-workout1").first().id == 1 # 1, Workout should not be deleted after deleting movement
    
    assert Movement.query.filter_by(movement_name="test-movement1").first() != None # Movement should exist before deletion of workout
    db.session.delete(w1)
    db.session.commit()
    assert Movement.query.filter_by(movement_name="test-movement1").first() == None # Movement associated with workout should be None after deletion
    
    assert User.query.filter_by(username="test_user1").first().id == 1 # 1 before deleting user's workout
    db.session.delete(w2)
    db.session.commit()
    assert User.query.filter_by(username="test_user1").first().id == 1 # 1 user should not be deleted after deleting workout of the user
   
    assert Workout.query.filter_by(workout_name="test-workout3").first() != None # Workout should exist before deletion of the user
    db.session.delete(u1)
    db.session.commit()
    assert Workout.query.filter_by(workout_name="test-workout3").first() == None # Workout should be None after deletion of the user
    
    db.session.delete(u2)
    db.session.commit()
    
    # All movements, All workouts, and all workouts should be deleted in the previous section, check that model counts have been updated correctly
    assert Workout.query.count() == 0
    assert User.query.count() == 0
    assert Movement.query.count() == 0 
    
    db.session.close()
