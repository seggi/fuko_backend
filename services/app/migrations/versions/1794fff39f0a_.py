"""empty message

Revision ID: 1794fff39f0a
Revises: 689786c3f73e
Create Date: 2022-03-07 23:52:03.921929

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1794fff39f0a'
down_revision = '689786c3f73e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('expense_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('expense_id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('currency_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['currency_id'], ['currency.id'], ),
    sa.ForeignKeyConstraint(['expense_id'], ['expense.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('expense', sa.Column('expense_name', sa.Text(), nullable=False))
    op.drop_constraint('expense_currency_id_fkey', 'expense', type_='foreignkey')
    op.drop_column('expense', 'description')
    op.drop_column('expense', 'title')
    op.drop_column('expense', 'currency_id')
    op.drop_column('expense', 'amount')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('expense', sa.Column('amount', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False))
    op.add_column('expense', sa.Column('currency_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('expense', sa.Column('title', sa.TEXT(), autoincrement=False, nullable=True))
    op.add_column('expense', sa.Column('description', sa.TEXT(), autoincrement=False, nullable=True))
    op.create_foreign_key('expense_currency_id_fkey', 'expense', 'currency', ['currency_id'], ['id'])
    op.drop_column('expense', 'expense_name')
    op.drop_table('expense_details')
    # ### end Alembic commands ###
