"""empty message

Revision ID: 9477fc0e5476
Revises: 8504ca66be06
Create Date: 2022-09-12 11:58:58.026699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9477fc0e5476'
down_revision = '8504ca66be06'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_profile',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('gender', sa.String(length=8), nullable=True),
    sa.Column('country', sa.Integer(), nullable=True),
    sa.Column('state', sa.Integer(), nullable=True),
    sa.Column('city', sa.Integer(), nullable=True),
    sa.Column('picture', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['city'], ['cities.id'], ),
    sa.ForeignKeyConstraint(['country'], ['country.id'], ),
    sa.ForeignKeyConstraint(['state'], ['state.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_profile')
    # ### end Alembic commands ###
