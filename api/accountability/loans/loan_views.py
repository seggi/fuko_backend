from datetime import date
from datetime import datetime
from api.utils.constant import COMPUTE_SINGLE_AMOUNT
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.accountability.global_amount.global_amount_views import QUERY
from sqlalchemy import extract, desc

from api.core.query import QueryGlobalReport
from api.utils.responses import response_with
from api.utils import responses as resp
from api.utils.model_marsh import CurrencySchema, LoanNoteBookSchema, LoanPaymentSchema, LoanSchema, NoteBookMemberSchema, UserSchema
from api.core.objects import ManageQuery
from api.core.labels import AppLabels

from ... import db
from api.database.models import Currency, LoanNoteBook, LoanPayment, Loans, NoteBookMember, User

loans = Blueprint("loans", __name__,  url_prefix="/api/user/account/loans")

todays_date = date.today()
QUERY = QueryGlobalReport()
manage_query = ManageQuery()
APP_LABEL = AppLabels()
now = datetime.now()

# Register loans data && Record partners or (Lenders) to list
loans_schema = LoanSchema()
userSchema = UserSchema()
loans_note_book_schema = LoanNoteBookSchema()
noteBook_Member_Schema = NoteBookMemberSchema()
loan_payment_schema = LoanPaymentSchema()
currency_schema = CurrencySchema()

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
def add_lent_to_notebook():
    try:
        user_id = get_jwt_identity()['id']
        data = request.json | {"user_id": user_id}
        QUERY.insert_data(db=db, table_data=LoanNoteBook(**data))
        return jsonify({
            "code": APP_LABEL.label("success"),
            "message": APP_LABEL.label("Name created with success")
        })
    except Exception:
        return response_with(resp.INVALID_INPUT_422)


@loans.get("/personal-loan-notebook")
@jwt_required(refresh=True)
def retrieve_members_from_loan_notebook():
    user_id = get_jwt_identity()['id']
    member_in_loan_list = []
    outside_friend = []
    get_member = db.session.query(LoanNoteBook, NoteBookMember.id, User.username).\
        join(NoteBookMember, LoanNoteBook.friend_id == NoteBookMember.id, isouter=True).\
        join(User, NoteBookMember.friend_id == User.id, isouter=True).\
        filter(LoanNoteBook.partner_name == None).\
        filter(LoanNoteBook.user_id == user_id).\
        all()

    get_friend_outside = db.session.query(LoanNoteBook.id, LoanNoteBook.partner_name).\
        filter(LoanNoteBook.partner_name != None).\
        filter(LoanNoteBook.user_id == user_id).\
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


@loans.get("/pub-loan-notebook")
@jwt_required(refresh=True)
def pub_loan_notebook():
    user_id = get_jwt_identity()['id']
    member_in_loan_list = []
    outside_friend = []
    get_member = db.session.query(LoanNoteBook, NoteBookMember.id, User.username).\
        join(NoteBookMember, LoanNoteBook.friend_id == NoteBookMember.id, isouter=True).\
        join(User, NoteBookMember.friend_id == User.id, isouter=True).\
        filter(LoanNoteBook.partner_name == None).\
        filter(LoanNoteBook.user_id == user_id).\
        all()

    for member in get_member:
        member_in_loan_list.append({
            **userSchema.dump(member),
            **noteBook_Member_Schema.dump(member)
        })

    combine_all_list = member_in_loan_list + outside_friend

    return jsonify(data=combine_all_list)

# Get all loans


@loans.get("/retrieve/<int:currency_id>")
@jwt_required(refresh=True)
def user_get_loans(currency_id):
    try:
        user_id = get_jwt_identity()['id']
        loan_list = []
        currency = []
        total_loan_amount = db.session.query(Loans.amount, Currency.code).\
            join(Currency, Loans.currency_id == Currency.id, isouter=True).\
            join(LoanNoteBook, Loans.note_id == LoanNoteBook.id).\
            filter(
                LoanNoteBook.user_id == user_id,
                Loans.currency_id == currency_id
        ).order_by(
                desc(Loans.created_at)).all()

        for item in total_loan_amount:
            loans_data = loans_schema.dump(item) | currency_schema.dump(item)
            loan_list.append(loans_data)

        for loan in loan_list:
            currency.append(loan['code'])

        total_amount = manage_query.generate_total_amount(loan_list)

        return jsonify(data={
            "loan_list": loan_list,
            "total_loan": total_amount,
            "currency": currency[0] if len(currency) > 0 else ""
        })
    except Exception:
        return response_with(resp.INVALID_INPUT_422)

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

# Add loan


@loans.post("/record-loan/<int:note_id>")
@jwt_required(refresh=True)
def user_record_loan(note_id):
    # Generate inputs
    try:
        data = request.json | {"note_id": note_id}
        for value in data["data"]:
            if value["amount"] is None:
                return response_with(resp.INVALID_INPUT_422)
            else:
                if value["recieve_money_at"] == "":
                    received_at = {"recieve_money_at": now}
                    QUERY.insert_data(db=db, table_data=Loans(
                        **value | {"note_id": note_id, **received_at}))
                    return jsonify({
                        "code": APP_LABEL.label("success"),
                        "message": APP_LABEL.label("Loan Amount recorded with success")
                    })
                else:
                    QUERY.insert_data(db=db, table_data=Loans(
                        **value | {"note_id": note_id}))
                    return jsonify({
                        "code": APP_LABEL.label("success"),
                        "message": APP_LABEL.label("Loan Amount recorded with success")
                    })

    except Exception:
        return response_with(resp.INVALID_INPUT_422)

# Update loan


@loans.put("/update-loan/<int:loan_id>")
@jwt_required(refresh=True)
def user_update_loan(loan_id):
    # Generate inputs
    try:
        data = request.json
        if data["amount"] is None or data["currency_id"] is None:
            return response_with(resp.INVALID_INPUT_422)
        else:
            loan = db.session.query(Loans).filter(Loans.id == loan_id).one()
            loan.description = data['description']
            loan.recieve_money_at = data['recieve_money_at']
            loan.currency_id = data['currency_id']
            loan.update_at = now
            db.session.commit()
            return jsonify({
                "code": APP_LABEL.label("success"),
                "message": APP_LABEL.label("Loan Amount updated with success")
            })

    except Exception:
        return response_with(resp.INVALID_INPUT_422)

# Pay loan


@loans.post("/pay-borrowed-amount/<int:loan_id>")
@jwt_required(refresh=True)
def user_pay_loan(loan_id):
    collect_payment_history = []
    request_data = request.json | {"note_id": loan_id}

    try:
        if request_data['data']["amount"] is None:
            return response_with(resp.INVALID_INPUT_422)

        if request_data['method'] == COMPUTE_SINGLE_AMOUNT:
            get_single_amount = db.session.query(Loans.amount, Loans.currency_id).\
                filter(Loans.currency_id == request_data['data']['currency_id']).\
                filter(Loans.payment_status == False).\
                filter(Loans.id == loan_id).first()

            get_payment_history = db.session.query(LoanPayment.amount).\
                filter(LoanPayment.loan_id == loan_id).all()

            for amount in get_payment_history:
                collect_payment_history.append(float(amount['amount']))

            get_total_paid_amount = sum(collect_payment_history)

            for amount in get_single_amount:
                get_dept = amount - get_total_paid_amount

                if request_data['data']["amount"] <= amount and get_total_paid_amount <= amount and \
                        request_data['data']['amount'] <= get_dept:
                    data = {**request_data['data'], **{"loan_id": loan_id}}
                    QUERY.insert_data(db=db, table_data=LoanPayment(**data))
                    return jsonify({
                        "code": APP_LABEL.label("success"),
                        "message": APP_LABEL.label("You come to pay part of the dept."),
                    })
                if get_total_paid_amount == amount:
                    loan = db.session.query(Loans).filter(
                        Loans.id == loan_id).one()
                    loan.payment_status = True
                    db.session.commit()
                    return jsonify({
                        "code": APP_LABEL.label("success"),
                        "message": APP_LABEL.label("Congratulation you paid to all this amount.")
                    })
                else:
                    return jsonify(message=APP_LABEL.label(
                        APP_LABEL.label(f"""You try pay much money...,the dept is {get_dept} . If you know what you are doing. please use pay multiple depts""")))

        else:
            return jsonify(data="Pease pay by selecting multiple.")

    except Exception:
        return response_with(resp.INVALID_INPUT_422)


@loans.post("/pay-multiple-depts")
@jwt_required(refresh=True)
def pay_multiple_loan():
    request_data = request.json
    try:
        for data in request_data:
            get_dept = db.session.query(LoanPayment).\
                filter(LoanPayment.loan_id == data['loan_id']).\
                filter(LoanPayment.description == data['description']).first()
            if get_dept:
                return jsonify({
                    "code": APP_LABEL.label("Alert"),
                    "message": APP_LABEL.label("Amount can't be applied twice."),
                })
            QUERY.insert_data(db=db, table_data=LoanPayment(**data))
            loan = db.session.query(Loans).filter(
                Loans.id == data['loan_id']).one()
            loan.payment_status = True
            db.session.commit()

        return jsonify({
            "code": APP_LABEL.label("success"),
            "message": APP_LABEL.label("You come complete some depts."),
        })
    except Exception:
        return response_with(resp.INVALID_INPUT_422)
