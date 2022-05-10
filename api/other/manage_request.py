from datetime import datetime
from api.utils.model_marsh import NoteBookSchema
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.accountability.global_amount.global_amount_views import QUERY

from api.core.query import QueryGlobalRepport
from api.utils.responses import response_with
from api.utils import responses as resp
from api.core.labels import AppLabels
from api.core.firebase.firebase_request import send_firebase_request
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
        data = request.json | {"sender_id": user_id, "request_status" : 1}
        check_member = db.session.query(NoteBookMember).\
            filter(NoteBookMember.notebook_id == data['notebook_id']).\
            filter(NoteBookMember.friend_id == data['friend_id']).\
            first()
        
        if check_member:
            return jsonify({
                "code": APP_LABEL.label("Alert"),
                "message": APP_LABEL.label("Request already sent."),
                "firebase": send_firebase_request()
            })
            
        else:
            QUERY.insert_data(db=db, table_data=NoteBookMember(**data))
            return jsonify({
                "code": APP_LABEL.label("success"),
                "message": APP_LABEL.label("Resquest sent")
            })
    except Exception as e:
        print(e, "KKK")
        return response_with(resp.INVALID_INPUT_422) 



@manage_request.get("/retrieve-invitation") 
@jwt_required(refresh=True)
def retrieve_request():
    user_id = get_jwt_identity()['id']
    request_list = []
    retrieve_request = db.session.query(NoteBookMember.id,NoteBookMember.sent_at, NoteBook.notebook_name , 
        User.first_name, User.last_name,  RequestStatus.request_status_name,).\
        join(NoteBook, NoteBookMember.notebook_id  == NoteBook.id, isouter=True).\
            join(User, NoteBookMember.friend_id == User.id, isouter=True).\
                join(RequestStatus, NoteBookMember.request_status  == RequestStatus.id , isouter=True).\
                filter(NoteBookMember.sender_id == user_id).all()

                
    for request in retrieve_request:
        request_list.append({
            **noteBookMemberSchema.dump(request), 
            **requestStatusSchema.dump(request),
            **noteBookSchema.dump(request),
            **userSchema.dump(request)
        })
       
    return jsonify(data=request_list)


