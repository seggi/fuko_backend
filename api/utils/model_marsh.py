from imp import load_dynamic
from xml.etree.ElementInclude import include
from marshmallow import fields

from ..database.models import (
    Accommodation, BudgetCategories, BudgetDetails, Cities, DeptNoteBook, DeptsPayment, ExpenseDetails, GroupeContributorAmount,
    LoanNoteBook, LoanPayment, State, Country, Language, Currency, AmountProvenance,
    User, UserProfile, UserSpokenLanguage, Expenses, Loans, Depts, Savings, Budget,
    NoteBook, NoteBookMember, RequestStatus,  UserDefaultCurrency, UserCreateGroup,
    GroupMembers, BudgetOption, RecordDeptPayment
)

from .. import db
from .. import marsh


class BudgetOptionSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = BudgetOption
        load_instance = True


class BudgetCategoriesSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = BudgetCategories
        load_instance = True


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


class CurrencySchema(marsh.SQLAlchemyAutoSchema):
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


class LoanNoteBookSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = LoanNoteBook
        include_relationships = True
        load_instance = True


class DeptNoteBookSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = DeptNoteBook
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


class NoteBookSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = NoteBook
        include_relationships = True
        load_instance = True


class NoteBookMemberSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = NoteBookMember
        include_relationships = True
        load_instance = True


class RequestStatusSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = RequestStatus
        include_relationships = True
        load_instance = True


class AccommodationStatusSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = Accommodation
        include_relationships = True
        load_instance = True


class UserDefaultCurrencySchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = UserDefaultCurrency
        include_relationships = True
        load_instance = True


class UserCreateGroupSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = UserCreateGroup
        include_relationships = True
        load_instance = True


class GroupMemberSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = GroupMembers
        include_relationships = True
        load_instance = True


class RecordDeptPaymentSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = RecordDeptPayment
        include_relationships = True
        load_instance = True


class GroupeContributorAmountSchema(marsh.SQLAlchemyAutoSchema):
    class Meta:
        model = GroupeContributorAmount
        include_relationships = True
        load_instance = True
