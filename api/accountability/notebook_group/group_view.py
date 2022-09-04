from datetime import date
from datetime import datetime
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from itsdangerous import json
from sqlalchemy import extract, desc

from api.accountability.global_amount.global_amount_views import QUERY
from api.utils.responses import response_with
from api.utils import responses as resp
from api.utils.model_marsh import GroupMemberSchema, RequestStatusSchema, UserCreateGroupSchema, UserSchema, GroupeContributorAmountSchema
from api.core.labels import AppLabels

from ... import db
from api.database.models import Currency, ExpenseDetails, Expenses, GroupDepts, GroupMembers, RequestStatus, User, UserCreateGroup, GroupeContributorAmount

REQUEST_SENT = 1
REQUEST_CANCELED = 3
REQUEST_ACCEPTED = 2


now = datetime.now()
APP_LABEL = AppLabels()
user_schema = UserSchema()
user_create_group_schema = UserCreateGroupSchema()
group_member_schema = GroupMemberSchema()
request_status_schema = RequestStatusSchema()
group_contributor_amount_schema = GroupeContributorAmountSchema()

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
        new_group = UserCreateGroup(**data)
        db.session.add(new_group)
        db.session.commit()
        creator = {"group_id": new_group.id,
                   "member_id": user_id,
                   "request_status": REQUEST_ACCEPTED,
                   "accepted_at": now,
                   "sender_id": user_id}

        QUERY.insert_data(db=db, table_data=GroupMembers(**creator))

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

    group_data = db.session.query(
        GroupMembers,
        UserCreateGroup.id,
        UserCreateGroup.user_id,
        UserCreateGroup.group_name,
        User.first_name,
        User.last_name,
        User.username).\
        join(UserCreateGroup, GroupMembers.group_id == UserCreateGroup.id).\
        join(User, UserCreateGroup.user_id == User.id).\
        filter(GroupMembers.request_status == REQUEST_ACCEPTED).\
        filter(GroupMembers.member_id == user_id).\
        order_by(desc(UserCreateGroup.created_at)).all()

    for item in group_data:
        group_list.append({
            **user_create_group_schema.dump(item),
            **user_schema.dump(item),
            **{"creator": True if item['user_id'] == user_id else False}
        })

    return jsonify({
        "all_group": group_list
    })


@group.post("/add-partner-to-your-group")
@jwt_required(refresh=True)
def add_partner_to_group():
    user_id = get_jwt_identity()['id']
    try:
        request_data = request.json | {
            "request_status": REQUEST_SENT, "sender_id": user_id}
        check_friend = db.session.query(GroupMembers).filter(
            GroupMembers.group_id == request_data['group_id'],
            GroupMembers.request_status == REQUEST_SENT,
            GroupMembers.member_id == request_data['member_id']).first()
        if check_friend:
            return jsonify({
                "code": APP_LABEL.label("success"),
                "message": APP_LABEL.label("Request already sent")
            })
        QUERY.insert_data(db=db, table_data=GroupMembers(
            **request_data))
        return jsonify({
            "code": APP_LABEL.label("success"),
            "message": APP_LABEL.label("Request sent with success.")
        })
    except Exception as e:
        print(e)
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
        User.first_name,
        User.last_name,
        GroupMembers.id,
        GroupMembers.sent_at,
        UserCreateGroup.group_name,
        RequestStatus.request_status_name).\
        join(User, GroupMembers.member_id == User.id).\
        join(UserCreateGroup, GroupMembers.group_id == UserCreateGroup.id).\
        join(RequestStatus, GroupMembers.request_status == RequestStatus.id).\
        filter(GroupMembers.sender_id == user_id).\
        filter(GroupMembers.request_status == REQUEST_SENT).\
        order_by(desc(GroupMembers.sent_at)).all()

    for item in get_request:
        member_list.append(user_schema.dump(item))
        user_create_group_list.append(user_create_group_schema.dump(item))
        request_status_list.append(request_status_schema.dump(item))
        group_member.append(group_member_schema.dump(item))

    manage_request = ManageRequest(
        schema=[user_schema, user_create_group_schema], data=[*get_request])
    retrieve_request = manage_request.getRequest()
    # manageRequest(data=[user_schema.dump(item), {"lastname": "serge"}])
    for member in get_request:
        add_list.append({
            **user_schema.dump(member),
            **group_member_schema.dump(member),
            **user_create_group_schema.dump(member),
            **request_status_schema.dump(member)
        })

    return jsonify(data=add_list)


@group.get("/retrieve-request-accepted/<int:group_id>")
@jwt_required(refresh=True)
def get_accepted_request(group_id):
    user_id = get_jwt_identity()['id']
    group_member = []
    request_status_list = []
    user_create_group_list = []
    member_list = []
    add_list = []
    get_request = db.session.query(
        User.username,
        User.first_name,
        User.last_name,
        GroupMembers.id,
        GroupMembers.sent_at,
        UserCreateGroup.group_name,
        RequestStatus.request_status_name).\
        join(User, GroupMembers.member_id == User.id).\
        join(UserCreateGroup, GroupMembers.group_id == UserCreateGroup.id).\
        join(RequestStatus, GroupMembers.request_status == RequestStatus.id).\
        filter(GroupMembers.request_status == REQUEST_ACCEPTED).\
        filter(GroupMembers.group_id == group_id).\
        order_by(desc(GroupMembers.sent_at)).all()

    for item in get_request:
        member_list.append(user_schema.dump(item))
        user_create_group_list.append(user_create_group_schema.dump(item))
        request_status_list.append(request_status_schema.dump(item))
        group_member.append(group_member_schema.dump(item))

    manage_request = ManageRequest(
        schema=[user_schema, user_create_group_schema], data=[*get_request])
    retrieve_request = manage_request.getRequest()
    # manageRequest(data=[user_schema.dump(item), {"lastname": "serge"}])
    for member in get_request:
        add_list.append({
            **user_schema.dump(member),
            **group_member_schema.dump(member),
            **user_create_group_schema.dump(member),
            **request_status_schema.dump(member)
        })

    return jsonify(data=add_list)

# TODO: Calculate Amount


@group.get("/retrieve-member-contribution/<int:group_id>/<int:currency_code>")
@jwt_required(refresh=True)
def retrieve_member_contributions(group_id, currency_code):
    add_list = []
    get_request = db.session.query(
        GroupMembers,
        User.username,
        User.first_name,
        User.last_name,
        GroupeContributorAmount.created_at, GroupeContributorAmount.description,
        GroupeContributorAmount.id, GroupeContributorAmount.amount).\
        join(GroupeContributorAmount, GroupMembers.id == GroupeContributorAmount.contributor_id).\
        join(User, GroupMembers.member_id == User.id).\
        filter(GroupeContributorAmount.currency_id == currency_code).\
        filter(GroupMembers.group_id == group_id).all()

    for member in get_request:
        add_list.append({
            **user_schema.dump(member),
            **group_contributor_amount_schema.dump(member),
        })

    return jsonify(data=add_list)

# ! to changed


@group.get("/retrieve-participator/<int:contribution_id>/<int:currency_code>")
@jwt_required(refresh=True)
def retrieve_participator(contribution_id, currency_code):
    contributor_list = []
    total_amount = []
    new_contributor_list = []
    get_request = db.session.query(
        GroupDepts,
        GroupMembers,
        User.first_name, User.last_name,
        GroupeContributorAmount.id, GroupeContributorAmount.amount).\
        join(GroupeContributorAmount, GroupDepts.contribution_id == GroupeContributorAmount.id).\
        join(GroupMembers, GroupDepts.member_id == GroupMembers.id).\
        join(User, GroupMembers.member_id == User.id).\
        filter(GroupeContributorAmount.currency_id == currency_code).\
        filter(GroupDepts.contribution_id == contribution_id).all()

    for member in get_request:
        contributor_list.append({
            **user_schema.dump(member),
            **group_contributor_amount_schema.dump(member),
        })

    for amounts in contributor_list:
        total_amount.append(amounts['amount'])

    amount_sum = total_amount[0]
    members = len(contributor_list)

    if members > 0:
        splitted_amount = amount_sum / members
        for member in contributor_list:
            new_contributor_list.append({
                **{"username": f"{member['first_name']} {member['last_name']}"},
                **{"id": member["id"]},
                **{"amount": splitted_amount}
            })

    return jsonify(data=new_contributor_list)


# TODO: Saved Amount
@group.post("/save-group-contribution/<int:group_id>")
@jwt_required(refresh=True)
def save_group_contribution(group_id):
    user_id = get_jwt_identity()['id']
    new_member_list = []
    current_user_id = []
    try:
        request_data = request.json
        if request_data:
            current_user = db.session.query(GroupMembers.id).\
                filter(GroupMembers.request_status == REQUEST_ACCEPTED).\
                filter(GroupMembers.member_id == user_id).\
                filter(GroupMembers.group_id == group_id).all()

            group_members = db.session.query(GroupMembers.id, User.username).join(
                User, GroupMembers.member_id == User.id).\
                filter(GroupMembers.request_status == REQUEST_ACCEPTED).\
                filter(GroupMembers.group_id == group_id).all()

            for user in current_user:
                current_user_id.append(group_member_schema.dump(user))

            contributions = {
                **request_data[0], **{"contributor_id": current_user_id[0]["id"]}}

            contribution = GroupeContributorAmount(**contributions)
            db.session.add(contribution)
            db.session.commit()

            if len(request_data[1]['members']) == 0:
                for member in group_members:
                    if member['id'] == current_user_id[0]['id']:
                        new_member_list.append({
                            **{"member_id": group_member_schema.dump(member)['id']},
                            **{"contributor": True},
                            ** {"contribution_id": contribution.id}
                        })
                    if current_user_id[0]['id'] != member['id']:
                        new_member_list.append({
                            **{"member_id": group_member_schema.dump(member)['id']},
                            ** {"contribution_id": contribution.id}
                        })

            else:
                for member in request_data[1]['members']:
                    if member['id'] == current_user_id[0]['id']:
                        new_member_list.append({
                            **{"member_id": member['id']},
                            **{"contributor": True},
                            ** {"contribution_id": contribution.id}
                        })
                    if current_user_id[0]['id'] != member['id']:
                        new_member_list.append({
                            **{"member_id": member['id']},
                            ** {"contribution_id": contribution.id}
                        })

        for member in new_member_list:
            contribution = GroupDepts(**member)
            db.session.add(contribution)
            db.session.commit()

        return jsonify({
            "code": APP_LABEL.label("success"),
            "message": APP_LABEL.label("Amount added with success")
        })

    except Exception as e:
        print(e)
        return response_with(resp.INVALID_INPUT_422)


@group.put("/cancel-accept-reject-request")
@jwt_required(refresh=True)
def request_status():
    try:
        data = request.json

        if data["request_status"] == REQUEST_CANCELED:
            group = db.session.query(GroupMembers).filter(
                GroupMembers.id == data['id']).one()
            if group:
                group.request_status = REQUEST_CANCELED
                group.remove_member_at = now
                db.session.commit()

                return jsonify({
                    "code": APP_LABEL.label("success"),
                    "message": APP_LABEL.label("Request canceled!")
                })

            return jsonify({
                "code": APP_LABEL.label("Alert"),
                "message": APP_LABEL.label("Group does not exist")
            })

        if data["request_status"] == REQUEST_ACCEPTED:
            group = db.session.query(GroupMembers).filter(
                GroupMembers.id == data['id']).one()
            if group:
                group.request_status = REQUEST_ACCEPTED
                group.accepted_at = now
                db.session.commit()

                return jsonify({
                    "code": APP_LABEL.label("success"),
                    "message": APP_LABEL.label("Request accepted!")
                })

            return jsonify({
                "code": APP_LABEL.label("Alert"),
                "message": APP_LABEL.label("Group does not exist")
            })

        if data["request_status"] == REQUEST_CANCELED:
            group = db.session.query(GroupMembers).filter(
                GroupMembers.id == data['id']).one()
            if group:
                group.request_status = REQUEST_CANCELED
                group.remove_member_at = now
                db.session.commit()

                return jsonify({
                    "code": APP_LABEL.label("success"),
                    "message": APP_LABEL.label("Request canceled!")
                })

            return jsonify({
                "code": APP_LABEL.label("Alert"),
                "message": APP_LABEL.label("Group does not exist")
            })

    except Exception:
        return response_with(resp.INVALID_INPUT_422)
