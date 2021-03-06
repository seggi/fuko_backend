"""empty message

Revision ID: 92be516c7592
Revises: aebe28acb37b
Create Date: 2022-05-10 08:58:40.981432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92be516c7592'
down_revision = 'aebe28acb37b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('rent_payment_option',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.Text(), nullable=True),
                    sa.Column('value', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('request_status',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('accommodation',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('lessor_id', sa.Integer(), nullable=False),
                    sa.Column('landlord_id', sa.Integer(), nullable=False),
                    sa.Column('amount', sa.Float(), nullable=False),
                    sa.Column('period_range', sa.Text(), nullable=True),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.Column('status', sa.Boolean(), nullable=True),
                    sa.Column('landlord_confirm', sa.Boolean(), nullable=True),
                    sa.Column('lessor_confirm', sa.Boolean(), nullable=True),
                    sa.Column('currency_id', sa.Integer(), nullable=True),
                    sa.Column('payment_option', sa.Integer(), nullable=True),
                    sa.Column('paid_at', sa.DateTime(
                        timezone=True), nullable=True),
                    sa.Column('updated_at', sa.DateTime(
                        timezone=True), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['currency_id'], ['currency.id'], ),
                    sa.ForeignKeyConstraint(['landlord_id'], ['users.id'], ),
                    sa.ForeignKeyConstraint(['lessor_id'], ['users.id'], ),
                    sa.ForeignKeyConstraint(['payment_option'], [
                        'rent_payment_option.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('notebook',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.Text(), nullable=True),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.Column('created_at', sa.DateTime(
                        timezone=True), nullable=True),
                    sa.Column('updated_at', sa.DateTime(
                        timezone=True), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('user_create_group',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('group_name', sa.Text(), nullable=False),
                    sa.Column('is_admin', sa.Boolean(), nullable=True),
                    sa.Column('group_deleted', sa.Boolean(), nullable=True),
                    sa.Column('created_at', sa.DateTime(
                        timezone=True), nullable=True),
                    sa.Column('updated_at', sa.DateTime(
                        timezone=True), nullable=True),
                    sa.Column('delete_at', sa.DateTime(
                        timezone=True), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('group_members',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.Column('group_id', sa.Integer(), nullable=True),
                    sa.Column('request_status', sa.Integer(), nullable=True),
                    sa.Column('requested_at', sa.DateTime(
                        timezone=True), nullable=True),
                    sa.Column('accepted_at', sa.DateTime(
                        timezone=True), nullable=True),
                    sa.Column('remove_member_at', sa.DateTime(
                        timezone=True), nullable=True),
                    sa.Column('status', sa.Boolean(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['group_id'], ['user_create_group.id'], ),
                    sa.ForeignKeyConstraint(['request_status'], [
                                            'request_status.id'], ),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('notebook_member',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('notebook_id', sa.Integer(), nullable=False),
                    sa.Column('sender_id', sa.Integer(), nullable=False),
                    sa.Column('friend_id', sa.Integer(), nullable=True),
                    sa.Column('request_status', sa.Integer(), nullable=True),
                    sa.Column('sent_at', sa.DateTime(
                        timezone=True), nullable=True),
                    sa.Column('confirmed_at', sa.DateTime(
                        timezone=True), nullable=True),
                    sa.Column('canceled_at', sa.DateTime(
                        timezone=True), nullable=True),
                    sa.ForeignKeyConstraint(['friend_id'], ['users.id'], ),
                    sa.ForeignKeyConstraint(
                        ['notebook_id'], ['notebook.id'], ),
                    sa.ForeignKeyConstraint(['request_status'], [
                                            'request_status.id'], ),
                    sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('group_depts',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('memeber_id', sa.Integer(), nullable=True),
                    sa.Column('amount', sa.Float(), nullable=False),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.Column('currency_id', sa.Integer(), nullable=True),
                    sa.Column('created_at', sa.DateTime(
                        timezone=True), nullable=True),
                    sa.Column('updated_at', sa.DateTime(
                        timezone=True), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['currency_id'], ['currency.id'], ),
                    sa.ForeignKeyConstraint(
                        ['memeber_id'], ['group_members.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('group_manage_money',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('contributor_id', sa.Integer(), nullable=True),
                    sa.Column('amount', sa.Float(), nullable=False),
                    sa.Column('description', sa.Text(), nullable=True),
                    sa.Column('currency_id', sa.Integer(), nullable=True),
                    sa.Column('created_at', sa.DateTime(
                        timezone=True), nullable=True),
                    sa.Column('updated_at', sa.DateTime(
                        timezone=True), nullable=True),
                    sa.ForeignKeyConstraint(['contributor_id'], [
                                            'group_members.id'], ),
                    sa.ForeignKeyConstraint(
                        ['currency_id'], ['currency.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.add_column('dept_note_book', sa.Column(
        'friend_id', sa.Integer(), nullable=True))
    op.drop_constraint('dept_note_book_borrower_id_fkey',
                       'dept_note_book', type_='foreignkey')
    op.create_foreign_key(None, 'dept_note_book',
                          'notebook_member', ['friend_id'], ['id'])
    op.drop_column('dept_note_book', 'borrower_id')
    op.add_column('loan_note_book', sa.Column(
        'friend_id', sa.Integer(), nullable=True))
    op.drop_constraint('loan_note_book_partner_id_fkey',
                       'loan_note_book', type_='foreignkey')
    op.create_foreign_key(None, 'loan_note_book',
                          'notebook_member', ['friend_id'], ['id'])
    op.drop_column('loan_note_book', 'partner_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('loan_note_book', sa.Column(
        'partner_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'loan_note_book', type_='foreignkey')
    op.create_foreign_key('loan_note_book_partner_id_fkey',
                          'loan_note_book', 'users', ['partner_id'], ['id'])
    op.drop_column('loan_note_book', 'friend_id')
    op.add_column('dept_note_book', sa.Column(
        'borrower_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'dept_note_book', type_='foreignkey')
    op.create_foreign_key('dept_note_book_borrower_id_fkey',
                          'dept_note_book', 'users', ['borrower_id'], ['id'])
    op.drop_column('dept_note_book', 'friend_id')
    op.drop_table('group_manage_money')
    op.drop_table('group_depts')
    op.drop_table('notebook_member')
    op.drop_table('group_members')
    op.drop_table('user_create_group')
    op.drop_table('notebook')
    op.drop_table('accommodation')
    op.drop_table('request_status')
    op.drop_table('rent_payment_option')
    # ### end Alembic commands ###
