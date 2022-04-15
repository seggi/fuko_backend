from datetime import datetime
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
    name = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())

# Amount provenance category


class AmountProvenance(db.Model):
    __tablename__ = "amount_provenance"
    id = Column('id', Integer, primary_key=True)
    name = Column(String(200), nullable=False)
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


# User spoken language


class UserSpokenLanguage(db.Model):
    __tablename__ = "user_spoken_language"
    id = Column('id', Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    languages_id = Column(Integer, ForeignKey('languages.id'))
    created_at = Column(DateTime(timezone=True), default=func.now())

# Accountability Table

# Expenses
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
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())


# Loan Table
'''Make in the future you include ORGANIZATION'''

class LoanNoteBook(db.Model):
    __tablename__ = "loan_note_book"
    id = Column('id', Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    partner_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    '''If your partener is not fuko user <mension his/her name>'''
    partner_name = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())

class Loans(db.Model):
    __tablename__ = "loans"
    id = Column('id', Integer, primary_key=True)
    note_id = Column(Integer, ForeignKey('loan_note_book.id'), nullable=True)
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    '''Enter the date of receiving money & section works when the your financial partener is not in the system'''
    recieve_money_at = Column(DateTime())
    payment_status = Column(Boolean, default=False)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())


class LoanPayment(db.Model):
    __tablename__ = "loan_payment"
    id = Column('id', Integer, primary_key=True)
    loan_id = Column(Integer, ForeignKey('loans.id'), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())

# Depts Table
# Record lender in note list

class DeptNoteBook(db.Model):
    __tablename__ = "dept_note_book"
    id = Column('id', Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    borrower_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    '''If lender is not fuko user <mension his/her name>'''
    borrower_name = Column(Text, nullable=True)
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


class DeptsPayment(db.Model):
    __tablename__ = "dept_payment"
    id = Column('id', Integer, primary_key=True)
    dept_id = Column(Integer, ForeignKey('depts.id'), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())


# Savings Table


class Savings(db.Model):
    __tablename__ = "savings"
    id = Column('id', Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
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
    start_date = Column(DateTime(), nullable=True)
    end_date = Column(DateTime(), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())


class BudgetDetails(db.Model):
    __tablename__ = "budget_details"
    id = Column('id', Integer, primary_key=True)
    budget_id = Column(Integer, ForeignKey('Budget.id'), nullable=False)
    amount = Column(Float, nullable=False)
    activity_description = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    currency_id = Column(Integer, ForeignKey('currency.id'), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now())


''' In the future we have to combine with tontine && back'''
