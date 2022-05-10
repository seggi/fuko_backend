from datetime import datetime
from api.utils.model_marsh import NoteBookSchema
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import  desc
from api.accountability.global_amount.global_amount_views import QUERY

from api.core.query import QueryGlobalRepport
from api.utils.responses import response_with
from api.utils import responses as resp
from api.core.labels import AppLabels
from api.utils.model_marsh import NoteBookSchema, NoteBookMemberSchema, UserSchema, RequestStatusSchema


from .. import db
from api.database.models import NoteBook, NoteBookMember, RequestStatus, User


QUERY = QueryGlobalRepport()
APP_LABEL = AppLabels()
now = datetime.now()

manage_request = Blueprint("invite", __name__,
                  url_prefix="/api/user/manage_request")

noteBookMemberSchema = NoteBookMemberSchema()
noteBookSchema = NoteBookSchema()
userSchema = UserSchema()
requestStatusSchema = RequestStatusSchema()

request_status = {"sent" : 1, "accepted": 2, "rejected": 3, "expired": 4}

@manage_request.post("/invite-friend") 
@jwt_required(refresh=True)
def invite_friend():
    '''
        notebook_id,
        sender_id,
        friend_id,
        request_status = 1 (default)
    '''
    try:
        user_id = get_jwt_identity()['id']
        data = request.json | {"sender_id": user_id, "request_status" : request_status['sent']}
        check_member = db.session.query(NoteBookMember).\
            filter(NoteBookMember.notebook_id == data['notebook_id']).\
            filter(NoteBookMember.friend_id == data['friend_id']).\
            first()
        
        if check_member:
            return jsonify({
                "code": APP_LABEL.label("Alert"),
                "message": APP_LABEL.label("Request already sent."),
            })
            
        else:
            QUERY.insert_data(db=db, table_data=NoteBookMember(**data))
            return jsonify({
                "code": APP_LABEL.label("success"),
                "message": APP_LABEL.label("Resquest sent")
            })
    except Exception as e:
        return response_with(resp.INVALID_INPUT_422) 



@manage_request.get("/retrieve-invitation") 
@jwt_required(refresh=True)
def retrieve_invitation():
    user_id = get_jwt_identity()['id']
    request_list = []

    retrieve_request = db.session.query(NoteBookMember.id,NoteBookMember.sent_at, NoteBook.notebook_name , 
        User.first_name, User.last_name, User.username, RequestStatus.request_status_name,).\
        join(NoteBook, NoteBookMember.notebook_id  == NoteBook.id, isouter=True).\
            join(User, NoteBookMember.sender_id == User.id, isouter=True).\
                join(RequestStatus, NoteBookMember.request_status  == RequestStatus.id , isouter=True).\
                filter(NoteBookMember.friend_id == user_id).\
                    filter(NoteBookMember.request_status == request_status['sent']). \
                        order_by(desc(NoteBookMember.sent_at)).\
                        all()
                
    for request in retrieve_request:
        request_list.append({
            **noteBookMemberSchema.dump(request), 
            **requestStatusSchema.dump(request),
            **noteBookSchema.dump(request),
            **userSchema.dump(request)
        })
       
    return jsonify(data=request_list)

@manage_request.get("/retrieve-request") 
@jwt_required(refresh=True)
def retrieve_request():
    user_id = get_jwt_identity()['id']
    request_list = []
    retrieve_request = db.session.query(NoteBookMember.id,NoteBookMember.sent_at, NoteBook.notebook_name , 
        User.first_name, User.last_name,  RequestStatus.request_status_name,).\
        join(NoteBook, NoteBookMember.notebook_id  == NoteBook.id, isouter=True).\
            join(User, NoteBookMember.friend_id == User.id, isouter=True).\
                join(RequestStatus, NoteBookMember.request_status  == RequestStatus.id , isouter=True).\
                filter(NoteBookMember.sender_id == user_id).\
                    filter(NoteBookMember.request_status == request_status['sent']).\
                        order_by(desc(NoteBookMember.sent_at)).\
                        all()


                
    for request in retrieve_request:
        request_list.append({
            **noteBookMemberSchema.dump(request), 
            **requestStatusSchema.dump(request),
            **noteBookSchema.dump(request),
            **userSchema.dump(request)
        })
       
    return jsonify(data=request_list)


@manage_request.put("/response")
@jwt_required(refresh=True)
def update_notebook():
    try:
        data = request.json
        if data['id'] == '':
            response_with(resp.INVALID_INPUT_422)
        notebook_member = db.session.query(NoteBookMember).filter(NoteBookMember.id == data['id']).one()
        notebook_member.request_status = data['request_status'] 
        notebook_member.confirmed_at = now
        db.session.commit()
        return jsonify({
            "code": APP_LABEL.label("success"),
            "message": APP_LABEL.label("Request accepted!")
        })
    except Exception:
        return response_with(resp.INVALID_INPUT_422)

@manage_request.get("/retrieve-request-status") 
@jwt_required(refresh=True)
def retrieve_request_status():
    get_status  = db.session.query(RequestStatus).all()
    status_list =[]
    for status in get_status:
        status_list.append(requestStatusSchema.dump(status))
    return jsonify(data=status_list)
