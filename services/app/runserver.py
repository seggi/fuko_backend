import os
from re import DEBUG
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_migrate import Migrate
from api import create_app, db
from api.database.models import *

app = create_app(os.getenv('FLASK_ENV') or 'production')

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()