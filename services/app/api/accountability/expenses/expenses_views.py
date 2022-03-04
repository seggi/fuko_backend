from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from api.accountability.global_amount.global_amount_views import QUERY

from api.core.query import QueryGlobalRepport
from api.utils.responses import response_with
from api.utils import responses as resp
from api.utils.model_marsh import ExpensesSchema

from ... import db
from api.database.models import Expenses, User
expenses = Blueprint("expenses", __name__,
                     url_prefix="/api/user/account")

QUERY = QueryGlobalRepport()

# Register expenses


@expenses.post("/add-expenses/<int:user_id>")
@jwt_required()
def user_add_expenses(user_id):
    # Generate inputs
    data = request.json
    for value in data["data"]:
        QUERY.insert_data(db=db, table_data=Expenses(**value))
    return jsonify({
        "code": "success",
        "message": "Amount saved with success"
    })


# Retrieve all expense


@expenses.get("/expenses/<int:user_id>")
# @jwt_required()
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
        "total_amount": total_amount
    })
