from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from api.accountability.global_amount.global_amount_views import QUERY

from api.core.query import QueryGlobalRepport
from api.utils.responses import response_with
from api.utils import responses as resp
from api.utils.model_marsh import DeptsSchema

from ... import db
from api.database.models import Depts, User
dept = Blueprint("dept", __name__,
                 url_prefix="/api/user/account/dept")

QUERY = QueryGlobalRepport()

# Register dept data


@dept.post("/add-dept/<int:user_id>")
@jwt_required()
def user_add_dept(user_id):
    # Generate inputs
    data = request.json | {"user_id": user_id}
    if data["amount"] is None or data["description"] is None:
        return response_with(resp.INVALID_INPUT_422)
    else:
        QUERY.insert_data(db=db, table_data=Depts(**data))
    return jsonify({
        "code": "success",
        "message": "Amount saved with success"
    })

# Get all dept


@dept.get("/retrieve/<int:user_id>")
@jwt_required()
def user_get_dept(user_id):
    item_list = []
    dept_schema = DeptsSchema()
    data = QUERY.get_data(db=db, model=Depts, user_id=user_id)
    for item in data:
        item_list.append(dept_schema.dump(item))
    return jsonify(data=item_list)


# Get saving by date
@dept.get("/retrieve-date/<int:user_id>")
@jwt_required()
def get_dept_date(user_id):
    data = request.json | {"user_id": user_id}
    pass
