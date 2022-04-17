from datetime import date
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from api.database.models import DeptNoteBook, Depts, ExpenseDetails, Expenses, LoanNoteBook, Loans, Savings, User
from api.utils.model_marsh import DeptsSchema, ExpenseDetailsSchema, ExpensesSchema, LoanSchema, SavingsSchema, UserSchema
from api.core.query import QueryGlobalRepport
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

# Call Schema
USER_SCHEMA = UserSchema(many=True)
EXPENSES_SCHEMA = ExpenseDetailsSchema(many=True)
LOANS_SCHEMA = LoanSchema(many=True)
DEPT_SCHEMA = DeptsSchema(many=True)
SAVINGS_SCHEMA = SavingsSchema(many=True)


QUERY = QueryGlobalRepport()


@global_account.get("/global-amount/<int:user_id>")
@jwt_required()
def user_global_amount(user_id):
    expenses = db.session.query(ExpenseDetails).join(
        Expenses, ExpenseDetails.expense_id == Expenses.id, isouter=True).\
        filter(Expenses.user_id == user_id).all()

    loans = db.session.query(Loans).join(
        LoanNoteBook, Loans.note_id == LoanNoteBook.id, isouter=True).\
            filter(LoanNoteBook.user_id == user_id).all()

    savings = QUERY.get_all_joined_table_by_id(
        db=db, model1=USER, model2=SAVINGS, user_id=user_id)

    dept = db.session.query(Depts).join(
        DeptNoteBook, Depts.note_id == DeptNoteBook.id, isouter=True).\
        filter(DeptNoteBook.user_id == user_id).all()

    result = GlobalAmount(
        tbl1=EXPENSES_SCHEMA.dump(expenses),
        tbl2=LOANS_SCHEMA.dump(loans),
        tbl3=SAVINGS_SCHEMA.dump(savings),
        tbl4=DEPT_SCHEMA.dump(dept)
    )

    global_amount = result.computer_amount(
        item_list=result.out_put(),
    )
    return jsonify(data={"all_4_tables": result.out_put(), "global_amount": global_amount})


# @global_account.get("/global-amount-by-date/<int:user_id>")
# @jwt_required()
# def user_global_amount_by_date(user_id):
#     expenses = QUERY.get_data_by_date(
#         db=db, model1=USER, model2=EXPENSES, user_id=user_id,
#         date={"year": todays_date.year, "month": todays_date.month})
#     loans = QUERY.get_data_by_date(
#         db=db, model1=USER, model2=LOANS, user_id=user_id,
#         date={"year": todays_date.year, "month": todays_date.month})
#     savings = QUERY.get_data_by_date(
#         db=db, model1=USER, model2=SAVINGS, user_id=user_id,
#         date={"year": todays_date.year, "month": todays_date.month})
#     dept = QUERY.get_data_by_date(
#         db=db, model1=USER, model2=DEPT, user_id=user_id,
#         date={"year": todays_date.year, "month": todays_date.month})

#     result = GlobalAmount(
#         tbl1=EXPENSES_SCHEMA.dump(expenses),
#         tbl2=LOANS_SCHEMA.dump(loans),
#         tbl3=SAVINGS_SCHEMA.dump(savings),
#         tbl4=DEPT_SCHEMA.dump(dept)
#     )

#     global_amount = result.computer_amount(
#         item_list=result.out_put(),
#     )

#     return jsonify(data={"all_4_tables": result.out_put(), "all_in_one": global_amount})
