"""
REFERENCE:
https://github.com/enkwolf/pwp-course-sensorhub-api-example/blob/master/sensorhub/__init__.py
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger, swag_from

db = SQLAlchemy()

def create_app(test_config=None):
    """
    Function used to create the application
    """

    app = Flask(__name__, instance_relative_config=True, static_folder="static")
    app.config.from_mapping(
            SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, "dev.db"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False
        )
    app.config["SWAGGER"] = {
        "title": "Gym Workout API",
        "openapi": "3.0.3",
        "uiversion": 3,
    }
    swagger = Swagger(app, template_file="doc/documentation.yml")

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    from gymworkoutapi.utils import UserConverter, WorkoutConverter
    from . import models
    from . import api
    app.url_map.converters["user"] = UserConverter
    app.url_map.converters["workout"] = WorkoutConverter
    app.cli.add_command(models.init_db_command)
    app.cli.add_command(models.db_test)
    app.register_blueprint(api.api_bp)

    return app
