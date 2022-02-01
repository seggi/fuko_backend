import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail
from flask_jwt_extended import JWTManager


from config import config

# Global variables
DB = SQLAlchemy()
MARSH = Marshmallow()
JWT = JWTManager()
MAIL = Mail()

# Setup enviroment for the app
def create_app(config_name) -> any:
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    #  Register the App to packages 
    DB.init_app(app)
    MARSH.init_app(app)
    MAIL.init_app(app)
    JWT.init_app(app)

    # Colling views

    return app