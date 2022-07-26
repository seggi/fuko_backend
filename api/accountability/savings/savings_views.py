from datetime import date
from api.core.constant import CURRENT_YEAR, MONTHS_LIST
from api.core.reducer import Reducer
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import extract, desc
from api.accountability.global_amount.global_amount_views import QUERY

from api.core.query import QueryGlobalReport
from api.utils.responses import response_with
from api.utils import responses as resp
from api.utils.model_marsh import CurrencySchema, SavingsSchema

from ... import db
from api.database.models import Currency, Savings, User
savings = Blueprint("savings", __name__,
                    url_prefix="/api/user/account/savings")

QUERY = QueryGlobalReport()

# Register saving data

todays_date = date.today()
savings_schema = SavingsSchema()
currency_schema = CurrencySchema()


@savings.post("/add-saving")
@jwt_required(refresh=True)
def user_add_saving():
    # Generate inputs
    try:
        user_id = get_jwt_identity()['id']
        data = request.json
        for value in data["data"]:
            QUERY.insert_data(db=db, table_data=Savings(
                **value | {"user_id": user_id}))
        return jsonify({
            "code": "success",
            "message": "Amount saved with success"
        })
    except Exception as e:
        return response_with(resp.INVALID_INPUT_422)


# Get all savings
@savings.get("/retrieve-by-current-date/<int:currency_id>")
@jwt_required(refresh=True)
def user_get_saving_by_date(currency_id):
    user_id = get_jwt_identity()['id']
    item_list: list = []
    total_amount_list = []
    currency_amount = []
    currency_code = []

    currency_data_code = db.session.query(Currency.code).\
        filter(Currency.id == currency_id).all()

    data = db.session.query(
        Savings.amount,
        Savings.description,
        Savings.created_at,
        Savings.money_provenance,
        Currency.code).\
        join(Currency, Savings.currency_id == Currency.id).\
        filter(Savings.currency_id == currency_id).\
        filter(Savings.user_id == user_id).\
        filter(extract('year', Savings.created_at) == todays_date.year).\
        filter(extract('month', Savings.created_at) ==
               todays_date.month).order_by(desc(Savings.created_at)).all()

    for item in data:
        item_list.append(savings_schema.dump(item))
        currency_amount.append(
            savings_schema.dump(item) | currency_schema.dump(item)
        )

    for code in currency_data_code:
        currency_code.append(currency_schema.dump(code))

    for item in item_list:
        total_amount_list.append(item['amount'])

    total_amount = sum(total_amount_list)

    return jsonify(data={
        "saving_list": currency_amount,
        "total_amount": {
            "currency": currency_code[0]["code"],
            "amount":  total_amount
        },
        "today_date": todays_date,
    })


@savings.get("/retrieve-saving-report/<int:currency_id>/<int:selected_years>")
@jwt_required(refresh=True)
def get_saving_report(currency_id, selected_years):
    user_id = get_jwt_identity()['id']
    item_list: list = []
    total_amount = []
    saving_list = []
    currency_code = []
    monthly_report = []
    total_amount_list = []

    convert_year = int(selected_years
                       ) if selected_years != "" else None

    selected_year = CURRENT_YEAR if convert_year == None else convert_year

    for month in MONTHS_LIST:
        data = db.session.query(
            Savings.amount,
            Savings.description,
            Savings.created_at,
            Savings.money_provenance,
            Currency.code).\
            join(Currency, Savings.currency_id == Currency.id).\
            filter(Savings.currency_id == currency_id).\
            filter(Savings.user_id == user_id).\
            filter(extract('year', Savings.created_at) == selected_year).\
            filter(extract('month', Savings.created_at) ==
                   month['number']).order_by(desc(Savings.created_at)).all()

        if len(data) > 0:
            for item in data:
                total_saving = savings_schema.dump(
                    item) | currency_schema.dump(item)
                total_amount.append(total_saving)

            for item in data:
                monthly_report.append(
                    {month['name']: savings_schema.dump(item)})
    for saving in total_amount:
        total_amount_list.append(saving['amount'])
        currency_code.append(saving["code"])

    global_amount = sum(total_amount_list)
    collect_months_data = Reducer(monthly_report).reduce_list()
    currency = list(set(currency_code))

    return jsonify(data={
        "total_amount": global_amount,
        "today_date": todays_date,
        'monthly_report': collect_months_data,
        'currency_code': currency[0] if len(currency) > 0 else ""
    })


# Get saving by date
@savings.get("/retrieve-date")
@jwt_required(refresh=True)
def get_savings_date():
    user_id = get_jwt_identity()['id']
    item_list: list = []
    total_amount_list = []
    currency_amount = []
    currency_code = []

    data = request.json

    currency_data_code = db.session.query(Currency.code).\
        filter(Currency.id == data["currency_id"]).all()

    data = db.session.query(
        Savings.amount,
        Savings.description,
        Savings.created_at,
        Savings.money_provenance,
        Currency.code).\
        join(Currency, Savings.currency_id == Currency.id).\
        filter(Savings.currency_id == data["currency_id"]).\
        filter(Savings.user_id == user_id).\
        filter(extract('year', Savings.created_at) == data["year"]).\
        filter(extract('month', Savings.created_at) ==
               data["month"]).order_by(desc(Savings.created_at)).all()

    for item in data:
        item_list.append(savings_schema.dump(item))
        currency_amount.append(
            savings_schema.dump(item) | currency_schema.dump(item)
        )

    for code in currency_data_code:
        currency_code.append(currency_schema.dump(code))

    for item in item_list:
        total_amount_list.append(item['amount'])

    total_amount = sum(total_amount_list)

    return jsonify(data={
        "saving_list": currency_amount,
        "total_amount": {
            "currency": currency_code[0]["code"],
            "amount":  total_amount
        },
        "today_date": todays_date,
    })
