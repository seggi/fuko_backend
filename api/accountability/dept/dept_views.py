from datetime import date
from datetime import datetime
from api.auth.auth_views import refresh
from api.utils.constant import COMPUTE_SIMGLE_AMOUNT
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import extract, desc

from api.accountability.global_amount.global_amount_views import QUERY
from api.core.query import QueryGlobalReport
from api.utils.responses import response_with
from api.utils import responses as resp
from api.utils.model_marsh import DeptNoteBookSchema, DeptsSchema, NoteBookMemberSchema, UserSchema
from api.core.labels import AppLabels
from api.core.objects import ManageQuery

from ... import db
from api.database.models import DeptNoteBook, Depts, DeptsPayment, NoteBookMember, User

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
noteBook_Member_Schema = NoteBookMemberSchema()
now = datetime.now()

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


@dept.get("/get-friend-from-dept-notebook")
@jwt_required(refresh=True)
def retrieve_members_from_dept_notebook():
    user_id = get_jwt_identity()['id']
    member_in_dept_list = []
    outside_friend = []

    get_member = db.session.query(DeptNoteBook, NoteBookMember.id, User.username).\
        join(NoteBookMember, DeptNoteBook.memeber_id == NoteBookMember.id, isouter=True).\
        join(User, NoteBookMember.friend_id == User.id, isouter=True).\
        filter(DeptNoteBook.borrower_name == None).\
        filter(DeptNoteBook.user_id == user_id).\
        all()

    get_friend_outside = db.session.query(DeptNoteBook.id, DeptNoteBook.borrower_name).\
        filter(DeptNoteBook.borrower_name != None).\
        filter(DeptNoteBook.user_id == user_id).\
        all()

    for member in get_friend_outside:
        outside_friend.append({
            **dept_note_book_schema.dump(member)
        })

    for member in get_member:
        member_in_dept_list.append({
            **user_schema.dump(member),
            **noteBook_Member_Schema.dump(member)
        })

    combine_all_list = member_in_dept_list + outside_friend

    return jsonify(data=combine_all_list)


@dept.get("/retrieve")
@jwt_required(refresh=True)
def user_get_dept():
    user_id = get_jwt_identity()['id']
    dept_list = []

    total_dept_amount = db.session.query(Depts).join(
        DeptNoteBook, Depts.note_id == DeptNoteBook.id, isouter=True).\
        filter(DeptNoteBook.user_id == user_id).order_by(
            desc(Depts.created_at)).all()

    for item in total_dept_amount:
        dept_list.append(dept_schema.dump(item))

    total_amount = manage_query.generate_total_amount(dept_list)

    return jsonify(data={"dept_list": dept_list, "total_dept": total_amount})

# Get dept by date


@dept.get("/retrieve-dept-by-current-date/<int:dept_note_id>")
@jwt_required(refresh=True)
def get_loan_by_current_date(dept_note_id):
    dept_list = []
    loan_data = Depts.query.filter_by(note_id=dept_note_id).\
        filter(extract('year', Depts.created_at) == todays_date.year).\
        filter(extract('month', Depts.created_at) ==
               todays_date.month).order_by(desc(Depts.created_at)).all()

    for item in loan_data:
        dept_list.append(dept_schema.dump(item))

    total_amount = manage_query.generate_total_amount(dept_list)

    return jsonify(data={
        "dept_list": dept_list,
        "total_amount": total_amount,
        "today_date": todays_date,
    })

# Add dept


@dept.post("/record-dept/<int:note_id>")
@jwt_required(refresh=True)
def user_add_dept(note_id):
    # Generate inputs
    try:
        data = request.json | {"note_id": note_id}
        for value in data["data"]:
            if value["amount"] is None:
                return response_with(resp.INVALID_INPUT_422)
            else:
                if value["lent_at"] == "":
                    recieved_at = {"lent_at": now}
                    QUERY.insert_data(db=db, table_data=Depts(
                        **value | {"note_id": note_id, **recieved_at}))
                    return jsonify({
                        "code": APP_LABEL.label("success"),
                        "message": APP_LABEL.label("Dept Amount recorded with success")
                    })
                else:
                    QUERY.insert_data(db=db, table_data=Depts(
                        **value | {"note_id": note_id}))
                    return jsonify({
                        "code": APP_LABEL.label("success"),
                        "message": APP_LABEL.label("Dept Amount recorded with success")
                    })

    except Exception:
        return response_with(resp.INVALID_INPUT_422)


# Pay dept
@dept.post("/pay-borrowed-amount/<int:dept_id>")
@jwt_required(refresh=True)
def user_pay_loan(dept_id):
    collect_payment_history = []
    request_data = request.json | {"note_id": dept_id}

    try:
        if request_data['data']["amount"] is None:
            return response_with(resp.INVALID_INPUT_422)

        if request_data['method'] == COMPUTE_SIMGLE_AMOUNT:
            get_single_amount = db.session.query(Depts.amount, Depts.currency_id).\
                filter(Depts.currency_id == request_data['data']['currency_id']).\
                filter(Depts.payment_status == False).\
                filter(Depts.id == dept_id).first()

            get_payment_history = db.session.query(DeptsPayment.amount).\
                filter(DeptsPayment.dept_id == dept_id).all()

            for amount in get_payment_history:
                collect_payment_history.append(float(amount['amount']))

            get_total_paid_amount = sum(collect_payment_history)

            for amount in get_single_amount:
                get_dept = amount - get_total_paid_amount

                if request_data['data']["amount"] <= amount and get_total_paid_amount <= amount and \
                        request_data['data']['amount'] <= get_dept:
                    data = {
                        **request_data['data'],
                        **{"dept_id": dept_id},
                        **{"budget_category_id": 7},
                        **{"budget_option_id": 2}
                    }
                    QUERY.insert_data(db=db, table_data=DeptsPayment(**data))
                    return jsonify({
                        "code": APP_LABEL.label("success"),
                        "message": APP_LABEL.label("You come to pay part of the dept."),
                    })
                if get_total_paid_amount == amount:
                    loan = db.session.query(Depts).filter(
                        Depts.id == dept_id).one()
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

    except Exception as e:
        return response_with(resp.INVALID_INPUT_422)
