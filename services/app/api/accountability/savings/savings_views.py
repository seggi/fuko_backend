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


@savings.post("/add-saving/<int:user_id>")
@jwt_required()
def user_add_saving(user_id):
    # Generate inputs
    data = request.json | {"user_id": user_id}
    if data["amount"] is None or data["description"] is None:
        return response_with(resp.INVALID_INPUT_422)
    else:
        QUERY.insert_data(db=db, table_data=Savings(**data))
    return jsonify({
        "code": "success",
        "message": "Amount saved with success"
    })


@savings.get("/savings/<int:user_id>")
@jwt_required()
def user_get_saving(user_id):
    item_list = []
    savings_schema = SavingsSchema()
    data = QUERY.get_data(db=db, model=Savings, user_id=user_id)
    for item in data:
        item_list.append(savings_schema.dump(item))
    return jsonify(data=item_list)
