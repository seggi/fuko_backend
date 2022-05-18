from datetime import date
from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from itsdangerous import json
from sqlalchemy import extract, desc

from api.accountability.global_amount.global_amount_views import QUERY
from api.core.query import QueryGlobalRepport
from api.utils.responses import response_with
from api.utils import responses as resp
from api.utils.model_marsh import CurrenySchema, ExpenseDetailsSchema, ExpensesSchema
from api.core.labels import AppLabels

from ... import db
from api.database.models import Currency, ExpenseDetails, Expenses, User
expenses = Blueprint("expenses", __name__,
                     url_prefix="/api/user/account")

QUERY = QueryGlobalRepport()

# Register expenses
# Get current date
todays_date = date.today()
now = datetime.now()
APP_LABEL = AppLabels()
currency_schema = CurrenySchema()
expense_schema = ExpensesSchema()
expense_detail_schema = ExpenseDetailsSchema()


@expenses.post("/create-expenses")
@jwt_required(refresh=True)
def user_create_expense():
    user_id = get_jwt_identity()['id']
    data = request.json | {"user_id": user_id}
    expense = Expenses.query.filter_by(
        expense_name=data['expense_name']).first()
    if data['expense_name'] is None and data['user_id'] is None:
        return response_with(resp.INVALID_INPUT_422)
        
    if expense:
        return jsonify({
            "code": APP_LABEL.label("Alert"),
            "message": APP_LABEL.label("Expense name already exist")
        })

    else:
        QUERY.insert_data(db=db, table_data=Expenses(**data))
        return jsonify({
            "code": APP_LABEL.label("success"),
            "message": APP_LABEL.label("Expense saved with success")
        })

# Retrieve all expense
@expenses.get("/expenses")
@jwt_required(refresh=True)
def user_get_expense():
    user_id = get_jwt_identity()['id']
    expenses_list: list = []
    expenses_details_list: list = []
    total_amount_list = []
    expenses_schema = ExpensesSchema()
    expenses_details_schema = ExpenseDetailsSchema()
    expenses = QUERY.get_data(db=db, model=Expenses, user_id=user_id)
    expenses_details = db.session.query(ExpenseDetails).join(
        Expenses, ExpenseDetails.expense_id == Expenses.id, isouter=True).\
        filter(Expenses.user_id == user_id).order_by(
            desc(ExpenseDetails.created_at)).all()

    for item in expenses:
        expenses_list.append(expenses_schema.dump(item))

    for item in expenses_details:
        expenses_details_list.append(
            expenses_details_schema.dump(item))

    for item in expenses_details_list:
        total_amount_list.append(item['amount'])

    total_amount = sum(total_amount_list)

    return jsonify(data={
        "expense": expenses_list,
        "total": total_amount
    })


# Update Expenses
@expenses.put("/update-expense/<int:expense_id>")
@jwt_required(refresh=True)
def update_expense(expense_id):
    user_id = get_jwt_identity()['id']
    try:
        data = request.json
        if data['expense_name'] is None:
            return response_with(resp.INVALID_INPUT_422)
        else:
            expense = db.session.query(Expenses).filter(
                Expenses.id == expense_id, 
                Expenses.user_id == user_id
            ).one()
            expense.expense_name = data['expense_name']
            expense.updated_at = now
            db.session.commit()
            return jsonify({
                "code": APP_LABEL.label("success"),
                "message": APP_LABEL.label("Expene name updated with success"),
                "data": expense_schema.dump(expense)
            })

    except Exception:
        return response_with(resp.INVALID_FIELD_NAME_SENT_422)

# Add Expense details
@expenses.post("/add-expenses-details/<int:expense_id>")
@jwt_required(refresh=True)
def user_add_expenses(expense_id):
    # Generate inputs
    try:
        data = request.json
        for value in data["data"]:
            if value['amount'] is None and value['expense_id'] is None:
                return response_with(resp.INVALID_INPUT_422)
            else:
                QUERY.insert_data(db=db, table_data=ExpenseDetails(
                    **value | {"expense_id": expense_id}))

        return jsonify({
            "code": APP_LABEL.label("success"),
            "message": APP_LABEL.label("Expense Amount saved with success")
        })

    except Exception as e:
        return response_with(resp.INVALID_INPUT_422)

#  Get expenses details
@expenses.get("/expense-details/<int:expense_details_id>")
@jwt_required(refresh=True)
def user_get_expense_details(expense_details_id):
    item_list: list = []
    total_amount_list = []
    currency_amount = []
    data = db.session.query(
        ExpenseDetails.amount, 
        ExpenseDetails.created_at, 
        ExpenseDetails.description,
        Currency.code).\
        join(Currency, ExpenseDetails.currency_id == Currency.id).\
        filter(ExpenseDetails.expense_id == expense_details_id).\
        order_by(desc(ExpenseDetails.created_at)).all()

    for item in data:
        item_list.append(expense_detail_schema.dump(item))
        currency_amount.append([expense_detail_schema.dump(item) | currency_schema.dump(item)])
    

    for item in item_list:
        total_amount_list.append(item['amount'])

    total_amount = sum(total_amount_list)

    return jsonify(data={
        "expenses_list": currency_amount,
        "total_amount": total_amount,
        "today_date": todays_date,
    })

# Retrieve default
# Expenses by current date
@ expenses.get("/expenses-by-current-date/<int:expense_id>/<int:currency_id>")
@ jwt_required(refresh=True)
def user_get_expenses_by_date(expense_id, currency_id):
    item_list: list = []
    total_amount_list = []
    currency_amount = []
    curency_code = []

    curency_data_code = db.session.query(Currency.code).\
            filter(Currency.id == currency_id).all()

    data = db.session.query(
                ExpenseDetails.amount,
                ExpenseDetails.created_at, 
                ExpenseDetails.id,
                ExpenseDetails.description,
                Currency.code,
            ).\
        join(Currency, ExpenseDetails.currency_id == Currency.id).\
        filter(ExpenseDetails.expense_id == expense_id).\
        filter(ExpenseDetails.currency_id == currency_id).\
        filter(extract('year', ExpenseDetails.created_at) == todays_date.year).\
        filter(extract('month', ExpenseDetails.created_at) ==
               todays_date.month).order_by(desc(ExpenseDetails.created_at)).all()
   
    for item in data:
        item_list.append(expense_detail_schema.dump(item))
        currency_amount.append(
            expense_detail_schema.dump(item) | currency_schema.dump(item)
        )

    for item in item_list:
        total_amount_list.append(item['amount'])

    for code in curency_data_code:
            curency_code.append(currency_schema.dump(code))

    total_amount = sum(total_amount_list)

    return jsonify(data={
            "expenses_list": currency_amount,
            "total_amount": {
                "currency": curency_code[0]['code'],
                "amount": total_amount
            },
            "today_date": todays_date,
        })

# Expenses by date (month and year)
@ expenses.post("/expenses-by-month/<int:expense_id>")
@ jwt_required(refresh=True)
def user_get_expenses_by_month(expense_id):
    try:
        data = request.json
        item_list: list = []
        total_amount_list = []
        currency_amount = []
        curency_code = []

        curency_data_code = db.session.query(Currency.code).\
            filter(Currency.id == data['currency_id']).all()

        data = db.session.query(
                ExpenseDetails,
                ExpenseDetails.amount,
                ExpenseDetails.created_at, 
                ExpenseDetails.id,
                ExpenseDetails.description,
                Currency.code,
            ).\
            join(Currency, ExpenseDetails.currency_id == Currency.id).\
            filter(ExpenseDetails.expense_id == expense_id).\
            filter(ExpenseDetails.currency_id == data['currency_id']).\
            filter(extract('year', ExpenseDetails.created_at) ==data['year']).\
            filter(extract('month', ExpenseDetails.created_at) ==data['month']
               ).order_by(desc(ExpenseDetails.created_at)).all()

        

        for item in data:
            item_list.append(expense_detail_schema.dump(item))
            currency_amount.append(
                expense_detail_schema.dump(item) | currency_schema.dump(item)
            )

        for item in item_list:
            total_amount_list.append(item['amount'])

        for code in curency_data_code:
            curency_code.append(currency_schema.dump(code))

        total_amount = sum(total_amount_list)

        return jsonify(data={
            "expenses_list": currency_amount,
            "total_amount": {
                "currency": curency_code[0]['code'],
                "amount": total_amount
            },
            "today_date": todays_date,
        })

    except Exception as e:
        return response_with(resp.INVALID_FIELD_NAME_SENT_422)



# Update Expense Details
@expenses.put("/update-expense-detail/<int:expense_detials_id>")
@jwt_required(refresh=True)
def update_expense_detial(expense_detials_id):
    user_id = get_jwt_identity()['id']
    try:
        data = request.json
        if data['description'] is None:
            return response_with(resp.INVALID_INPUT_422)
        else:
            expense_details = db.session.query(ExpenseDetails).filter(
                Expenses.id == expense_detials_id, 
                Expenses.user_id == user_id
            ).one()
            expense_details.description = data['description']
            expense_details.currency_id = data['currency_id']
            expense_details.updated_at = now
            db.session.commit()
            return jsonify({
                "code": APP_LABEL.label("success"),
                "message": APP_LABEL.label("Expene name updated with success"),
                "data": expense_detail_schema.dump(expense_details)
            })

    except Exception:
        return response_with(resp.INVALID_FIELD_NAME_SENT_422)