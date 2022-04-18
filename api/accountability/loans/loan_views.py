from datetime import date
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.accountability.global_amount.global_amount_views import QUERY
from sqlalchemy import extract, desc

from api.core.query import QueryGlobalRepport
from api.utils.responses import response_with
from api.utils import responses as resp
from api.utils.model_marsh import LoanNoteBookSchema, LoanSchema, UserSchema
from api.core.objects import ManageQuery
from api.core.labels import AppLabels

from ... import db
from api.database.models import LoanNoteBook, Loans, User
loans = Blueprint("loans", __name__,
                  url_prefix="/api/user/account/loans")

todays_date = date.today()
QUERY = QueryGlobalRepport()
manage_query = ManageQuery()
APP_LABEL = AppLabels()

# Register loans data && Record partners or (Lenders) to list 
loans_schema = LoanSchema()
loans_note_book_schame = LoanNoteBookSchema()

@loans.post("/add-partner-to-notebook")
@jwt_required()
def add_borrower_to_notebook():
    user_id = get_jwt_identity()['id']
    data = request.json | {"user_id": user_id}
    QUERY.insert_data(db=db, table_data=LoanNoteBook(**data))
    return jsonify({
        "code": "success",
        "message": "Partnert added with success"
    })


# Get all loans

@loans.get("/retrieve")
@jwt_required()
def user_get_loans():
    user_id = get_jwt_identity()['id']
    data = QUERY.get_data(db=db, model=LoanNoteBook, user_id=user_id)
    total_loan_amount = db.session.query(Loans).join(
        LoanNoteBook, Loans.note_id == LoanNoteBook.id, isouter=True
    ).filter(LoanNoteBook.user_id == user_id).all()
    
    loan_list = manage_query.serialize_schema(data, loans_note_book_schame)
    total_amount = manage_query.generate_total_amount(total_loan_amount, loans_schema)

    return jsonify(data={"loan_list": loan_list, "total_loan": total_amount} )

# Search for financial partener 

@loans.post("/search-user")
@jwt_required()
def search_user():
    user_schema = UserSchema(many=True)
    data = request.json["username"]
    if User.find_by_username(data.lower()):
        user = db.session.query(User.username, User.first_name, User.id,
                                User.last_name).filter_by(username=data.lower()).all()

        return jsonify(data=user_schema.dump(user))
    return jsonify(data="User not found!")

# Add loan
@loans.post("/add-loan/<int:note_id>")
@jwt_required()
def user_add_loan(note_id):
    # Generate inputs
    data = request.json | {"note_id": note_id}
    for value in data["data"]:
        if value["amount"] is None:
            return response_with(resp.INVALID_INPUT_422)
        else:
            QUERY.insert_data(db=db, table_data=Loans(
                **value | {"note_id": note_id}))

    return jsonify({
        "code": APP_LABEL.label("success"),
        "message": APP_LABEL.label("Loan Amount recorded with success")
    })

# Get saving by date
@loans.get("/retrieve-date/<int:loan_note_id>")
@jwt_required()
def get_loan_date(loan_note_id):
    data = Loans.query.filter_by(note_id=loan_note_id).\
        filter(extract('year', Loans.created_at) == todays_date.year).\
        filter(extract('month', Loans.created_at) ==
               todays_date.month).order_by(desc(Loans.created_at)).all()

    loan_list = manage_query.serialize_schema(data, loans_note_book_schame)
    total_amount = manage_query.generate_total_amount(loan_list, loans_schema)

    return jsonify(data={
        "loan_list": loan_list,
        "total_amount": total_amount,
        "today_date": todays_date,
    })
