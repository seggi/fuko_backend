from datetime import date
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.accountability.global_amount.global_amount_views import QUERY
from sqlalchemy import extract, desc, and_, func

from api.core.query import QueryGlobalRepport
from api.utils.responses import response_with
from api.utils import responses as resp
from api.utils.model_marsh import LoanNoteBookSchema, LoanSchema, NoteBookMemberSchema, UserSchema
from api.core.objects import ManageQuery
from api.core.labels import AppLabels

from ... import db
from api.database.models import LoanNoteBook, Loans, NoteBookMember, User
loans = Blueprint("loans", __name__,
                  url_prefix="/api/user/account/loans")

todays_date = date.today()
QUERY = QueryGlobalRepport()
manage_query = ManageQuery()
APP_LABEL = AppLabels()

# Register loans data && Record partners or (Lenders) to list 
loans_schema = LoanSchema()
userSchema = UserSchema()
loans_note_book_schema = LoanNoteBookSchema()
noteBook_Member_Schema = NoteBookMemberSchema()

# Invite Friend
@loans.post("/add-partner-to-notebook")
@jwt_required(refresh=True)
def invite_friend_to_notebook():
    user_id = get_jwt_identity()['id']
    data = request.json | {"user_id": user_id}
    QUERY.insert_data(db=db, table_data=LoanNoteBook(**data))
    return jsonify({
        "code": APP_LABEL.label("success"),
        "message": APP_LABEL.label("Friend added with success")
    })

# Add People
# No from fuko
@loans.post("/add-people-notebook")
@jwt_required(refresh=True)
def add_borrower_to_notebook():
    user_id = get_jwt_identity()['id']
    data = request.json | {"user_id": user_id}
    QUERY.insert_data(db=db, table_data=LoanNoteBook(**data))
    return jsonify({
        "code": APP_LABEL.label("success"),
        "message": APP_LABEL.label("Friend added with success")
    })

@loans.get("/get-friend-from-loan-notebook") 
@jwt_required(refresh=True)
def retrieve_members_in_loan_notebook():
    user_id = get_jwt_identity()['id']
    member_in_loan_list =[]
    outside_friend = []
    get_member  = db.session.query(LoanNoteBook, NoteBookMember.id, User.username).\
        join(NoteBookMember, LoanNoteBook.friend_id == NoteBookMember.id, isouter=True).\
            join(User, NoteBookMember.friend_id == User.id, isouter=True).\
                filter(LoanNoteBook.partner_name == None ).\
                filter(LoanNoteBook.user_id == user_id ).\
                all()
    get_friend_outside = db.session.query(LoanNoteBook.id, LoanNoteBook.partner_name).\
        filter(LoanNoteBook.partner_name != None ).\
        filter(LoanNoteBook.user_id == user_id ).\
        all()

    for member in get_friend_outside:
        outside_friend.append({
            **loans_note_book_schema.dump(member)
            })
    
    for member in get_member:
        member_in_loan_list.append({
            **userSchema.dump(member),
            **noteBook_Member_Schema.dump(member)
            })

    combine_all_list = member_in_loan_list + outside_friend

    return jsonify(data=combine_all_list)

# Get all loans

@loans.get("/retrieve")
@jwt_required(refresh=True)
def user_get_loans():
    user_id = get_jwt_identity()['id']
    loan_list = []
    total_loan_amount_list = []
    loan_data = QUERY.get_data(db=db, model=LoanNoteBook, user_id=user_id)
    total_loan_amount = db.session.query(Loans).join(
        LoanNoteBook, Loans.note_id == LoanNoteBook.id, isouter=True
    ).filter(LoanNoteBook.user_id == user_id).order_by(desc(Loans.created_at)).all()

    for item in loan_data:
        loan_list.append(loans_schema.dump(item))

    for item in total_loan_amount:
        total_loan_amount_list.append(loans_schema.dump(item))
    
    total_amount = manage_query.generate_total_amount(total_loan_amount_list)

    return jsonify(data={"loan_list": loan_list, "total_loan": total_amount} )

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

# Get loan by date
@loans.get("/retrieve-by-current-date/<int:loan_note_id>")
@jwt_required(refresh=True)
def get_loan_by_current_date(loan_note_id):
    loan_list = []
    loan_data = Loans.query.filter_by(note_id=loan_note_id).\
        filter(extract('year', Loans.created_at) == todays_date.year).\
        filter(extract('month', Loans.created_at) ==
               todays_date.month).order_by(desc(Loans.created_at)).all()

    for item in loan_data:
        loan_list.append(loans_schema.dump(item))

    total_amount = manage_query.generate_total_amount(loan_list)

    return jsonify(data={
        "loan_list": loan_list,
        "total_amount": total_amount,
        "today_date": todays_date,
    })

# Get loan by selected date
@loans.post("/retrieve")
@jwt_required(refresh=True)
def get_dept_by_date(loan_note_id):
    try:
        inputs =  request.json 
        loan_list = []
        loan_data = Loans.query.filter_by(note_id=loan_note_id).\
            filter(extract('year', Loans.created_at) == inputs['year']).\
            filter(extract('month', Loans.created_at) == inputs['month']).\
                order_by(desc(Loans.created_at)).all()

        for item in loan_data:
            loan_list.append(loans_schema.dump(item))
            
        total_amount = manage_query.generate_total_amount(loan_list)

        return jsonify(data={
            "loan_list": loan_list,
            "total_amount": total_amount
        })
    except Exception:
        return response_with(resp.INVALID_INPUT_422)

