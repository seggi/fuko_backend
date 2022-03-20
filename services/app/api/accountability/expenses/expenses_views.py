from datetime import date
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from itsdangerous import json
from sqlalchemy import extract, desc

from api.accountability.global_amount.global_amount_views import QUERY
from api.core.query import QueryGlobalRepport
from api.utils.responses import response_with
from api.utils import responses as resp
from api.utils.model_marsh import ExpenseDetailsSchema, ExpensesSchema
from api.core.labels import AppLabels

from ... import db
from api.database.models import ExpenseDetails, Expenses, User
expenses = Blueprint("expenses", __name__,
                     url_prefix="/api/user/account")

QUERY = QueryGlobalRepport()

# Register expenses
# Get current date
todays_date = date.today()
APP_LABEL = AppLabels()


@expenses.post("/create-expenses/<int:user_id>")
@jwt_required()
def user_create_expense(user_id):
    data = request.json | {"user_id": user_id}
    if data['expense_name'] is None and data['user_id'] is None:
        return response_with(resp.INVALID_INPUT_422)
    # expense = Expenses.query.filter_by(
    #     expense_name=data['expense_name']).first()
    # if expense:
    #     return jsonify(message=APP_LABEL.label("Expense name already exist"))

    # else:
    QUERY.insert_data(db=db, table_data=Expenses(**data))
    return jsonify(data={
        "code": APP_LABEL.label("success"),
        "message": APP_LABEL.label("Expense saved with success")
    })


@expenses.post("/add-expenses-details/<int:expense_id>")
@jwt_required()
def user_add_expenses(expense_id):
    # Generate inputs
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


# Retrieve all expense

@expenses.get("/expenses/<int:user_id>")
@jwt_required()
def user_get_expense(user_id):
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


@ expenses.get("/expense-details/<int:expense_id>")
@ jwt_required()
def user_get_expense_details(expense_id):
    item_list: list = []
    total_amount_list = []
    expenses_details_schema = ExpenseDetailsSchema()
    data = ExpenseDetails.query.filter_by(expense_id=expense_id).all()
    for item in data:
        item_list.append(expenses_details_schema.dump(item))

    for item in item_list:
        total_amount_list.append(item['amount'])

    total_amount = sum(total_amount_list)

    return jsonify(data={
        "expenses_list": item_list,
        "total_amount": total_amount,
        "today_date": todays_date,
    })


@ expenses.get("/expenses-by-date/<int:expense_id>")
@ jwt_required()
def user_get_expenses_by_date(expense_id):
    item_list: list = []
    total_amount_list = []
    expenses_details_schema = ExpenseDetailsSchema()
    data = ExpenseDetails.query.filter_by(expense_id=expense_id).\
        filter(extract('year', ExpenseDetails.created_at) == todays_date.year).\
        filter(extract('month', ExpenseDetails.created_at) ==
               todays_date.month).order_by(desc(ExpenseDetails.created_at)).all()

    for item in data:
        item_list.append(expenses_details_schema.dump(item))

    for item in item_list:
        total_amount_list.append(item['amount'])

    total_amount = sum(total_amount_list)

    return jsonify(data={
        "expenses_list": item_list,
        "total_amount": total_amount,
        "today_date": todays_date,
    })
