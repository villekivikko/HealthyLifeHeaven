
"""
REFERENCE:
https://github.com/enkwolf/pwp-course-sensorhub-api-example/blob/master/sensorhub/models.py
https://coverage.readthedocs.io/en/6.4.4/excluding.html
"""

import click
from flask.cli import with_appcontext
from gymworkoutapi import db

class User(db.Model):
    """
    Class for the user model
    """

    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), nullable = False, unique=True)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=True)
    mean_bmi = db.Column(db.Float, nullable=True)

    workout = db.relationship('Workout', cascade="all,delete", back_populates='user')

    def serialize(self):
        """
        Serializer for the User class
        """

        return {
            "username": self.username,
            "height": self.height,
            "weight": self.weight,
            "bmi": self.bmi,
            "mean_bmi": self.mean_bmi
        }

    def deserialize(self, doc):
        """
        Deserializer for the User class
        """

        self.username = doc.get("username")
        self.height = doc.get("height")
        self.weight = doc.get("weight")

        #calculate bmi for the user
        self.bmi = self.weight/((self.height/100)**2)

    @staticmethod
    def json_schema():
        """
        Defines a valid user document
        """

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
    """
    Class for the workout model
    """

    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = "CASCADE"), nullable = False)
    workout_name = db.Column(db.String(64), unique=True, nullable=False)
    favorite = db.Column(db.Boolean, nullable=False)

    movement = db.relationship('Movement', cascade="all,delete", back_populates='workout')
    user = db.relationship('User', back_populates='workout')

    def serialize(self):
        """
        Serializer for the Workout class
        """

        return {
            "user_id": self.user_id,
            "workout_name": self.workout_name,
            "favorite": self.favorite
        }

    def deserialize(self, doc):
        """
        Deserializer for the Workout class
        """

        self.workout_name = doc.get("workout_name")
        self.favorite = doc.get("favorite")

    @staticmethod
    def json_schema():
        """
        Defines a valid workout document
        """

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
    """
    Class for the movement model
    """

    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id', ondelete = "CASCADE"), nullable = False)
    movement_name = db.Column(db.String(64), nullable=False)
    sets = db.Column(db.Float, nullable=False)
    reps = db.Column(db.Float, nullable=False)

    workout = db.relationship('Workout', back_populates='movement')

    def serialize(self):
        """
        Serializer for the Movement class
        """

        return {
            "workout_id": self.workout_id,
            "movement_name": self.movement_name,
            "sets": self.sets,
            "reps": self.reps
        }

    @staticmethod
    def json_schema():
        """
        Defines a valid movement document
        """

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
def init_db_command(): # pragma: no cover
    """
    Initializes database
    """

    import os
    file_path = "instance/dev.db"
    if os.path.isfile(file_path):
        os.remove(file_path)
        print("Previous database file has been deleted, new created successfully")
    else:
        print("Previous database file does not exist, new created successfully")
    db.create_all()


@click.command("test_db")
@with_appcontext
def db_test(): # pragma: no cover
    """
    Database testing
    """

    # Create test data
    u_1 = User(
        username="test_user1",
        height=175,
        weight=80
    )
    u_2 = User(
        username="test_user2",
        height=169,
        weight=69
    )
    w_1 = Workout(
        user_id = 1,
        workout_name="test-workout1",
        favorite=True
    )
    w_2 = Workout(
        user_id = 1,
        workout_name="test-workout2",
        favorite=False
    )
    w_3 = Workout(
        user_id = 1,
        workout_name="test-workout3",
        favorite=False
    )
    m_1 = Movement(
        movement_name="test-movement1",
        workout_id=1,
        sets=4,
        reps=6
    )
    m_2 = Movement(
        movement_name="test-movement2",
        workout_id=2,
        sets=2,
        reps=12
    )
    m_3 = Movement(
        movement_name="test-movement3",
        workout_id=2,
        sets=10,
        reps=3
    )

    db.session.add(u_1)
    db.session.add(u_2)
    db.session.add(w_1)
    db.session.add(w_2)
    db.session.add(w_3)
    db.session.add(m_1)
    db.session.add(m_2)
    db.session.add(m_3)
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

    ############################################################################
    # Check that ONDELETE updates/deletes the pointed value correctly
    ############################################################################

    # 1 before deleting Movement 1
    assert Workout.query.filter_by(workout_name="test-workout1").first().id == 1

    db.session.delete(m_2)
    db.session.commit()

    # 1, Workout should not be deleted after deleting movement
    assert Workout.query.filter_by(workout_name="test-workout1").first().id == 1

    # Movement should exist before deletion of workout
    assert Movement.query.filter_by(movement_name="test-movement1").first() is not None

    db.session.delete(w_1)
    db.session.commit()

    # Movement associated with workout should be None after deletion
    assert Movement.query.filter_by(movement_name="test-movement1").first() is None

    # 1 before deleting user's workout
    assert User.query.filter_by(username="test_user1").first().id == 1

    db.session.delete(w_2)
    db.session.commit()

    # 1 user should not be deleted after deleting workout of the user
    assert User.query.filter_by(username="test_user1").first().id == 1

    # Workout should exist before deletion of the user
    assert Workout.query.filter_by(workout_name="test-workout3").first() is not None

    db.session.delete(u_1)
    db.session.commit()

    # Workout should be None after deletion of the user
    assert Workout.query.filter_by(workout_name="test-workout3").first() is None

    db.session.delete(u_2)
    db.session.commit()

    # All movements, All workouts, and all workouts should be deleted in the previous section,
    # check that model counts have been updated correctly
    assert Workout.query.count() == 0
    assert User.query.count() == 0
    assert Movement.query.count() == 0

    db.session.close()
