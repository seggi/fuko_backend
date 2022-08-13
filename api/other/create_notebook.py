from datetime import datetime
from api.utils.model_marsh import NoteBookMemberSchema, NoteBookSchema, RequestStatusSchema, UserSchema
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.accountability.global_amount.global_amount_views import QUERY

from api.core.query import QueryGlobalReport
from api.utils.responses import response_with
from api.utils import responses as resp
from api.core.labels import AppLabels
from api.utils.model_marsh import NoteBookSchema

from .. import db
from api.database.models import NoteBook, NoteBookMember, RequestStatus, User

QUERY = QueryGlobalReport()
APP_LABEL = AppLabels()
now = datetime.now()

notebook = Blueprint("notebook", __name__,
                     url_prefix="/api/user/notebook")

user_schema = UserSchema()
noteBookSchema = NoteBookSchema()
notebook_member_schema = NoteBookMemberSchema()
request_status_schema = RequestStatusSchema()
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
    retrieve_member = []
    get_member = db.session.query(
        NoteBookMember.id,
        RequestStatus.request_status_name,
        User.first_name, User.last_name,
        User.username).\
        join(NoteBook, NoteBookMember.notebook_id == NoteBook.id).\
        join(User, NoteBookMember.friend_id == User.id).\
        join(RequestStatus, NoteBookMember.request_status == RequestStatus.id).\
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
            NoteBookMember.friend_id == data['friend_id'],
            NoteBookMember.request_status == data["request_status"]).first()

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
