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

def _get_user_json(number=1):
    """
    Creates a valid user JSON object to be used for PUT and POST tests.
    """
    return {"username": "extra_user{}".format(number), 
        "height": 150.0, "weight": 50.0}

def _get_workout_json(number=1):
    """
    Creates a valid workout JSON object to be used for PUT and POST tests.
    """
    return {"user_id":1,"workout_name": "extra_workout{}".format(number),
        "favorite":True}

def _get_movement_json(number=1):
    """
    Creates a valid movement JSON object to be used for PUT and POST tests.
    """
    return {"workout_id":1,"movement_name": "extra_movement{}".format(number), 
        "sets": 3, "reps": 5}


class TestUserCollection(object):
    """
    This class implements tests for each HTTP method in UserCollection resource. 
    """
    RESOURCE_URL = "/api/users/"

    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body[0]) == 5
        for item in body:
            assert "username" in item
            assert "height" in item
            assert "weight" in item

    def test_post(self, client):
        """
        Tests POST method by checking the following:
        error codes, valid request receives a 201 response
        """
        valid = _get_user_json()

        #test with wrong content type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 400

        #test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201
        location = "/api/users/" + valid["username"] + "/"
        resp = client.get(location)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["username"] == "extra_user1"
        assert body["height"] == 150.0
        assert body["weight"] == 50.0

        #send same data again for 409
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409

        #remove height field for 400
        valid.pop("weight")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400


class TestUserItem(object):
    """
    This class implements tests for each HTTP method in TestUserItem resource. 
    """
    RESOURCE_URL = "/api/users/test_user1/"
    INVALID_URL = "/api/users/non_user1/"
    MODIFIED_URL = "/api/users/extra_user1/"

    def test_get(self, client):
        """
        Tests the GET method. Checks the following:
        response status code is 200, expected attributes are present,
        all of the items in DB population are present.
        """
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["username"] == "test_user1"
        #assert body["height"] == float
        #assert body["weight"] == float
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404
    
    def test_put(self, client):
        """
        Tests the PUT method. Checks the following:
        error codes, valid request receives a 201 response,
        when name is changed the user can't be found from its new URI
        """
        valid = _get_user_json()

        #test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 400
        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404
        
        #test with another user's name
        valid["username"] = "test_user2"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

        #test with valid (change user)
        valid["username"] = "test_user1"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201

        #remove field for 400
        valid.pop("height")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

        valid = _get_user_json()
        resp = client.put(self.RESOURCE_URL, json=valid)
        resp = client.get(self.MODIFIED_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["height"] == valid["height"]
        
    def test_delete(self, client):
        """
        Tests the DELETE method. Checks the following:
        valid request receives 201 response and trying to GET
        the user afterwards results in 404 and trying to delete a user
        that doesn't exist results in 404.
        """
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 201
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404
        
class TestWorkoutCollection(object):
    """
    This class implements tests for each HTTP method in WorkoutCollection resource. 
    """
    RESOURCE_URL = "/api/users/test_user1/workouts/"

    def test_get(self, client):
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert len(body[0]) == 3
        for item in body:
            assert "workout_name" in item
            assert "favorite" in item
            assert "user_id" in item

    def test_post(self, client):
        """
        Tests POST method by checking the following:
        error codes, valid request receives a 201 response
        """
        valid = _get_workout_json()

        #test with wrong content type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 400

        #test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201
        location = self.RESOURCE_URL + 'extra_workout1' + '/'
        resp = client.get(location)
        body = json.loads(resp.data)
        assert body["workout_name"] == "extra_workout1"
        assert body["favorite"] == True

        #send same data again for 409
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409

        #remove favorite field for 400
        valid.pop("favorite")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400
        
class TestWorkoutItem(object):
    """
    This class implements tests for each HTTP method in TestWorkoutItem resource. 
    """
    RESOURCE_URL = "/api/users/test_user1/workouts/test_workout1/"
    INVALID_URL = "/api/users/test_user1/workouts/non_workout1/"
    MODIFIED_URL = "/api/users/test_user1/workouts/extra_workout1/"

    def test_get(self, client):
        """
        Tests the GET method. Checks the following:
        response status code is 200, expected attributes are present,
        all of the items in DB population are present.
        """
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["workout_name"] == "test_workout1"
        #assert body["favorite"] == True
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404
    
    def test_put(self, client):
        """
        Tests the PUT method. Checks the following:
        error codes, valid request receives a 201 response,
        when name is changed the sensor can't be found from its new URI
        """
        valid = _get_workout_json()

        #test with wrong content type
        resp = client.put(self.RESOURCE_URL, data=json.dumps(valid))
        assert resp.status_code == 400
        resp = client.put(self.INVALID_URL, json=valid)
        assert resp.status_code == 404
        
        #test with another workout's name
        valid["workout_name"] = "test_workout2"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

        #test with valid (change workout)
        valid["workout_name"] = "test_workout1"
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201

        #remove field for 400
        valid.pop("favorite")
        resp = client.put(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400

        valid = _get_workout_json()
        resp = client.put(self.RESOURCE_URL, json=valid)
        resp = client.get(self.MODIFIED_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["workout_name"] == valid["workout_name"]
        
    def test_delete(self, client):
        """
        Tests the DELETE method. Checks the following:
        valid request receives 201 response and trying to GET
        the user afterwards results in 404 and trying to delete a user
        that doesn't exist results in 404.
        """
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 201
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404
    
    def test_post(self, client):
        
        valid = _get_movement_json()
        
        #test with wrong content type
        resp = client.post(self.RESOURCE_URL, data=json.dumps(valid))
        print(resp)
        assert resp.status_code == 400

        #test with valid and see that it exists afterward
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 201
        location = self.RESOURCE_URL + 'extra_movement1' + '/'
        resp = client.get(location)
        body = json.loads(resp.data)
        assert body["movement_name"] == "extra_movement1"
        assert body["sets"] == 3
        assert body["reps"] == 5

        # send same data again for 409
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 409
        
        # remove field for 400
        valid.pop("sets")
        resp = client.post(self.RESOURCE_URL, json=valid)
        assert resp.status_code == 400
        
        
class TestMovementItem(object):
    """
    This class implements tests for each HTTP method in TestMovementItem resource. 
    """
    RESOURCE_URL = "/api/users/test_user1/workouts/test_workout1/test_movement1/"
    INVALID_URL = "/api/users/test_user1/workouts/test_workout1/non_movement1/"
    MODIFIED_URL = "/api/users/test_user1/workouts/test_workout1/extra_movement1/"

    def test_get(self, client):
        """
        Tests the GET method. Checks the following:
        response status code is 200, expected attributes are present,
        all of the items in DB population are present.
        """
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 200
        body = json.loads(resp.data)
        assert body["movement_name"] == "test_movement1"
        #assert body["sets"]
        #assert body["reps"]
        resp = client.get(self.INVALID_URL)
        assert resp.status_code == 404
    
    def test_delete(self, client):
        """
        Tests the DELETE method. Checks the following:
        valid request receives 201 response and trying to GET
        the user afterwards results in 404 and trying to delete a user
        that doesn't exist results in 404.
        """
        resp = client.delete(self.RESOURCE_URL)
        assert resp.status_code == 201
        resp = client.get(self.RESOURCE_URL)
        assert resp.status_code == 404
        resp = client.delete(self.INVALID_URL)
        assert resp.status_code == 404
        