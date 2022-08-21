from datetime import date
from datetime import datetime
from dbm import dumb
from locale import currency
from threading import local
from api.auth.auth_views import refresh
from api.core.payment_manager import ComputePaymentAmount
from api.core.reducer import Reducer
from api.utils.constant import COMPUTE_SINGLE_AMOUNT
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import extract, desc

from api.accountability.global_amount.global_amount_views import QUERY
from api.core.query import QueryGlobalReport
from api.utils.responses import response_with
from api.utils import responses as resp
from api.utils.model_marsh import CurrencySchema, DeptNoteBookSchema, DeptPaymentSchema, DeptsSchema, LoanNoteBookSchema, LoanPaymentSchema, NoteBookMemberSchema, RecordDeptPaymentSchema, UserSchema
from api.core.labels import AppLabels
from api.core.objects import ManageQuery

from ... import db
from api.database.models import Currency, DeptNoteBook, Depts, DeptsPayment, LoanNoteBook, LoanPayment, NoteBookMember, RecordDeptPayment, User, RecordDeptPayment

dept = Blueprint("dept", __name__, url_prefix="/api/user/account/dept")

QUERY = QueryGlobalReport()
manage_query = ManageQuery()

# Register dept data && Record borrower to note book
# Get all dept

todays_date = date.today()
APP_LABEL = AppLabels()
dept_note_book_schema = DeptNoteBookSchema()
dept_schema = DeptsSchema()
user_schema = UserSchema()
currency_schema = CurrencySchema()
noteBook_Member_Schema = NoteBookMemberSchema()
dept_payment_schema = DeptPaymentSchema()
record_dept_payment_schema = RecordDeptPaymentSchema()
loan_payment_schema = LoanPaymentSchema()
loan_note_notebook_schema = LoanNoteBookSchema()
now = datetime.now()


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


@dept.get("/get-friend-from-dept-notebook")
@jwt_required(refresh=True)
def retrieve_members_from_dept_notebook():
    user_id = get_jwt_identity()['id']
    outside_friend = []

    get_friend_outside = db.session.query(DeptNoteBook.id, DeptNoteBook.borrower_name).\
        filter(DeptNoteBook.borrower_name != None).\
        filter(DeptNoteBook.user_id == user_id).\
        all()

    for member in get_friend_outside:
        outside_friend.append({
            **dept_note_book_schema.dump(member)
        })

    combine_all_list = outside_friend

    return jsonify(data=combine_all_list)


@dept.get("/friend-pub-dept-notebook")
@jwt_required(refresh=True)
def retrieve_members_from_pub_dept_notebook():
    user_id = get_jwt_identity()['id']
    member_in_dept_list = []

    get_member = db.session.query(
        DeptNoteBook,
        DeptNoteBook.id,
        User.username,
        User.first_name,
        User.last_name).\
        join(NoteBookMember, DeptNoteBook.memeber_id == NoteBookMember.id, isouter=True).\
        join(User, NoteBookMember.friend_id == User.id, isouter=True).\
        filter(DeptNoteBook.borrower_name == None).\
        filter(DeptNoteBook.user_id == user_id).\
        all()

    get_loan_member = db.session.query(
        LoanNoteBook,
        LoanNoteBook.id,).\
        join(NoteBookMember, LoanNoteBook.friend_id == NoteBookMember.id, isouter=True).\
        join(User, NoteBookMember.friend_id == User.id, isouter=True).\
        filter(LoanNoteBook.partner_name == None).\
        filter(LoanNoteBook.user_id == user_id).\
        all()

    for member in get_member:
        new_dict = {}
        for membership_id in get_loan_member:
            new_dict["loan_notebook_membership_id"] = membership_id['id']

        member_in_dept_list.append({
            **user_schema.dump(member),
            **noteBook_Member_Schema.dump(member),
            **new_dict
        })

    return jsonify(data=member_in_dept_list)


@dept.get("/retrieve/<int:currency_id>")
@jwt_required(refresh=True)
def user_get_dept(currency_id):
    user_id = get_jwt_identity()['id']
    dept_list = []
    currency = []
    total_dept_amount = db.session.query(Depts.amount, Currency.code).\
        join(Currency, Depts.currency_id == Currency.id, isouter=True).\
        filter(DeptNoteBook.user_id == user_id, Depts.currency_id == currency_id).order_by(
            desc(Depts.created_at)).all()

    for item in total_dept_amount:
        dept_data = dept_schema.dump(item) | currency_schema.dump(item)
        dept_list.append(dept_data)

    for dept in dept_list:
        currency.append(dept['code'])

    total_amount = manage_query.generate_total_amount(dept_list)

    return jsonify(data={
        "dept_list": dept_list,
        "total_dept": total_amount,
        "currency": currency[0] if len(currency) > 0 else ""})


@dept.get("/retrieve-friend-dept/<int:friend_id>/<int:currency_id>")
@jwt_required(refresh=True)
def retrieve_friend_dept(currency_id, friend_id):
    user_id = get_jwt_identity()['id']
    dept_list = []
    currency = []
    total_dept_amount = db.session.query(
        Depts.id, Depts.amount,
        Depts.description,
        Depts.created_at,
        Depts.payment_status,
        Currency.code).\
        join(Currency, Depts.currency_id == Currency.id, isouter=True).\
        join(DeptNoteBook, Depts.note_id == DeptNoteBook.id, isouter=True).\
        filter(
            DeptNoteBook.user_id == user_id,
            Depts.currency_id == currency_id,
            DeptNoteBook.id == friend_id).order_by(
            desc(Depts.created_at)).all()

    for item in total_dept_amount:
        dept_data = dept_schema.dump(item) | currency_schema.dump(item)
        dept_list.append(dept_data)

    for dept in dept_list:
        currency.append(dept['code'])

    total_amount = manage_query.generate_total_amount(dept_list)

    return jsonify(data={
        "dept_list": dept_list,
        "total_dept": total_amount,
        "currency": currency[0] if len(currency) > 0 else ""})

# Get dept by date


@dept.get("/retrieve-dept-by-current-date/<int:dept_note_id>")
@jwt_required(refresh=True)
def get_loan_by_current_date(dept_note_id):
    dept_list = []
    currency = []
    loan_data = Depts.query.filter_by(note_id=dept_note_id).\
        filter(extract('year', Depts.created_at) == todays_date.year).\
        filter(extract('month', Depts.created_at) ==
               todays_date.month).order_by(desc(Depts.created_at)).all()

    for item in loan_data:
        dept_data = dept_schema.dump(item) | currency_schema.dump(item)
        dept_list.append(dept_data)

    for expense_detail in dept_list:
        currency.append(expense_detail['code'])

    total_amount = manage_query.generate_total_amount(dept_list)

    return jsonify(data={
        "dept_list": dept_list,
        "total_amount": total_amount,
        "today_date": todays_date,
        "currency": currency[0] if len(currency) > 0 else ""
    })

# Add dept


@dept.post("/record-dept/<int:note_id>")
@jwt_required(refresh=True)
def user_add_dept(note_id):
    # Generate inputs
    try:
        request_data = request.json
        for data in request_data["data"]:
            QUERY.insert_data(db=db, table_data=Depts(
                **data | {"note_id": note_id}))
        return jsonify({
            "code": APP_LABEL.label("success"),
            "message": APP_LABEL.label("Dept Amount recorded with success")
        })

    except Exception:
        return response_with(resp.INVALID_INPUT_422)


# Pay dept
# @dept.post("/pay-borrowed-amount/<int:dept_id>")
# @jwt_required(refresh=True)
# def user_pay_dept(dept_id):
#     collect_payment_history = []
#     request_data = request.json | {"note_id": dept_id}

#     try:
#         if request_data['data']["amount"] is None:
#             return response_with(resp.INVALID_INPUT_422)

#         if request_data['method'] == COMPUTE_SINGLE_AMOUNT:
#             get_single_amount = db.session.query(Depts.amount, Depts.currency_id).\
#                 filter(Depts.currency_id == request_data['data']['currency_id']).\
#                 filter(Depts.payment_status == False).\
#                 filter(Depts.id == dept_id).first()

#             get_payment_history = db.session.query(DeptsPayment.amount).\
#                 filter(DeptsPayment.notebook_id == dept_id).all()

#             for amount in get_payment_history:
#                 collect_payment_history.append(float(amount['amount']))

#             get_total_paid_amount = sum(collect_payment_history)

#             for amount in get_single_amount:
#                 get_dept = amount - get_total_paid_amount

#                 if request_data['data']["amount"] <= amount and get_total_paid_amount <= amount and \
#                         request_data['data']['amount'] <= get_dept:
#                     data = {
#                         **request_data['data'],
#                         **{"dept_id": dept_id},
#                         **{"budget_category_id": 7},
#                         **{"budget_option_id": 2}
#                     }
#                     QUERY.insert_data(db=db, table_data=DeptsPayment(**data))
#                     return jsonify({
#                         "code": APP_LABEL.label("success"),
#                         "message": APP_LABEL.label("You come to pay part of the dept."),
#                     })
#                 if get_total_paid_amount == amount:
#                     loan = db.session.query(Depts).filter(
#                         Depts.id == dept_id).one()
#                     loan.payment_status = True
#                     db.session.commit()
#                     return jsonify({
#                         "code": APP_LABEL.label("success"),
#                         "message": APP_LABEL.label("Congratulation you paid all the amount.")
#                     })
#                 else:
#                     return jsonify(message=APP_LABEL.label(
#                         APP_LABEL.label(f"""You try to pay much money...,the dept is {get_dept} . If you know what you are doing. please use pay multiple depts""")))

#         else:
#             return jsonify(data="Please pay by selecting multiple.")

#     except Exception as e:
#         return response_with(resp.INVALID_INPUT_422)


# @dept.post("/pay-multiple-depts")
# @jwt_required(refresh=True)
# def pay_multiple_dept():
#     request_data = request.json
#     try:
#         for data in request_data:
#             get_dept = db.session.query(DeptsPayment).\
#                 filter(DeptsPayment.notebook_id == data['dept_id']).\
#                 filter(DeptsPayment.description == data['description']).first()
#             if get_dept:
#                 return jsonify({
#                     "code": APP_LABEL.label("Alert"),
#                     "message": APP_LABEL.label("Amount can't be applied twice."),
#                 })
#             QUERY.insert_data(db=db, table_data=DeptsPayment(**data))
#             dept = db.session.query(Depts).filter(
#                 Depts.id == data['dept_id']).one()
#             dept.payment_status = True
#             db.session.commit()

#         return jsonify({
#             "code": APP_LABEL.label("success"),
#             "message": APP_LABEL.label("You come to complete some depts."),
#         })
#     except Exception:
#         return response_with(resp.INVALID_INPUT_422)

# To be kept
# Dept payment


@dept.post("/pay-many-dept")
@jwt_required(refresh=True)
def pay_many_dept():
    # amount
    request_data = request.json
    try:
        for data in request_data:
            QUERY.insert_data(db=db, table_data=RecordDeptPayment(**data))
            return jsonify({
                "code": APP_LABEL.label("success"),
                "message": APP_LABEL.label(f"Amount saved with success."),
            })

    except Exception:
        return response_with(resp.INVALID_INPUT_422)


@dept.get("/retrieved-paid-amount/<int:note_id>/<int:loan_membership_id>/<int:currency_id>")
@jwt_required(refresh=True)
def retrieve_payment_recorded(note_id, currency_id, loan_membership_id):
    user_id = get_jwt_identity()['id']
    collect_payment_history_dept = []
    get_amount_dept = []
    currency = []

    collect_payment_history_loan = []
    get_amount_loan = []
    currency = []

    paid_dept_amount = db.session.query(
        RecordDeptPayment.description,
        RecordDeptPayment.amount,
        RecordDeptPayment.created_at,
        Currency.code).\
        join(Currency, RecordDeptPayment.currency_id == Currency.id).\
        filter(RecordDeptPayment.currency_id == currency_id).\
        filter(RecordDeptPayment.note_id == note_id).order_by(
            desc(RecordDeptPayment.created_at)).all()

    for amount in paid_dept_amount:
        get_all_amount = record_dept_payment_schema.dump(
            amount) | currency_schema.dump(amount)
        if loan_membership_id != 0:
            bind_auth = get_all_amount | {"username": "You"}
            collect_payment_history_dept.append(bind_auth)
            get_amount_dept.append(float(amount['amount']))
            currency.append(amount['code'])

        collect_payment_history_dept.append(get_all_amount)
        get_amount_dept.append(float(amount['amount']))
        currency.append(amount['code'])

    if loan_membership_id != 0:
        paid_loan_amount = db.session.query(
            LoanPayment.description,
            LoanPayment.amount,
            LoanPayment.created_at,
            User.username,
            Currency.code).\
            join(Currency, LoanPayment.currency_id == Currency.id).\
            join(LoanNoteBook, LoanPayment.notebook_id == LoanNoteBook.id).\
            join(User, LoanNoteBook.user_id == User.id).\
            filter(LoanPayment.currency_id == currency_id).\
            filter(LoanNoteBook.user_id == user_id).order_by(
                desc(LoanPayment.created_at)).all()

        for amount in paid_loan_amount:
            get_all_amount = loan_payment_schema.dump(
                amount) | currency_schema.dump(amount)
            bind_auth = get_all_amount | user_schema.dump(amount)
            collect_payment_history_loan.append(bind_auth)
            get_amount_loan.append(float(amount['amount']))
            currency.append(amount['code'])

    get_total_paid_loan = sum(get_amount_dept)
    get_total_paid_dept = sum(get_amount_loan)

    get_total_paid_amount = get_total_paid_loan + get_total_paid_dept
    collect_payment_history = collect_payment_history_loan + collect_payment_history_dept

    return jsonify(data={
        "payment_history": collect_payment_history,
        "currency": currency[0] if len(currency) > 0 else "",
        "paid_amount": get_total_paid_amount,
    })


#! To be changed

# @ dept.get("/retrieve-paid-amount/<int:currency_id>/<int:notebook_id>")
# @ jwt_required(refresh=True)
# def retrieve_payment_dept(notebook_id, currency_id):
#     user_id = get_jwt_identity()['id']
#     currency = []
#     get_status = []
#     payment_history_list = []
#     collect_payment_history = []

#     collect_payment_history = []
#     get_amount = []
#     currency = []

#     get_payment_history = db.session.query(
#         DeptsPayment.amount,
#         DeptsPayment.created_at,
#         DeptsPayment.description,
#         Currency.code,
#     ).\
#         join(Currency, DeptsPayment.currency_id == Currency.id).\
#         filter(DeptsPayment.currency_id == currency_id).\
#         filter(DeptsPayment.notebook_id == notebook_id).all()

#     paid_amount = db.session.query(
#         LoanPayment.description,
#         LoanPayment.amount,
#         LoanPayment.created_at,
#         Currency.code).\
#         join(Currency, LoanPayment.currency_id == Currency.id).\
#         join(LoanNoteBook, LoanPayment.notebook_id == LoanNoteBook.id).\
#         filter(LoanPayment.currency_id == currency_id).\
#         filter(LoanNoteBook.user_id == 2).order_by(
#             desc(LoanPayment.created_at)).all()

#     for amount in paid_amount:
#         get_all_amount = LoanPaymentSchema.dump(
#             amount) | currency_schema.dump(amount)
#         collect_payment_history.append(get_all_amount)
#         get_amount.append(float(amount['amount']))
#         currency.append(amount['code'])

#     for amount in get_payment_history:
#         payment_history_list.append(dept_payment_schema.dump(amount))
#         collect_payment_history.append(float(amount['amount']))
#         currency.append(amount['code'])

#     get_total_paid_loan = sum(get_amount)

#     get_total_paid_dept = sum(collect_payment_history)

#     get_total_paid_amount = get_total_paid_loan + get_total_paid_dept

#     return jsonify(data={
#         "payment_history": collect_payment_history,
#         "currency": currency[0] if len(currency) > 0 else "",
#         "paid_amount": get_total_paid_amount,
#     })
