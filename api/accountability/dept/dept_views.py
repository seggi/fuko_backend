from datetime import date
from api.auth.auth_views import refresh
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import extract, desc

from api.accountability.global_amount.global_amount_views import QUERY
from api.core.query import QueryGlobalRepport
from api.utils.responses import response_with
from api.utils import responses as resp
from api.utils.model_marsh import DeptNoteBookSchema, DeptsSchema, UserSchema
from api.core.labels import AppLabels
from api.core.objects import ManageQuery

from ... import db
from api.database.models import DeptNoteBook, Depts

dept = Blueprint("dept",__name__, url_prefix="/api/user/account/dept")

QUERY = QueryGlobalRepport()
manage_query = ManageQuery()

# Register dept data && Record borrower to note book
# Get all dept

todays_date = date.today()
APP_LABEL = AppLabels()
dept_note_book_schema = DeptNoteBookSchema()
dept_schema = DeptsSchema()

# Invite Friend
@dept.post("/add-borrower-to-notebook")
@jwt_required(refresh=True)
def add_friend_to_notebook():
    user_id = get_jwt_identity()['id']
    data = request.json | {"user_id": user_id}
    QUERY.insert_data(db=db, table_data=DeptNoteBook(**data))
    return jsonify({
        "code": "success",
        "message": "Borrower added with success"
    })

# Add People
# No from fuko
@dept.post("/add-people-notebook")
@jwt_required(refresh=True)
def add_borrower_to_notebook():
    user_id = get_jwt_identity()['id']
    data = request.json | {"user_id": user_id}
    QUERY.insert_data(db=db, table_data=DeptNoteBook(**data))
    return jsonify({
        "code": APP_LABEL.label("success"),
        "message": APP_LABEL.label("Friend added with success")
    })



@dept.get("/retrieve")
@jwt_required(refresh=True)
def user_get_dept():
    user_id = get_jwt_identity()['id']
    dept_list = []

    total_dept_amount = db.session.query(Depts).join(
        DeptNoteBook, Depts.note_id == DeptNoteBook.id, isouter=True).\
        filter(DeptNoteBook.user_id == user_id).order_by(desc(Depts.created_at)).all()

    for item in total_dept_amount:
        dept_list.append(dept_schema.dump(item))

    total_amount = manage_query.generate_total_amount(dept_list)
    
    return jsonify(data={"dept_list": dept_list, "total_dept": total_amount})


# Add dept
@dept.post("/add-dept/<int:note_id>")
@jwt_required()
def user_add_dept(note_id):
    # Generate inputs
    data = request.json | {"note_id": note_id}
    for value in data["data"]:
        if value['amount'] is None:
            return response_with(resp.INVALID_INPUT_422)
        else:
            QUERY.insert_data(db=db, table_data=Depts(
                **value | {"note_id": note_id}))

    return jsonify({
        "code": APP_LABEL.label("success"),
        "message": APP_LABEL.label("Dept Amount recorded with success")
    })

# Get saving by date
@dept.get("/retrieve-date/<int:dept_note_id>")
@jwt_required()
def get_dept_date(dept_note_id):
    data = Depts.query.filter_by(note_id=dept_note_id).\
        filter(extract('year', Depts.created_at) == todays_date.year).\
        filter(extract('month', Depts.created_at) ==
               todays_date.month).order_by(desc(Depts.created_at)).all()

    dept_list = manage_query.serialize_schema(data, dept_note_book_schema)
    total_amount = manage_query.generate_total_amount(dept_list, dept_schema)

    return jsonify(data={
        "dept_list": dept_list,
        "total_amount": total_amount,
        "today_date": todays_date,
    })

# Get saving by selected date
@dept.post("/retrieve-dept-date/<int:dept_note_id>")
@jwt_required(refresh=True)
def get_dept_by_date(dept_note_id):
    inputs =  request.json 
    loan_list = []
    depts_data = Depts.query.filter_by(note_id=dept_note_id).\
        filter(Depts.created_at <= inputs['date_one']).\
        filter(Depts.created_at >= inputs['date_two']).order_by(desc(Depts.created_at)).all()

    for item in depts_data:
            loan_list.append(dept_schema.dump(item))
    total_amount = manage_query.generate_total_amount(loan_list)

    return jsonify(data={
        "dept_list": loan_list,
        "total_amount": total_amount,
    })
