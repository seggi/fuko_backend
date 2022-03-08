from datetime import date
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from itsdangerous import json
from api.accountability.global_amount.global_amount_views import QUERY

from api.core.query import QueryGlobalRepport
from api.utils.responses import response_with
from api.utils import responses as resp
from api.utils.model_marsh import ExpensesSchema
from api.core.labels import AppLabels

from ... import db
from api.database.models import Expenses, User
expenses = Blueprint("expenses", __name__,
                     url_prefix="/api/user/account")

QUERY = QueryGlobalRepport()

# Register expenses
# Get current date
todays_date = date.today()
APP_LABEL = AppLabels()


# @expenses.post("/create-expenses/<int:user_id>")
# @jwt_required()
# def user_create_expense(user_id):
#     data = request.json | {"user_id": user_id}
#     if data['expense_name'] is None and data['user_id'] is None:
#         return response_with(resp.INVALID_INPUT_422)

#     if User.find_by_email(data['email']) or User.find_by_username(data['username']):
#         return response_with(resp.SUCCESS_201)

#     if Expenses.find_by_expense_name(data['expense_name']):
#         return jsonify(message=APP_LABEL.label("Expense name already exist"))

#     else:
#         QUERY.insert_data(db=db, table_data=Expenses(**data))
#         return jsonify(data={
#             "code": APP_LABEL.label("success"),
#             "message": APP_LABEL.label("Expense saved with success")
#         })


@expenses.post("/expenses-details/<int:expense_id>")
@jwt_required()
def user_add_expenses(expense_id):
    # Generate inputs
    data = request.json | {"expense_id": expense_id}
    for value in data["data"]:
        QUERY.insert_data(db=db, table_data=ExpenseDetails(**value))
    return jsonify({
        "code": APP_LABEL.label("success"),
        "message": APP_LABEL.label("Amount saved with success")
    })


# Retrieve all expense


@expenses.get("/expenses/<int:user_id>")
@jwt_required()
def user_get_expenses(user_id):
    item_list: list = []
    total_amount_list = []
    expenses_schema = ExpensesSchema()
    data = QUERY.get_data(db=db, model=Expenses, user_id=user_id)
    for item in data:
        item_list.append(expenses_schema.dump(item))

    for item in item_list:
        total_amount_list.append(item['amount'])

    total_amount = sum(total_amount_list)

    return jsonify(data={
        "expenses_list": item_list,
        "total_amount": total_amount,
        "today_date": todays_date,
    })


@expenses.get("/expenses-by-date/<int:user_id>")
@jwt_required()
def user_get_expenses_by_date(user_id):
    item_list: list = []
    total_amount_list = []
    expenses_schema = ExpensesSchema()
    data = QUERY.single_table_by_date(db=db, model=Expenses, user_id=user_id, date={
        "year": todays_date.year, "month": todays_date.month})
    for item in data:
        item_list.append(expenses_schema.dump(item))

    for item in item_list:
        total_amount_list.append(item['amount'])

    total_amount = sum(total_amount_list)

    return jsonify(data={
        "expenses_list": item_list,
        "total_amount": total_amount,
        "today_date": todays_date,
    })
