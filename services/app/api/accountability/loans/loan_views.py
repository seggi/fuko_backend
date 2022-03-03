from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from api.accountability.global_amount.global_amount_views import QUERY

from api.core.query import QueryGlobalRepport
from api.utils.responses import response_with
from api.utils import responses as resp
from api.utils.model_marsh import LoanSchema

from ... import db
from api.database.models import Loans, User
loans = Blueprint("loans", __name__,
                  url_prefix="/api/user/account/loans")

QUERY = QueryGlobalRepport()

# Register loans data


@loans.post("/add-loans/<int:user_id>")
@jwt_required()
def user_add_loans(user_id):
    # Generate inputs
    data = request.json | {"user_id": user_id}
    if data["amount"] is None or data["description"] is None:
        return response_with(resp.INVALID_INPUT_422)
    else:
        QUERY.insert_data(db=db, table_data=Loans(**data))
    return jsonify({
        "code": "success",
        "message": "Amount saved with success"
    })

# Get all loans


@loans.get("/retrieve/<int:user_id>")
@jwt_required()
def user_get_loans(user_id):
    item_list = []
    loans_schema = LoanSchema()
    data = QUERY.get_data(db=db, model=Loans, user_id=user_id)
    for item in data:
        item_list.append(loans_schema.dump(item))
    return jsonify(data=item_list)


# Get saving by date
@loans.get("/retrieve-date/<int:user_id>")
@jwt_required()
def get_loans_date(user_id):
    data = request.json | {"user_id": user_id}
    pass
