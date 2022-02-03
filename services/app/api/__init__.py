import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail
from flask_jwt_extended import JWTManager

import api.utils.responses as resp
from config import config
from api.utils.responses import response_with


db = SQLAlchemy()
marsh = Marshmallow()
jwt = JWTManager()
mail = Mail()

# Create app according to environment
def create_app(config_name) -> any:
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Global HTTP configurations
    @app.after_request
    def add_header(response):
        return response

    @app.errorhandler(400)
    def bad_request(e):
        logging.error(e)
        return response_with(resp.BAD_REQUEST_400)
    
    @app.errorhandler(500)
    def server_error(e):
        logging.error(e)
        return response_with(resp.SERVER_ERROR_500)

    @app.errorhandler(404)
    def not_found(e):
        logging.error(e)
        return response_with(resp.SERVER_ERROR_404)

    # Register App to packages
    db.init_app(app)
    marsh.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)

    # Import views
    from . auth import auth_view as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/api/user")

    return app