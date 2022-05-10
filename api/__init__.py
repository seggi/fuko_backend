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
    from .auth.auth_views  import auth as auth_blueprint
    from .auth.profile_views import profile_view as profile_blueprint
    from . accountability.global_amount.global_amount_views import global_account as account_blueprint
    from .accountability.expenses.expenses_views import expenses as expenses_blueprint
    from .accountability.savings.savings_views import savings as savings_blueprint
    from .accountability.budget.budget_views import budget as budget_blueprint
    from .accountability.loans.loan_views import loans as loans_blueprint
    from .accountability.dept.dept_views import dept as dept_blueprint
    from .documentation.index import document as document_blueprint
    from .other.create_notebook import notebook as notebook_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(profile_blueprint)
    app.register_blueprint(account_blueprint)
    app.register_blueprint(expenses_blueprint)
    app.register_blueprint(savings_blueprint)
    app.register_blueprint(budget_blueprint)
    app.register_blueprint(loans_blueprint)
    app.register_blueprint(dept_blueprint)
    app.register_blueprint(notebook_blueprint)

    app.register_blueprint(document_blueprint)

    return app
