"""empty message

Revision ID: a230ca9dbb09
Revises: fffd02da636d
Create Date: 2022-03-12 08:44:46.088088

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a230ca9dbb09'
down_revision = 'fffd02da636d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dept_note_book',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('borrower_id', sa.Integer(), nullable=True),
    sa.Column('borrower_name', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['borrower_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('depts', sa.Column('note_id', sa.Integer(), nullable=True))
    op.drop_constraint('depts_user_id_fkey', 'depts', type_='foreignkey')
    op.drop_constraint('depts_borrower_id_fkey', 'depts', type_='foreignkey')
    op.create_foreign_key(None, 'depts', 'dept_note_book', ['note_id'], ['id'])
    op.drop_column('depts', 'borrower_name')
    op.drop_column('depts', 'user_id')
    op.drop_column('depts', 'borrower_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('depts', sa.Column('borrower_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('depts', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('depts', sa.Column('borrower_name', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'depts', type_='foreignkey')
    op.create_foreign_key('depts_borrower_id_fkey', 'depts', 'users', ['borrower_id'], ['id'])
    op.create_foreign_key('depts_user_id_fkey', 'depts', 'users', ['user_id'], ['id'])
    op.drop_column('depts', 'note_id')
    op.drop_table('dept_note_book')
    # ### end Alembic commands ###
