from marshmallow import fields

from ..database.models import (
    BudgetDetails, Cities, DeptsPayment, ExpenseDetails, LoanPayment, State, Country, Language, Currency, AmountProvenance,
    User, UserProfile, UserSpokenLanguage, Expenses, Loans, Depts, Savings, Budget
)

from .. import db
from .. import marsh


class CitiesSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Cities
        include_relationships = True
        load_instance = True


class StateSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = State
        include_relationships = True
        load_instance = True


class CountrySchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Country
        include_relationships = True
        load_instance = True


class LanguageSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Language
        include_relationships = True
        load_instance = True


class LanguageSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Currency
        include_relationships = True
        load_instance = True


class AmountProvenanceSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = AmountProvenance
        include_relationships = True
        load_instance = True


class UserSpokenLanguageProvenanceSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = UserSpokenLanguage
        include_relationships = True
        load_instance = True


class UserSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        sqla_session = db.session
        include_relationships = True
        load_instance = True
        include_fk = True

    id = fields.Number(dump_only=True)
    username = fields.String(required=False)
    email = fields.String(require=True)
    first_name = fields.String(required=False)
    last_name = fields.String(required=False)
    birth_date = fields.String(required=False)
    phone = fields.String(required=False)
    is_admin = fields.Boolean()
    is_user = fields.Boolean()
    country = fields.Number()
    language = fields.Number()
    password = fields.String()
    status = fields.Boolean()
    created_at = fields.String()
    updated_at = fields.String()
    confirmed = fields.String()
    confirmed_on = fields.String()
    profile = fields.Nested(lambda: UserProfileSchema())


class UserProfileSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = UserProfile
        sqla_session = db.session
        include_relationships = True
        load_instance = True
        include_fk = True

    id = fields.Number(dump_only=True)
    user_id = fields.Number(required=False)
    gender = fields.String(required=False)
    country = fields.Number(required=False)
    state = fields.Number(required=False)
    city = fields.Number(required=False)
    picture = fields.String(required=False)
    created_at = fields.String(required=False)


class ExpensesSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Expenses
        include_relationships = True
        load_instance = True


class ExpenseDetailsSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = ExpenseDetails
        include_relationships = True
        load_instance = True


class LoanSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Loans
        include_relationships = True
        load_instance = True


class LoanPaymentSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = LoanPayment
        include_relationships = True
        load_instance = True


class DeptsSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Depts
        include_relationships = True
        load_instance = True


class DeptPaymentSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = DeptsPayment
        include_relationships = True
        load_instance = True


class SavingsSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Savings
        include_relationships = True
        load_instance = True


class BudgetSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Budget
        include_relationships = True
        load_instance = True


class BudgetDetailsSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = BudgetDetails
        include_relationships = True
        load_instance = True
