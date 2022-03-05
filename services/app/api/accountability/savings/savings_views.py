from datetime import date
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from api.accountability.global_amount.global_amount_views import QUERY

from api.core.query import QueryGlobalRepport
from api.utils.responses import response_with
from api.utils import responses as resp
from api.utils.model_marsh import SavingsSchema

from ... import db
from api.database.models import Savings, User
savings = Blueprint("savings", __name__,
                    url_prefix="/api/user/account/savings")

QUERY = QueryGlobalRepport()

# Register saving data

todays_date = date.today()


@savings.post("/add-saving/<int:user_id>")
@jwt_required()
def user_add_saving(user_id):
    # Generate inputs
    data = request.json
    for value in data["data"]:
        QUERY.insert_data(db=db, table_data=Savings(**value))
    return jsonify({
        "code": "success",
        "message": "Amount saved with success"
    })


# Get all savings


@savings.get("/retrieve-by-date/<int:user_id>")
@jwt_required()
def user_get_saving_by_date(user_id):
    item_list: list = []
    total_amount_list = []
    savings_schema = SavingsSchema()
    data = QUERY.single_table_by_date(db=db, model=Savings, user_id=user_id, date={
        "year": todays_date.year, "month": todays_date.month})
    for item in data:
        item_list.append(savings_schema.dump(item))

    for item in item_list:
        total_amount_list.append(item['amount'])

    total_amount = sum(total_amount_list)

    return jsonify(data={
        "saving_list": item_list,
        "total_amount": total_amount,
        "today_date": todays_date,
    })


# Get saving by date
@savings.get("/retrieve-date/<int:user_id>")
@jwt_required()
def get_savings_date(user_id):
    data = request.json | {"user_id": user_id}
    pass
