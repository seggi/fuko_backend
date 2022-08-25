from datetime import datetime
from api.core.labels import AppLabels
from api.utils.responses import response_with
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import extract, desc, Date, cast, and_, func

from api.core.objects import ManageQuery

from ... import db
from api.utils import responses as resp
from api.accountability.global_amount.global_amount_views import QUERY
from api.database.models import Budget, BudgetCategories, BudgetDetails, BudgetOption, User

from api.utils.model_marsh import BudgetCategoriesSchema, BudgetDetailsSchema, BudgetOptionSchema, BudgetSchema

now = datetime.now()

budget = Blueprint("budget", __name__, url_prefix="/api/user/budget")

manage_query = ManageQuery()
budget_option_schema = BudgetOptionSchema()
budget_schema = BudgetSchema()
budget_categories_schema = BudgetCategoriesSchema()
budget_details_schema = BudgetDetailsSchema()
APP_LABEL = AppLabels()



@budget.get("/budget-option")
@jwt_required(refresh=True)
def get_budget_options():
    item_list: list = []
    budget_options = QUERY.get_data(db=db, model=BudgetOption)
    for budget_option in budget_options:
        item_list.append(budget_option_schema.dump(budget_option))
    return jsonify(data=item_list)


@budget.get("/budget-category")
@jwt_required(refresh=True)
def get_budget_categories():
    item_list: list = []
    budget_categories = QUERY.get_data(db=db, model=BudgetCategories)
    for budget_category in budget_categories:
        item_list.append(budget_categories_schema.dump(budget_category))
    return jsonify(data=item_list)


@budget.get("/retrieve-all")
@jwt_required(refresh=True)
def user_budget():
    user_id = get_jwt_identity()['id']
    item_list: list = []
    data = QUERY.get_data(db=db, model=Budget, user_id=user_id)
    for item in data:
        item_list.append(budget_schema.dump(item))
    return jsonify(data=item_list)


@budget.post("/create-budget")
@jwt_required(refresh=True)
def create_budget():
    try:
        user_id = get_jwt_identity()['id']
        data = request.json | {"user_id": user_id}
        QUERY.insert_data(db=db, table_data=Budget(**data))
        return jsonify({
            "code": APP_LABEL.label("success"),
            "message": APP_LABEL.label("Budget saved with success")
        })

    except Exception as e:
        return response_with(resp.INVALID_FIELD_NAME_SENT_422)


@budget.put("/update-budget/<int:budget_id>")
@jwt_required(refresh=True)
def update_budget(budget_id):
    try:
        data = request.json
        budget = db.session.query(Budget).filter(
            Budget.id == budget_id,
        ).one()
        budget.name = data['name']
        budget.description = data['description']
        budget.updated_at = now
        budget.start_date = data["start_date"]
        budget.end_date = data["end_date"]
        db.session.commit()
        return jsonify({
            "code": APP_LABEL.label("success"),
            "message": APP_LABEL.label("Budget Updated with success"),
            "data": budget_schema.dump(budget)
        })

    except Exception as e:
        return response_with(resp.INVALID_FIELD_NAME_SENT_422)


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


@budget.post("/add-envelope-budget")
@jwt_required(refresh=True)
def save_budget_envelop():
    try:
        user_id = get_jwt_identity()['id']
        data = request.json
        QUERY.insert_data(db=db, table_data=BudgetDetails(**data))
        return jsonify({
            "code": APP_LABEL.label("success"),
            "message": APP_LABEL.label("Budget envelope saved with success")
        })

    except Exception as e:
        return response_with(resp.INVALID_FIELD_NAME_SENT_422)


@budget.get("/get-envelope/<int:budget_id>/<int:currency_code>")
@jwt_required(refresh=True)
def get_budget_envelop(currency_code, budget_id):
    try:
        user_id = get_jwt_identity()['id']
        collect_data = []
        budget_envelop_data = db.session.query(BudgetDetails.budget_amount, BudgetCategories.name, BudgetDetails.id).\
            join(Budget, BudgetDetails.budget_id == Budget.id).\
            join(BudgetCategories, BudgetDetails.budget_category_id == BudgetCategories.id).\
            filter(Budget.user_id == user_id).\
            filter(BudgetDetails.budget_id == budget_id).\
            filter(BudgetDetails.currency_id == currency_code).\
            order_by(desc(BudgetDetails.created_at)).\
            all()

        for envelope in budget_envelop_data:
            envelopes = budget_details_schema.dump(envelope) | budget_categories_schema.dump(envelope)
            collect_data.append(envelopes)

        return jsonify(data=collect_data)

    except Exception as e:
        print("==>",e)
        return response_with(resp.INVALID_FIELD_NAME_SENT_422)
