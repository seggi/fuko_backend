import os
from re import DEBUG
from flask.cli import FlaskGroup
from flask_migrate import Migrate
from api import create_app, db
from api.database.models import *

app = create_app(os.getenv('FLASK_ENV') or 'production')

if __name__ == '__main__':
    app.run()