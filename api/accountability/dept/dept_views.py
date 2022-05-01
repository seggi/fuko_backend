from datetime import date
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
from api.database.models import DeptNoteBook, Depts, User
dept = Blueprint("dept", __name__,
                 url_prefix="/api/user/account/dept")


QUERY = QueryGlobalRepport()
manage_query = ManageQuery()

# Register dept data && Record borrower to note book
# Get all dept

todays_date = date.today()
APP_LABEL = AppLabels()
dept_note_book_schema = DeptNoteBookSchema()
dept_schema = DeptsSchema()


@dept.post("/add-borrower-to-notebook")
@jwt_required()
def add_borrower_to_notebook():
    user_id = get_jwt_identity()['id']
    data = request.json | {"user_id": user_id}
    QUERY.insert_data(db=db, table_data=DeptNoteBook(**data))
    return jsonify({
        "code": "success",
        "message": "Borrower added with success"
    })

# Search User to be removed

@dept.post("/search-user")
@jwt_required(refresh=True)
def search_user():
    user_schema = UserSchema(many=True)
    data = request.json["username"]
    if User.find_by_username(data.lower()):
        user = db.session.query(User.username, User.first_name, User.id,
                                User.last_name).filter_by(username=data.lower()).all()
        return jsonify(data=user_schema.dump(user))

    if User.find_by_username(data):
        user = db.session.query(User.username, User.first_name, User.id,
                                User.last_name).filter_by(username=data).all()
        return jsonify(data=user_schema.dump(user))
    return jsonify(data="User not found!")


@dept.get("/retrieve")
@jwt_required()
def user_get_dept():
    user_id = get_jwt_identity()['id']
    dept_list = []
    borrower_list = QUERY.get_data(db=db, model=DeptNoteBook, user_id=user_id)
    total_dept_amount = db.session.query(Depts).join(
        DeptNoteBook, Depts.note_id == DeptNoteBook.id, isouter=True).\
        filter(DeptNoteBook.user_id == user_id).all()

    dept_list = manage_query.serialize_schema(borrower_list, dept_note_book_schema)
    total_amount = manage_query.generate_total_amount(total_dept_amount, dept_schema)
    
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
    data = Depts.query.filter_by(note_id=dept_note_id).\
        filter(Depts.created_at <= inputs['date_one']).\
        filter(Depts.created_at >= inputs['date_two'])

    dept_list = manage_query.serialize_schema(data, dept_note_book_schema)
    total_amount = manage_query.generate_total_amount(dept_list, dept_schema)

    return jsonify(data={
        "dept_list": dept_list,
        "total_amount": total_amount,
    })
