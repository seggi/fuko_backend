from datetime import date
from re import L
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.database.models import Currency, DeptNoteBook, Depts, DeptsPayment, ExpenseDetails, Expenses, LoanNoteBook, LoanPayment, Loans, RecordDeptPayment, Savings, User
from api.utils.model_marsh import CurrencySchema, DeptsSchema, ExpenseDetailsSchema, ExpensesSchema, LoanPaymentSchema, LoanSchema, RecordDeptPaymentSchema, SavingsSchema, UserSchema
from api.core.query import QueryGlobalReport
from api.core.objects import GlobalAmount

from ... import db

global_account = Blueprint("global_account", __name__,
                           url_prefix="/api/user/account")

# Get current date
todays_date = date.today()

# Call Models
USER = User
EXPENSES = ExpenseDetails
LOANS = Loans
DEPT = Depts
SAVINGS = Savings
RECORD_DEPT_PAYMENT = RecordDeptPayment

# Call Schema
USER_SCHEMA = UserSchema(many=True)
EXPENSES_SCHEMA = ExpenseDetailsSchema(many=True)
LOANS_SCHEMA = LoanSchema(many=True)
DEPT_SCHEMA = DeptsSchema(many=True)
SAVINGS_SCHEMA = SavingsSchema(many=True)
RECORD_DEPT_PAYMENT_SCHEMA = RecordDeptPaymentSchema(many=True)
PAID_LOAN_SCHEMA = LoanPaymentSchema(many=True)
CURRENCY_SCHEMA = CurrencySchema()


QUERY = QueryGlobalReport()


@global_account.get("/global-amount/<int:currency_id>")
@jwt_required(refresh=True)
def user_global_amount(currency_id):
    user_id = get_jwt_identity()['id']
    paid_amount = []

    currencyCode = db.session.query(Currency.code).filter(
        Currency.id == currency_id).all()

    expenses = db.session.query(ExpenseDetails).join(
        Expenses, ExpenseDetails.expense_id == Expenses.id, isouter=True).\
        filter(Expenses.user_id == user_id,
               ExpenseDetails.currency_id == currency_id).all()

    loans = db.session.query(Loans).join(
        LoanNoteBook, Loans.note_id == LoanNoteBook.id, isouter=True).\
        filter(LoanNoteBook.user_id == user_id,
               Loans.currency_id == currency_id).all()

    person_paid_loan = db.session.query(LoanPayment.amount).\
        join(LoanNoteBook, LoanPayment.notebook_id == LoanNoteBook.id).\
        filter(LoanNoteBook.user_id == user_id).\
        filter(LoanPayment.currency_id == currency_id).\
        all()

    pub_paid_loan = db.session.query(LoanPayment.amount).\
        join(LoanNoteBook, LoanPayment.notebook_id == LoanNoteBook.id).\
        filter(LoanNoteBook.friend_id == user_id,
               LoanPayment.currency_id == currency_id).all()

    pub_paid_dept = db.session.query(RecordDeptPayment.amount).\
        join(DeptNoteBook, RecordDeptPayment.note_id == DeptNoteBook.id).\
        filter(DeptNoteBook.memeber_id == user_id,
               RecordDeptPayment.currency_id == currency_id).all()

    person_paid_dept = db.session.query(RecordDeptPayment.amount).\
        join(DeptNoteBook, RecordDeptPayment.note_id == DeptNoteBook.id).\
        filter(DeptNoteBook.user_id == user_id,
               RecordDeptPayment.currency_id == currency_id).all()

    savings = db.session.query(Savings).join(
        User, Savings.user_id == User.id, isouter=True).\
        filter(Savings.user_id == user_id,
               Savings.currency_id == currency_id).all()

    dept = db.session.query(Depts).\
        join(DeptNoteBook, Depts.note_id == DeptNoteBook.id, isouter=True).\
        filter(DeptNoteBook.user_id == user_id).\
        filter(Depts.currency_id == currency_id).all()

    paid_dept = db.session.query(RecordDeptPayment).\
        join(DeptNoteBook, RecordDeptPayment.note_id == DeptNoteBook.id, isouter=True).\
        filter(DeptNoteBook.user_id == user_id).\
        filter(RecordDeptPayment.currency_id == currency_id).all()

    result = GlobalAmount(
        tbl1=EXPENSES_SCHEMA.dump(expenses),
        tbl2=LOANS_SCHEMA.dump(loans),
        tbl3=SAVINGS_SCHEMA.dump(savings),
        tbl4=DEPT_SCHEMA.dump(dept),
        tbl5=RECORD_DEPT_PAYMENT_SCHEMA.dump(paid_dept),
        tbl6=PAID_LOAN_SCHEMA.dump(person_paid_loan),
        tbl7=PAID_LOAN_SCHEMA.dump(pub_paid_loan),
        tbl8=RECORD_DEPT_PAYMENT_SCHEMA.dump(pub_paid_dept),
        tbl9=RECORD_DEPT_PAYMENT_SCHEMA.dump(person_paid_dept)
    )

    global_amount = result.computer_amount(
        item_list=result.out_put(),
    )

    currencyCode_list = []

    for code in currencyCode:
        getCode = CURRENCY_SCHEMA.dump(code)
        currencyCode_list.append(getCode['code'])

    return jsonify(data={"all_4_tables": result.out_put(), "global_amount": {**global_amount, **{"currencyCode": currencyCode_list[0]}}})


@global_account.get("/global-amount-by-date/<int:user_id>")
@jwt_required(refresh=True)
def user_global_amount_by_date(user_id):
    expenses = QUERY.get_data_by_date(
        db=db, model1=USER, model2=EXPENSES, user_id=user_id,
        date={"year": todays_date.year, "month": todays_date.month})
    loans = QUERY.get_data_by_date(
        db=db, model1=USER, model2=LOANS, user_id=user_id,
        date={"year": todays_date.year, "month": todays_date.month})
    savings = QUERY.get_data_by_date(
        db=db, model1=USER, model2=SAVINGS, user_id=user_id,
        date={"year": todays_date.year, "month": todays_date.month})
    dept = QUERY.get_data_by_date(
        db=db, model1=USER, model2=DEPT, user_id=user_id,
        date={"year": todays_date.year, "month": todays_date.month})

    result = GlobalAmount(
        tbl1=EXPENSES_SCHEMA.dump(expenses),
        tbl2=LOANS_SCHEMA.dump(loans),
        tbl3=SAVINGS_SCHEMA.dump(savings),
        tbl4=DEPT_SCHEMA.dump(dept)
    )

    global_amount = result.computer_amount(
        item_list=result.out_put(),
    )

    return jsonify(data={"all_4_tables": result.out_put(), "all_in_one": global_amount})
