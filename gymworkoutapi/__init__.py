"""
REFERENCE: https://github.com/enkwolf/pwp-course-sensorhub-api-example/blob/master/sensorhub/__init__.py
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.engine import Engine
from sqlalchemy import event

db = SQLAlchemy()

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    from . import models
    from . import api
    from gymworkoutapi.utils import UserConverter, WorkoutConverter
    app.url_map.converters["user"] = UserConverter
    app.url_map.converters["workout"] = WorkoutConverter
    app.cli.add_command(models.init_db_command)
    app.cli.add_command(models.db_test)
    app.register_blueprint(api.api_bp)

    
    return app
