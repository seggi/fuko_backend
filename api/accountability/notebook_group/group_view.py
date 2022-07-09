from datetime import date
from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from itsdangerous import json
from sqlalchemy import extract, desc

from api.accountability.global_amount.global_amount_views import QUERY
from api.utils.responses import response_with
from api.utils import responses as resp
from api.utils.model_marsh import GroupMemberSchema, RequestStatusSchema, UserCreateGroupSchema, UserSchema
from api.core.labels import AppLabels

from ... import db
from api.database.models import Currency, ExpenseDetails, Expenses, GroupMembers, RequestStatus, User, UserCreateGroup

REQUEST_SENT = "49"
REQUEST_CANCELED = "52"
REQUEST_ACCEPTED = "50"
REQUEST_REJECTED = "51"

now = datetime.now()
APP_LABEL = AppLabels()
user_schema = UserSchema()
user_create_group_schema = UserCreateGroupSchema()
group_member_schema = GroupMemberSchema()
request_status_schema = RequestStatusSchema()

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


@group.post("/add-partner-to-your-group")
@jwt_required(refresh=True)
def add_partner_to_group():
    user_id = get_jwt_identity()['id']
    try:
        request_data = request.json | {"request_status": REQUEST_SENT}
        QUERY.insert_data(db=db, table_data=GroupMembers(**request_data))
        return jsonify({
            "code": APP_LABEL.label("success"),
            "message": APP_LABEL.label("Friend added with success")
        })
    except Exception:
        return response_with(resp.INVALID_INPUT_422)


class ManageRequest:
    def __init__(self, data=[], schema=[]) -> None:
        self.schema = schema
        self.data = data

    def getRequest(self) -> list:
        schema_list = []
        # new_dict = {}
        for schema in self.schema:
            schema_list.append(self.getSchema(schema))

        # for item in schema_list:
        #     new_dict.update(item)
        return schema_list

    def getSchema(self, schema) -> dict:
        schema_dict = list()
        for item in self.data:
            schema_dict.append(schema.dump(item))
        return schema_dict


@group.get("/retrieve-request-sent")
@jwt_required(refresh=True)
def get_sent_request():
    user_id = get_jwt_identity()['id']
    group_member = []
    request_status_list = []
    user_create_group_list = []
    member_list = []
    add_list = []
    get_request = db.session.query(
        User.username,
        GroupMembers.requested_at,
        UserCreateGroup.group_name,
        RequestStatus.request_status_name).\
        join(User, GroupMembers.user_id == User.id).\
        join(UserCreateGroup, GroupMembers.group_id == UserCreateGroup.id).\
        join(RequestStatus, GroupMembers.request_status == RequestStatus.id).\
        filter(UserCreateGroup.id == user_id).\
        filter(GroupMembers.request_status == REQUEST_SENT).\
        order_by(desc(GroupMembers.requested_at)).all()

    for item in get_request:
        member_list.append(user_schema.dump(item))
        user_create_group_list.append(user_create_group_schema.dump(item))
        request_status_list.append(request_status_schema.dump(item))
        group_member.append(group_member_schema.dump(item))

    manage_request = ManageRequest(
        schema=[user_schema, user_create_group_schema], data=[*get_request])
    retrieve_request = manage_request.getRequest()
    # manageRequest(data=[user_schema.dump(item), {"lastname": "serge"}])
    for x in get_request:
        add_list.append(**user_schema.dump(x))
    print(add_list)
    return jsonify("")


@group.put("/cancel-accept-reject-request")
@jwt_required(refresh=True)
def request_status():
    response = jsonify({
        "code": APP_LABEL.label("success"),
        "message": APP_LABEL.label("Request canceled!")
    })
    try:
        data = request.json

        if data["request_status"] == REQUEST_CANCELED:
            group = db.session.query(GroupMembers).filter(
                GroupMembers.id == data['id']).one()
            group.request_status = REQUEST_CANCELED
            group.remove_member_at = now
            db.session.commit()

            return response

        if data["request_status"] == REQUEST_ACCEPTED:
            group = db.session.query(GroupMembers).filter(
                GroupMembers.id == data['id']).one()
            group.request_status = REQUEST_ACCEPTED
            group.remove_member_at = now
            db.session.commit()

            return response

        if data["request_status"] == REQUEST_REJECTED:
            group = db.session.query(GroupMembers).filter(
                GroupMembers.id == data['id']).one()
            group.request_status = REQUEST_REJECTED
            group.remove_member_at = now
            db.session.commit()

            return response

    except Exception:
        return response_with(resp.INVALID_INPUT_422)
