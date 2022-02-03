# import os
# from re import DEBUG
# from flask.cli import FlaskGroup
# from flask_migrate import Migrate
# from api import create_app, db
# from api.database.models import *

# app = create_app(os.getenv('FLASK_ENV') or 'production')

# cli = FlaskGroup(app)
# migrate = Migrate(app, db)


# @cli.command("create_db")
# def create_db():
#     db.create_all()
#     db.session.commit()


# @cli.command("drop_db")
# def drop_db():
#     db.drop_all()
#     db.session.commit()


# @cli.command('seed_db')
# def seed_db():
#     db.session.add(Country(name="RDC"))
#     db.session.commit()


# if __name__ == "__main__":
#     cli()

from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello this is the new fuko!"

if __name__ == "__main__":
    app.run()