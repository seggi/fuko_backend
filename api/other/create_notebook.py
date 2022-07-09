from datetime import datetime
from api.utils.model_marsh import NoteBookSchema
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.accountability.global_amount.global_amount_views import QUERY

from api.core.query import QueryGlobalReport
from api.utils.responses import response_with
from api.utils import responses as resp
from api.core.labels import AppLabels
from api.utils.model_marsh import NoteBookSchema

from .. import db
from api.database.models import NoteBook

QUERY = QueryGlobalReport()
APP_LABEL = AppLabels()
now = datetime.now()

notebook = Blueprint("notebook", __name__,
                     url_prefix="/api/user/notebook")

noteBookSchema = NoteBookSchema()

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
