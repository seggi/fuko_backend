from locale import currency
import os
from re import DEBUG
from flask.cli import FlaskGroup
from flask_migrate import Migrate
from api import create_app, db
from api.database.models import *

from api.core.convert_json_file import convert_currencies_json_file as currencies

app = create_app(os.getenv('FLASK_ENV') or 'production')

cli = FlaskGroup(app)
migrate = Migrate(app, db)

@cli.command("create_db")
def create_db():
    db.create_all()
    db.session.commit()

@cli.command("drop_db")
def drop_db():
    db.drop_all()
    db.session.commit()

@cli.command('seed_db')
def seed_db():
    request_status = ["sent", "accepted", "rejected", "expired"]
    
    for status in request_status:
        db.session.add(RequestStatus(name=status))
        db.session.commit()

    for code, desc in currencies().items():
        db.session.add(Currency(code=code, description=desc))
        db.session.commit()
    


if __name__ == "__main__":
    cli()
