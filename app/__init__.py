# third party import
from flask import Flask, abort, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from jsonschema import ValidationError

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    db.init_app(app)
    migrate = Migrate(app, db)

    from app import models

    from .user.views import user as user_blueprint
    app.register_blueprint(user_blueprint)

    @app.errorhandler(400)
    def bad_request(error):
        original_error = error.description
        if isinstance(original_error, ValidationError):
            # custom handling
            return make_response(jsonify({"status": "failed", 'message': original_error.message}), 400)
        return error

    @app.errorhandler(404)
    def bad_request(error):
        return make_response(jsonify({"status": "failed", 'message': error.description}), 404)

    return app
