from datetime import datetime
from api.utils.model_marsh import NoteBookSchema
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.accountability.global_amount.global_amount_views import QUERY

from api.core.query import QueryGlobalRepport
from api.utils.responses import response_with
from api.utils import responses as resp
from api.core.labels import AppLabels
from api.utils.model_marsh import NoteBookSchema


from .. import db
from api.database.models import NoteBook, NoteBookMember


QUERY = QueryGlobalRepport()
APP_LABEL = AppLabels()
now = datetime.now()

send_request = Blueprint("invite", __name__,
                  url_prefix="/api/user/account/send_request")

@send_request.post("/invite_friend") 
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
        data = request.json | {"user_id": user_id, "request_status" : 1}
        QUERY.insert_data(db=db, table_data=NoteBookMember(**data))
        return jsonify({
            "code": APP_LABEL.label("success"),
            "message": APP_LABEL.label("Resquest sent")
        })
    except Exception:
        return response_with(resp.INVALID_INPUT_422) 

