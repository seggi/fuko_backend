from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_current_user

from ... import db
from api.accountability.global_amount.global_amount_views import QUERY
from api.database.models import Budget, BudgetDetails, User

from api.utils.model_marsh import BudgetDetailsSchema, BudgetSchema


budget = Blueprint("budget", __name__, url_prefix="/api/user/budget")


@budget.get("/all/<int:user_id>")
@jwt_required()
def user_budget(user_id):
    item_list: list = []
    budget_schema = BudgetSchema()
    data = QUERY.get_data(db=db, model=Budget, user_id=user_id)
    for item in data:
        item_list.append(budget_schema.dump(item))
    return jsonify(data=item_list)


@budget.post("/create-budget/<int:user_id>")
@jwt_required()
def create_budget(user_id):
    data = request.json

    for value in data["data"]:
        QUERY.insert_data(db=db, table_data=Budget(
            **value))
    return jsonify({
        "code": "success",
        "message": "Budget saved with success"
    })


@budget.post("/save-budget-details/<int:budget_id>")
@jwt_required()
def save_budget_details(budget_id):
    data = request.json
    for value in data["data"]:
        QUERY.insert_data(db=db, table_data=BudgetDetails(
            **value))
    return jsonify({
        "code": "success",
        "message": "Budget details saved with success"
    })


@budget.get("/get-budget-details/<int:user_id>/<int:budget_id>")
@jwt_required()
def get_budget_details(user_id, budget_id):
    collect_total_amount = []
    budget_details = db.session.query(BudgetDetails).outerjoin(
        Budget, BudgetDetails.budget_id == Budget.id).filter(Budget.user_id == user_id).\
        filter(BudgetDetails.budget_id == budget_id).all()

    budget = db.session.query(Budget).outerjoin(
        BudgetDetails, Budget.id == BudgetDetails.budget_id).\
        filter(BudgetDetails.budget_id == budget_id).all()

    budget_schema = BudgetSchema(many=True).dump(budget)
    budget_details_schema = BudgetDetailsSchema(many=True).dump(budget_details)

    for item in budget_details_schema:
        collect_total_amount.append(item['amount'])
    total = {
        "total_amount": sum(collect_total_amount),
        "currency": ""
    }

    collect_amount = budget_details_schema + budget_schema + [total]

    return jsonify(data=collect_amount)
