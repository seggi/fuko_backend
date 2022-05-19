from datetime import date
from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from itsdangerous import json
from sqlalchemy import extract, desc

from api.accountability.global_amount.global_amount_views import QUERY
from api.core.query import QueryGlobalRepport
from api.utils.responses import response_with
from api.utils import responses as resp
from api.utils.model_marsh import UserCreateGroupSchema
from api.core.labels import AppLabels

from ... import db
from api.database.models import Currency, ExpenseDetails, Expenses, User,UserCreateGroup

now = datetime.now()
APP_LABEL = AppLabels()
user_create_group_schema = UserCreateGroupSchema()

group = Blueprint("group", __name__,
                     url_prefix="/api/user/account/group")

todays_date = date.today()

@group.post("/create-group")
@jwt_required(refresh=True)
def user_create_group():
    user_id = get_jwt_identity()['id']
    data = request.json | {"user_id": user_id}
    group = UserCreateGroup.query.filter_by(
        group_name=data['group_name']).first()
    if data['group_name'] is None and data['user_id'] is None:
        return response_with(resp.INVALID_INPUT_422)
        
    if group:
        return jsonify({
            "code": APP_LABEL.label("Alert"),
            "message": APP_LABEL.label("Group name already exist")
        })

    else:
        QUERY.insert_data(db=db, table_data=UserCreateGroup(**data))
        return jsonify({
            "code": APP_LABEL.label("success"),
            "message": APP_LABEL.label("Group name saved with success")
        })

@group.post("/update-group/<int:group_id>")
@jwt_required(refresh=True)
def user_update_group(group_id):
    user_id = get_jwt_identity()['id']
    data = request.json | {"user_id": user_id}
    
    if data['group_name'] is None:
        return response_with(resp.INVALID_INPUT_422)

    else:
        groups = db.session.query(UserCreateGroup).filter(
                UserCreateGroup.id == group_id, 
                UserCreateGroup.user_id == user_id
            ).one()
        groups.group_name = data["group_name"]
        groups.updated_at = now
        db.session.commit()
        return jsonify({
            "code": APP_LABEL.label("success"),
            "message": APP_LABEL.label("Group name updated with success")
        })

@group.get("/retrieve-group")
@jwt_required(refresh=True)
def retrieve_create_group():
    user_id = get_jwt_identity()['id']
    group_list: list = []

    group_data = db.session.query(UserCreateGroup).\
        filter(UserCreateGroup.user_id == user_id).\
        order_by(desc(UserCreateGroup.created_at)).all()

    for item in group_data:
        group_list.append(user_create_group_schema.dump(item))

    return jsonify({
        "all_group": group_list
    })
