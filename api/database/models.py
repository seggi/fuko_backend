from datetime import datetime
from email.policy import default
from pydoc import describe
from tokenize import group
from sqlalchemy import (
    Column, Integer, DateTime, Boolean, String, Float, Text, ForeignKey, LargeBinary
)
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy.orm import backref


from .. import db


class Country(db.Model):
    __tablename__ = "country"
    id = Column('id', Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())


class State(db.Model):
    __tablename__ = "state"
    id = Column('id', Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    country_id = Column(Integer, ForeignKey("country.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())


class Cities(db.Model):
    __tablename__ = "cities"
    id = Column('id', Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    state_id = Column(Integer, ForeignKey("state.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())


class Language(db.Model):
    __tablename__ = "languages"
    id = Column('id', Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    default = Column(Boolean(), default=True)
    created_at = Column(DateTime(timezone=True), default=func.now())


class Currency(db.Model):
    __tablename__ = "currency"
    id = Column('id', Integer, primary_key=True)
    code = Column(String(10), nullable=False)
    description = Column(String(200), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())


# Request Status
'''
 Status options
 - sent
 - accepted
 - rejected
 - expired
'''


class RequestStatus(db.Model):
    __tablename__ = "request_status"
    id = Column('id', Integer, primary_key=True)
    request_status_name = Column(Text(), nullable=True)


class BudgetOption(db.Model):
    __tablename__ = "budget_option"
    id = Column('id', Integer, primary_key=True)
    name = Column(Text(), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())


class BudgetCategories(db.Model):
    __tablename__ = "budget_categories"
    id = Column('id', Integer, primary_key=True)
    name = Column(Text(), nullable=True)
    description = Column(Text(), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())

# Amount provenance category


class AmountProvenance(db.Model):
    __tablename__ = "amount_provenance"
    id = Column('id', Integer, primary_key=True)
    provenance_name = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())

# Register User


class User(db.Model):
    __tablename__ = "users"
    id = Column('id', Integer, primary_key=True)
    username = Column(String(20), nullable=True, unique=False)
    email = Column(String(128), unique=True, nullable=True)
    first_name = Column(String(50), unique=False, nullable=True)
    last_name = Column(String(50), unique=False, nullable=True)
    birth_date = Column(String(10), unique=False, nullable=False)
    phone = Column(String(20), nullable=True, unique=True)
    is_admin = Column(Boolean(), default=False)
    is_user = Column(Boolean(), default=False)
    status = Column(Boolean(), default=False)
    language = Column(Integer, ForeignKey("languages.id"), nullable=True)
    password = Column(Text(), nullable=True)
    status = Column(Boolean(), default=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())
    confirmed = Column(Boolean(), nullable=False, default=False)
    confirmed_on = Column(DateTime(timezone=True),
                          default=func.now(), nullable=True)
    profile = db.relationship("UserProfile", backref="user", lazy=True)
    expense = db.relationship(
        "Expenses", backref=backref("users", lazy="joined"))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

# User Profile


class UserProfile(db.Model):
    __tablename__ = "user_profile"
    id = Column('id', Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    gender = Column(String(8), nullable=True)
    country = Column(Integer, ForeignKey("country.id"), nullable=True)
    state = Column(Integer, ForeignKey('state.id'), nullable=True)
    city = Column(Integer, ForeignKey('cities.id'), nullable=True)
    picture = Column(Text(), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())


class UserDefaultCurrency(db.Model):
    __tablename__ = "user_default_currency"
    id = Column('id', Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=True)

# User spoken language


class UserSpokenLanguage(db.Model):
    __tablename__ = "user_spoken_language"
    id = Column('id', Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    languages_id = Column(Integer, ForeignKey('languages.id'))
    created_at = Column(DateTime(timezone=True), default=func.now())

# Accountability Table

# Private Expenses
# Expense can not be deleted


class Expenses(db.Model):
    __tablename__ = "expense"
    id = Column('id', Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    expense_name = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())


class ExpenseDetails(db.Model):
    __tablename__ = "expense_details"
    id = Column('id', Integer, primary_key=True)
    expense_id = Column(Integer, ForeignKey('expense.id'), nullable=True)
    budget_category_id = Column(Integer, ForeignKey(
        'budget_categories.id'), nullable=True)
    budget_option_id = Column(Integer, ForeignKey(
        'budget_option.id'), default=2, nullable=True)
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())


# Note Book
'''
The notebook can be shared between two people 
When accept request then join share note book info
'''


class NoteBook(db.Model):
    __tablename__ = 'notebook'
    id = Column('id', Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    notebook_name = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())


'''Share your note book with friends'''


class NoteBookMember(db.Model):
    __tablename__ = 'notebook_member'
    id = Column('id', Integer, primary_key=True)
    notebook_id = Column(Integer, ForeignKey('notebook.id'), nullable=False)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    friend_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    request_status = Column(Integer, ForeignKey(
        'request_status.id'), nullable=True)
    sent_at = Column(DateTime(timezone=True), default=func.now())
    confirmed_at = Column(DateTime(timezone=True))
    canceled_at = Column(DateTime(timezone=True))


# Loan Table
'''Include ORGANIZATION in future'''


class LoanNoteBook(db.Model):
    __tablename__ = "loan_note_book"
    id = Column('id', Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    # ? to be changed to member_id
    friend_id = Column(Integer, ForeignKey(
        'notebook_member.id'), nullable=True)
    '''If your partner is not fuko user <mention his/her name>'''
    partner_name = Column(Text, nullable=True)
    notebook_id = Column(Integer, ForeignKey('notebook.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())


class Loans(db.Model):
    __tablename__ = "loans"
    id = Column('id', Integer, primary_key=True)
    note_id = Column(Integer, ForeignKey('loan_note_book.id'), nullable=True)
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    '''Enter the date of receiving money & section works when the your financial partener is not in the system'''
    recieve_money_at = Column(DateTime(), nullable=True)
    payment_status = Column(Boolean, default=False)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True))


class LoanPayment(db.Model):
    __tablename__ = "loan_payment"
    id = Column('id', Integer, primary_key=True)
    loan_id = Column(Integer, ForeignKey('loans.id'), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=True)
    budget_category_id = Column(Integer, ForeignKey(
        'budget_categories.id'), default=7, nullable=True)
    budget_option_id = Column(Integer, ForeignKey(
        'budget_option.id'), default=1, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())

# Depts Table
# Record lender in note list


class DeptNoteBook(db.Model):
    __tablename__ = "dept_note_book"
    id = Column('id', Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    memeber_id = Column(Integer, ForeignKey(
        'notebook_member.id'), nullable=True)
    '''If lender is not fuko user <provider his/her name>'''
    borrower_name = Column(Text, nullable=True)
    notebook_id = Column(Integer, ForeignKey('notebook.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())


class Depts(db.Model):
    __tablename__ = "depts"
    id = Column('id', Integer, primary_key=True)
    note_id = Column(Integer, ForeignKey('dept_note_book.id'), nullable=True)
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    '''Enter the date of receiving money & section works when the lender is not in the system'''
    lent_at = Column(DateTime())
    payment_status = Column(Boolean, default=False)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())

# ! Remove DeptsPayment in the near future


class DeptsPayment(db.Model):
    __tablename__ = "dept_payment"
    id = Column('id', Integer, primary_key=True)
    dept_id = Column(Integer, ForeignKey('depts.id'), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=True)
    budget_category_id = Column(Integer, ForeignKey(
        'budget_categories.id'), default=7, nullable=True)
    budget_option_id = Column(Integer, ForeignKey(
        'budget_option.id'), default=2, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())


class RecordDeptPayment(db.Model):
    __tablename__ = "record_dept_payment"
    id = Column('id', Integer, primary_key=True)
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    note_id = Column(Integer, ForeignKey('dept_note_book.id'), nullable=True)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=True)
    budget_category_id = Column(Integer, ForeignKey(
        'budget_categories.id'), default=7, nullable=True)
    budget_option_id = Column(Integer, ForeignKey(
        'budget_option.id'), default=2, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())

# Savings Table


class Savings(db.Model):
    __tablename__ = "savings"
    id = Column('id', Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    budget_category_id = Column(Integer, ForeignKey(
        'budget_categories.id'), default=7, nullable=True)
    budget_option_id = Column(Integer, ForeignKey(
        'budget_option.id'), default=2, nullable=True)
    money_provenance = Column(Integer, ForeignKey(
        'amount_provenance.id'), nullable=True)
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())


# Budget Table
'''The system will check first the total amount user has in his wallet'''


class Budget(db.Model):
    __tablename__ = "Budget"
    id = Column('id', Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(Text(), nullable=False)
    description = Column(Text, nullable=True)  # Example Incoming or Expenses
    start_date = Column(DateTime(), nullable=True)
    end_date = Column(DateTime(), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())


class BudgetDetails(db.Model):
    __tablename__ = "budget_details"
    id = Column('id', Integer, primary_key=True)
    budget_id = Column(Integer, ForeignKey('Budget.id'), nullable=False)
    budget_option_id = Column(Integer, ForeignKey(
        'budget_option.id'), nullable=True)
    budget_category_id = Column(Integer, ForeignKey(
        'budget_categories.id'), nullable=True)
    summary = Column(Text, nullable=True)
    budget_amount = Column(Float, nullable=True)
    actual_amount = Column(Float, nullable=True)
    difference_amount = Column(Float, nullable=True)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())

# User create Groupe


class UserCreateGroup(db.Model):
    __tablename__ = "user_create_group"
    id = Column('id', Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    group_name = Column(Text(), nullable=False)
    is_admin = Column(Boolean(), default=False)
    group_deleted = Column(Boolean(), default=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())
    delete_at = Column(DateTime(timezone=True))


class GroupMembers(db.Model):
    __tablename__ = "group_members"
    id = Column('id', Integer, primary_key=True)
    # member_id
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    group_id = Column(Integer, ForeignKey("user_create_group.id"))
    request_status = Column(Integer, ForeignKey(
        'request_status.id'), nullable=True)
    requested_at = Column(DateTime(timezone=True), default=func.now())
    accepted_at = Column(DateTime(timezone=True))
    remove_member_at = Column(DateTime(timezone=True))
    status = Column(Boolean(), default=True)


# Public Expenses or (Group Expenses)

class GroupeContributorAmount(db.Model):
    __tablename__ = "group_manage_money"
    id = Column('id', Integer, primary_key=True)
    contributor_id = Column(Integer, ForeignKey("group_members.id"))
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())


class GroupDepts(db.Model):
    __tablename__ = "group_depts"
    id = Column('id', Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("group_members.id"))
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())


'''
Defferents Rent payment options
- Month
- Week
- Day
- Year
'''


class RentPaymentOption(db.Model):
    __tablename__ = "rent_payment_option"
    id = Column('id', Integer, primary_key=True)
    name = Column(Text(), nullable=True)
    value = Column(Text(), nullable=True)


class LessorOrLandlordToRentPayment(db.Model):
    __tablename__ = "lessor_landlord_to_rent_payment"
    id = Column('id', Integer, primary_key=True)
    lessor_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    landlord_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    request_status = Column(Integer, ForeignKey(
        'request_status.id'), nullable=True)
    confirmed_at = Column(DateTime(timezone=True))
    sent_at = Column(DateTime(timezone=True), default=func.now())


class Accommodation(db.Model):
    __tablename__ = "accommodation"
    id = Column('id', Integer, primary_key=True)
    rent_payment_id = Column(Integer, ForeignKey(
        'lessor_landlord_to_rent_payment.id'), nullable=False)
    amount = Column(Float, nullable=False)
    period_range = Column(Text, nullable=True)
    month_name = Column(Text, nullable=True)
    year = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    '''If not paid yet default = False'''
    status = Column(Boolean(), default=False)
    landlord_confirm = Column(Boolean(), default=False)
    lessor_confirm = Column(Boolean(), default=False)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=True)
    payment_option = Column(Integer, ForeignKey(
        'rent_payment_option.id'), nullable=True)
    paid_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())
    budget_category_id = Column(Integer, ForeignKey(
        'budget_categories.id'), default=1)
    budget_option_id = Column(Integer, ForeignKey(
        'budget_option.id'), default=2, nullable=True)


'''In the future we have to combine with tontine && back'''
