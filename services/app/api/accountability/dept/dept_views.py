from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.accountability.global_amount.global_amount_views import QUERY

from api.core.query import QueryGlobalRepport
from api.utils.responses import response_with
from api.utils import responses as resp
from api.utils.model_marsh import DeptNoteBookSchema, DeptsSchema

from ... import db
from api.database.models import DeptNoteBook, Depts, User
dept = Blueprint("dept", __name__,
                 url_prefix="/api/user/account/dept")

QUERY = QueryGlobalRepport()

# Register dept data && Record borrower to note book
# Get all dept


@dept.post("/add-borrower-to-notebook")
@jwt_required()
def add_borrower_to_notebook():
    user_id = get_jwt_identity()
    data = request.json | {"user_id": user_id['id']}
    QUERY.insert_data(db=db, table_data=DeptNoteBook(**data))
    return jsonify({
        "code": "success",
        "message": "Amount saved with success"
    })


@dept.get("/retrieve")
@jwt_required()
def user_get_dept():
    user_id = get_jwt_identity()['id']
    item_list = []
    total_amount_list = []
    total_dept = []
    dept_list = []
    dept_schema = DeptsSchema()
    dept_note_book_schema = DeptNoteBookSchema()
    borrower_list = QUERY.get_data(db=db, model=DeptNoteBook, user_id=user_id)
    total_dept_amount = db.session.query(Depts).join(
        DeptNoteBook, Depts.note_id == DeptNoteBook.id, isouter=True).\
        filter(DeptNoteBook.user_id == user_id).all()

    for item in borrower_list:
        item_list.append(dept_schema.dump(item))

    for item in borrower_list:
        dept_list.append(dept_note_book_schema.dump(item))

    for item in total_dept_amount:
        total_amount_list.append(dept_schema.dump(item))

    for item in total_amount_list:
        total_dept.append(item['amount'])

    return jsonify(data={"dept_list": item_list, "total_dept": total_dept})


@dept.post("/add-dept")
@jwt_required()
def user_add_dept():
    # Generate inputs
    data = request.json
    if data["amount"] is None:
        return response_with(resp.INVALID_INPUT_422)
    else:
        QUERY.insert_data(db=db, table_data=Depts(**data))
    return jsonify({
        "code": "success",
        "message": "Amount saved with success"
    })


# Get saving by date
@dept.get("/retrieve-date/<int:user_id>")
@jwt_required()
def get_dept_date(user_id):
    data = request.json | {"user_id": user_id}
    pass
