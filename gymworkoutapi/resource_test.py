"""
REFERENCE: https://github.com/enkwolf/pwp-course-sensorhub-api-example/blob/master/tests/resource_test.py
           AND
           https://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/testing-flask-applications-part-2/
"""
import os
import json
import pytest
import tempfile
import random
from sqlalchemy.engine import Engine
from sqlalchemy import event

from . import create_app, db
from gymworkoutapi.models import User, Workout, Movement

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

@pytest.fixture
def client():
    db_fd, db_fname = tempfile.mkstemp()

    config = {
        "SQLALCHEMY_DATABASE_URI": "sqlite:///" + db_fname,
        "TESTING": True
    }

    app = create_app(config)

    with app.app_context():
        db.create_all()
        _populate_db()

    yield app.test_client()

    os.close(db_fd)
    #os.unlink(db_fname)


def _populate_db():
    
    workout_ids = [6, 5, 4, 3, 2, 1]
    movement_ids = [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    # 3 test users, 2 workouts for each user, 2 movements in each workout
    for i in range(1, 4):
        user = User(
            username="test_user{}".format(i),
            height= random.uniform(150.0, 200.0),
            weight= random.uniform(50.0, 120.0)
        )
        db.session.add(user)
        for j in range(1, 3):
            workout = Workout(
                user_id= i,
                workout_name="test_workout{}".format(workout_ids.pop()),
                favorite= random.choice([True, False])
            )
            db.session.add(workout)
            for z in range(1, 3):
                movement = Movement(
                    workout_id=j,
                    movement_name="test_movement{}".format(movement_ids.pop()),
                    sets= random.randrange(3, 5),
                    reps= random.randrange(5, 12)
                )
                db.session.add(movement)
    
    db.session.commit()


class TestUserCollection(object):
    """
    This class implements tests for each HTTP method in UserCollection resource. 
    """
    RESOURCE_URL = "/api/users/"

    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body) == 3
        for item in body:
            assert "username" in item
            assert "height" in item
            assert "weight" in item

    def test_post(self, client):
        pass



class TestUserItem(object):
    """
    This class implements tests for each HTTP method in TestUserItem resource. 
    """
    def test_get(self, client):
        pass
    
    def test_put(self, client):
        pass
        
    def delete(self, client):
        pass
        
class TestWorkoutCollection(object):
    """
    This class implements tests for each HTTP method in WorkoutCollection resource. 
    """
    def test_get(self, client):
        pass
    
    def test_post(self, client):
        pass
        
class TestWorkoutItem(object):
    """
    This class implements tests for each HTTP method in TestWorkoutItem resource. 
    """
    def test_get(self, client):
        pass
    
    def test_put(self, client):
        pass
    
    def test_post(self, client):
        pass
        
    def test_delete(self, client):
        pass
        
class TestMovementItem(object):
    """
    This class implements tests for each HTTP method in TestMovementItem resource. 
    """
    def test_get(self, client):
        pass
    
    def test_delete(self, client):
        pass
        