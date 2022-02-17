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
@jwt_required()
def user_global_amount(user_id):

    expenses = QUERY.get_all_joined_table_by_id(
        db=db, model1=USER, model2=EXPENSES, user_id=user_id)
    loans = QUERY.get_all_joined_table_by_id(
        db=db, model1=USER, model2=LOANS, user_id=user_id)
    savings = QUERY.get_all_joined_table_by_id(
        db=db, model1=USER, model2=SAVINGS, user_id=user_id)
    dept = QUERY.get_all_joined_table_by_id(
        db=db, model1=USER, model2=DEPT, user_id=user_id)

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
