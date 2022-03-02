from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ... import db
from api.accountability.global_amount.global_amount_views import QUERY
from api.database.models import Budget

from api.utils.model_marsh import BudgetSchema


budget = Blueprint("budget", __name__, url_prefix="/api/user/budget")


@budget.get("/budget/<int:user_id>")
@jwt_required()
def user_budget(user_id):
    item_list: list = []
    budget_schema = BudgetSchema()
    data = QUERY.get_data(db=db, model=Budget, user_id=user_id)
    for item in data:
        item_list.append(budget_schema.dump(item))
    return jsonify(data=item_list)
