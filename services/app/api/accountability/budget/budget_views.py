from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.core.objects import ManageQuery

from ... import db
from api.accountability.global_amount.global_amount_views import QUERY
from api.database.models import Budget, BudgetDetails, User

from api.utils.model_marsh import BudgetDetailsSchema, BudgetSchema

budget = Blueprint("budget", __name__, url_prefix="/api/user/budget")

manage_query = ManageQuery()

@budget.get("/all")
@jwt_required()
def user_budget():
    user_id = get_jwt_identity()['id']
    item_list: list = []
    budget_schema = BudgetSchema()
    data = QUERY.get_data(db=db, model=Budget, user_id=user_id)
    for item in data:
        item_list.append(budget_schema.dump(item))
    return jsonify(data=item_list)


@budget.post("/create-budget")
@jwt_required()
def create_budget():
    user_id = get_jwt_identity()['id']
    data = request.json | {"user_id": user_id}
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
    data = request.json | {"budget_id": budget_id}
    for value in data["data"]:
        QUERY.insert_data(db=db, table_data=BudgetDetails(
            **value))
    return jsonify({
        "code": "success",
        "message": "Budget details saved with success"
    })


@budget.get("/get-budget-details/<int:budget_id>")
@jwt_required()
def get_budget_details(budget_id):
    user_id = get_jwt_identity()['id']
    budget_details = db.session.query(BudgetDetails).outerjoin(
        Budget, BudgetDetails.budget_id == Budget.id).filter(Budget.user_id == user_id).\
        filter(BudgetDetails.budget_id == budget_id).all()

    budget = db.session.query(Budget).outerjoin(
        BudgetDetails, Budget.id == BudgetDetails.budget_id).\
        filter(BudgetDetails.budget_id == budget_id).all()

    budget_schema = BudgetSchema(many=True).dump(budget)
    budget_details_schema = BudgetDetailsSchema(many=True).dump(budget_details)

    total_amount = manage_query.generate_total_amount(budget_details_schema)
    
    total = {
        "total_amount": sum(total_amount),
        "currency": ""
    }

    collect_amount = budget_details_schema + budget_schema + [total]

    return jsonify(data=collect_amount)
