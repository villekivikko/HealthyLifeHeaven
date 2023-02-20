from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event
import click
from flask.cli import with_appcontext

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

class User(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), nullable = False, unique=True)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=True)
    mean_bmi = db.Column(db.Float, nullable=True)
    
    workout = db.relationship('Workout', cascade="all,delete", back_populates='user')

class Workout(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = True)
    workout_name = db.Column(db.String(64), unique=True, nullable=False)
    favorite = db.Column(db.Boolean, nullable=False)

    movement = db.relationship('Movement', cascade="all,delete", back_populates='workout')
    user = db.relationship('User', back_populates='workout')

class Movement(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable = True)
    movement_name = db.Column(db.String(64), nullable=False)
    sets = db.Column(db.Float, nullable=False)
    reps = db.Column(db.Float, nullable=False)

    workout = db.relationship('Workout', back_populates='movement')
        

@click.command("init_db")
@with_appcontext
def init_db_command():

    import os
    file_path = "test.db"
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
    
    
    # All movements, All workouts, and User 1 should be deleted in the previous section, check that model counts have been updated correctly
    assert Workout.query.count() == 0
    assert User.query.count() == 1
    assert Movement.query.count() == 0


app.cli.add_command(init_db_command)
app.cli.add_command(db_test)