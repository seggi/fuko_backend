from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from api.database.models import Depts, Expenses, Loans, Savings, User
from api.utils.model_marsh import DeptsSchema, ExpensesSchema, LoanSchema, SavingsSchema, UserSchema
from api.core.query import QueryGlobalRepport
from api.core.objects import GlobalAmount

from ... import db

global_account = Blueprint("global_account", __name__,
                           url_prefix="/api/user/account")

# Call Models
USER = User
EXPENSES = Expenses
LOANS = Loans
DEPT = Depts
SAVINGS = Savings

# Call Schema
USER_SCHEMA = UserSchema(many=True)
EXPENSES_SCHEMA = ExpensesSchema(many=True)
LOANS_SCHEMA = LoanSchema(many=True)
DEPT_SCHEMA = DeptsSchema(many=True)
SAVINGS_SCHEMA = SavingsSchema(many=True)

QUERY = QueryGlobalRepport()


@global_account.get("/global-amount/<int:user_id>")
# @jwt_required()
def user_global_amount(user_id):
    expenses_list = []
    loans_list = []
    savings_list = []
    dept_list = []

    expenses = QUERY.get_all_joined_table_by_id(
        db=db, model1=USER, model2=EXPENSES, user_id=user_id)
    loans = QUERY.get_all_joined_table_by_id(
        db=db, model1=USER, model2=LOANS, user_id=user_id)
    savings = QUERY.get_all_joined_table_by_id(
        db=db, model1=USER, model2=SAVINGS, user_id=user_id)
    dept = QUERY.get_all_joined_table_by_id(
        db=db, model1=USER, model2=DEPT, user_id=user_id)

    for data in expenses:
        expenses_list.append(EXPENSES_SCHEMA.dump(data))

    for data in loans:
        loans_list.append(LOANS_SCHEMA.dump(data))

    for data in savings:
        savings_list.append(SAVINGS_SCHEMA.dump(data))

    for data in dept:
        dept_list.append(DEPT_SCHEMA.dump(data))

    result = GlobalAmount(
        tbl1=expenses_list,
        tbl2=loans_list,
        tbl3=savings_list,
        tbl4=dept_list
    )

    return jsonify(data=result.out_put())
