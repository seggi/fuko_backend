"""empty message

Revision ID: 25146edfffe4
Revises: c258dc026978
Create Date: 2022-05-10 14:22:20.361373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25146edfffe4'
down_revision = 'c258dc026978'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('amount_provenance', sa.Column('provenance_name', sa.String(length=200), nullable=False))
    op.drop_column('amount_provenance', 'name')
    op.add_column('notebook', sa.Column('notebook_name', sa.Text(), nullable=True))
    op.drop_column('notebook', 'name')
    op.add_column('request_status', sa.Column('request_status_name', sa.Text(), nullable=True))
    op.drop_column('request_status', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('request_status', sa.Column('name', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_column('request_status', 'request_status_name')
    op.add_column('notebook', sa.Column('name', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_column('notebook', 'notebook_name')
    op.add_column('amount_provenance', sa.Column('name', sa.VARCHAR(length=200), autoincrement=False, nullable=False))
    op.drop_column('amount_provenance', 'provenance_name')
    # ### end Alembic commands ###
