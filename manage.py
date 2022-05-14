from locale import currency
import os
from re import DEBUG
from flask.cli import FlaskGroup
from flask_migrate import Migrate
from api import create_app, db
from api.database.models import *

from api.core.json.convert_json_file import convert_currencies_json_file as currencies
from api.core.json.convert_json_file import convert_budget_file as budgets

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
    budget_options = ["Icommes", "Expenses"]
    rent_payment_option = ["Month", "Week", "Day", "Year"]
    
    for status in request_status:
        db.session.add(RequestStatus(request_status_name=status))
        db.session.commit()

    for period in  rent_payment_option:
        db.session.add(RentPaymentOption(name=period))
        db.session.commit()


    for budget in budget_options:
        db.session.add(BudgetOption(name=budget))
        db.session.commit()

    for code, desc in currencies().items():
        db.session.add(Currency(code=code, description=desc))
        db.session.commit()

    for code, desc in budgets().items():
        db.session.add(BudgetCategories(name=code, description=desc))
        db.session.commit()

if __name__ == "__main__":
    cli()
