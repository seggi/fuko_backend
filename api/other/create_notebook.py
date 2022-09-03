from datetime import datetime
from api.accountability.notebook_group.group_view import REQUEST_SENT
from api.utils.model_marsh import GroupMemberSchema, GroupeContributorAmountSchema, NoteBookMemberSchema, NoteBookSchema, RequestStatusSchema, UserCreateGroupSchema, UserSchema
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import extract, desc
from api.accountability.global_amount.global_amount_views import QUERY

from api.core.query import QueryGlobalReport
from api.utils.responses import response_with
from api.utils import responses as resp
from api.core.labels import AppLabels
from api.utils.model_marsh import NoteBookSchema

from .. import db
from api.database.models import DeptNoteBook, GroupMembers, LoanNoteBook, NoteBook, NoteBookMember, RequestStatus, User, UserCreateGroup

QUERY = QueryGlobalReport()
APP_LABEL = AppLabels()
now = datetime.now()

notebook = Blueprint("notebook", __name__,
                     url_prefix="/api/user/notebook")

user_schema = UserSchema()
noteBookSchema = NoteBookSchema()
notebook_member_schema = NoteBookMemberSchema()
request_status_schema = RequestStatusSchema()
user_create_group_schema = UserCreateGroupSchema()
group_member_schema = GroupMemberSchema()
request_status_schema = RequestStatusSchema()
group_contributor_amount_schema = GroupeContributorAmountSchema()
# Create NoteBook


@notebook.post("/create")
@jwt_required(refresh=True)
def create_notebook():
    try:
        user_id = get_jwt_identity()['id']
        data = request.json | {"user_id": user_id}
        QUERY.insert_data(db=db, table_data=NoteBook(**data))
        return jsonify({
            "code": APP_LABEL.label("success"),
            "message": APP_LABEL.label("Notebook created with success")
        })
    except Exception:
        return response_with(resp.INVALID_INPUT_422)


@notebook.get("/retrieve")
@jwt_required(refresh=True)
def retrieve_notebook():
    user_id = get_jwt_identity()['id']
    notebook_list = []
    data = QUERY.get_data(db=db, model=NoteBook, user_id=user_id)

    for values in data:
        notebook_list.append(noteBookSchema.dump(values))
    return jsonify(data=notebook_list)

# Retrieve Send data(NoteBook)


@notebook.get("/retrieve-notebook-member/<int:note_id>")
@jwt_required(refresh=True)
def retrieve_notebook_member(note_id):
    sent_request = 2
    retrieve_member = []
    get_member = db.session.query(
        NoteBookMember.id,
        RequestStatus.request_status_name,
        User.first_name, User.last_name,
        User.username).\
        join(NoteBook, NoteBookMember.notebook_id == NoteBook.id).\
        join(User, NoteBookMember.friend_id == User.id).\
        join(RequestStatus, NoteBookMember.request_status == RequestStatus.id).\
        filter(NoteBookMember.request_status == sent_request).\
        filter(NoteBookMember.notebook_id == note_id).all()

    for member in get_member:
        combine_member_data = user_schema.dump(
            member) | notebook_member_schema.dump(member)
        collect_all = combine_member_data | request_status_schema.dump(member)
        retrieve_member.append(collect_all)

    return jsonify(data=retrieve_member)


@notebook.put("/update")
@jwt_required(refresh=True)
def update_notebook():
    try:
        data = request.json
        if data['id'] == '':
            response_with(resp.INVALID_INPUT_422)
        notebook = db.session.query(NoteBook).filter(
            NoteBook.id == data['id']).one()
        notebook.name = data['name']
        notebook.description = data['description']
        notebook.updated_at = now
        db.session.commit()
        return jsonify({
            "code": APP_LABEL.label("success"),
            "message": APP_LABEL.label("Notebook updated with success")
        })
    except Exception:
        return response_with(resp.INVALID_INPUT_422)

# Invite Friend


@notebook.post("/invite-friend")
@jwt_required(refresh=True)
def add_friend_to_notebook():
    try:
        user_id = get_jwt_identity()['id']
        data = request.json | {"sender_id": user_id}
        check_friend = db.session.query(NoteBookMember).filter(
            NoteBookMember.notebook_id == data['notebook_id'],
            NoteBookMember.friend_id == data['friend_id']).first()

        if check_friend:
            return jsonify({
                "code": APP_LABEL.label("success"),
                "message": APP_LABEL.label("Request already sent")
            })

        QUERY.insert_data(db=db, table_data=NoteBookMember(**data))
        return jsonify({
            "code": "success",
            "message": "Request sent with success"
        })

    except Exception:
        return response_with(resp.INVALID_INPUT_422)


@notebook.get("/received-request")
@jwt_required(refresh=True)
def request_received():
    try:
        sent_request = 1
        received_request = []
        add_list = []
        user_id = get_jwt_identity()['id']
        request_ = db.session.query(
            NoteBookMember.id,
            NoteBookMember.sent_at,
            RequestStatus.request_status_name,
            User.first_name, User.last_name,
            NoteBook.notebook_name,
            User.username).\
            join(NoteBook, NoteBookMember.notebook_id == NoteBook.id).\
            join(User, NoteBookMember.sender_id == User.id).\
            join(RequestStatus, NoteBookMember.request_status == RequestStatus.id).\
            filter(NoteBookMember.request_status == REQUEST_SENT).\
            filter(NoteBookMember.friend_id == user_id).all()

        for member in request_:
            received_request.append({
                **user_schema.dump(member),
                **notebook_member_schema.dump(member),
                **request_status_schema.dump(member),
                **noteBookSchema.dump(member),
                **{"notification": "notebook"}
            })

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

        for member in get_request:
            add_list.append({
                **user_schema.dump(member),
                **group_member_schema.dump(member),
                **user_create_group_schema.dump(member),
                **request_status_schema.dump(member),
                **{"notification": "group"}
            })

        combine_both_list = received_request + add_list

        return jsonify(data=combine_both_list)

    except Exception:
        return response_with(resp.INVALID_INPUT_422)


@notebook.get("/request-sent")
@jwt_required(refresh=True)
def request_sent():
    try:
        sent_request = 1
        received_request = []
        user_id = get_jwt_identity()['id']
        request_received = db.session.query(
            NoteBookMember.id,
            NoteBookMember.sent_at,
            RequestStatus.request_status_name,
            User.first_name, User.last_name,
            NoteBook.notebook_name,
            User.username).\
            join(NoteBook, NoteBookMember.notebook_id == NoteBook.id).\
            join(User, NoteBookMember.friend_id == User.id).\
            join(RequestStatus, NoteBookMember.request_status == RequestStatus.id).\
            filter(NoteBookMember.request_status == sent_request).\
            filter(NoteBookMember.sender_id == user_id).all()

        for member in request_received:
            combine_member_data = user_schema.dump(
                member) | notebook_member_schema.dump(member)
            collect_all = combine_member_data | request_status_schema.dump(
                member) | noteBookSchema.dump(member)
            received_request.append(collect_all)

        return jsonify(data=received_request)

    except Exception:
        return response_with(resp.INVALID_INPUT_422)


@notebook.put("/confirm-reject-request")
@jwt_required(refresh=True)
def confirm_request():
    rejected = "rejected"
    accepted = "accepted"
    try:
        data = request.json
        print(data)
        if data['method'] == rejected:
            if data['notebook_member_id'] is None:
                return response_with(resp.INVALID_INPUT_422)
            else:
                notebook_member = db.session.query(NoteBookMember).filter(
                    NoteBookMember.id == data['notebook_member_id'],
                ).one()
                notebook_member.request_status = data['request_status']
                notebook_member.canceled_at = now
                db.session.commit()
                return jsonify({
                    "code": APP_LABEL.label("Alert"),
                    "message": APP_LABEL.label("Request canceled"),
                })

        if data['method'] == accepted:
            if data['notebook_member_id'] is None:
                return response_with(resp.INVALID_INPUT_422)
            else:
                notebook_member = db.session.query(NoteBookMember).filter(
                    NoteBookMember.id == data['notebook_member_id'],
                ).one()
                notebook_member.request_status = data['request_status']
                notebook_member.confirmed_at = now
                db.session.commit()
                return jsonify({
                    "code": APP_LABEL.label("success"),
                    "message": APP_LABEL.label("Congratulation! now you can view and exchange data in this notebook"),
                    "data": notebook_member_schema.dump(notebook_member)
                })

    except Exception as e:
        print(e)
        return response_with(resp.INVALID_FIELD_NAME_SENT_422)


@notebook.post("/link-dept-notebook-notebook-member")
@jwt_required(refresh=True)
def add_friend_to_dept_notebook():
    try:
        user_id = get_jwt_identity()['id']
        data = request.json | {"user_id": user_id}
        check_friend = db.session.query(DeptNoteBook).filter(
            DeptNoteBook.memeber_id == data['memeber_id']).first()

        if check_friend:
            return jsonify({
                "code": APP_LABEL.label("Alert"),
                "message": APP_LABEL.label("Already linked")
            })

        QUERY.insert_data(db=db, table_data=DeptNoteBook(**data))
        return jsonify({
            "code": "success",
            "message": "Friend linked with success."
        })

    except Exception:
        return response_with(resp.INVALID_INPUT_422)


@notebook.post("/link-loan-notebook-notebook-member")
@jwt_required(refresh=True)
def add_friend_to_loan_notebook():
    try:
        user_id = get_jwt_identity()['id']
        data = request.json | {"user_id": user_id}
        check_friend = db.session.query(LoanNoteBook).filter(
            LoanNoteBook.friend_id == data['friend_id']).first()

        if check_friend:
            return jsonify({
                "code": APP_LABEL.label("Alert"),
                "message": APP_LABEL.label("Already linked")
            })

        QUERY.insert_data(db=db, table_data=LoanNoteBook(**data))
        return jsonify({
            "code": "success",
            "message": "Friend linked with success."
        })

    except Exception:
        return response_with(resp.INVALID_INPUT_422)
