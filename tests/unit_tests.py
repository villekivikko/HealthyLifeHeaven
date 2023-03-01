import json
import os
import pytest
import random
import tempfile
import time
import app
from datetime import datetime
from jsonschema import validate
from sqlalchemy.engine import Engine
from sqlalchemy import event
from sqlalchemy.exc import IntegrityError, StatementError

from app import app, db
from app import User, Workout, Movement

@pytest.fixture
def client():
    db_fd, db_fname = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
    app.config["TESTING"] = True

    db.create_all()
    #_populate_db() # Is this needed?

    yield app.test_client()

    db.session.remove()
    os.close(db_fd)
    os.unlink(db_fname)

# TODO: Is population of databases needed? Add here
"""
def _populate_db(): # In case Population of databases is needed(?)
    
"""

class TestUserCollection(object):
    """
    This class implements tests for each HTTP method in UserCollection resource. 
    """
    def test_get(self, client):
        pass
    
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