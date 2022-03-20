"""empty message

Revision ID: a18d93503c8d
Revises: a230ca9dbb09
Create Date: 2022-03-12 08:45:57.390014

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a18d93503c8d'
down_revision = 'a230ca9dbb09'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dept_note_book', sa.Column('created_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('dept_note_book', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('dept_note_book', 'updated_at')
    op.drop_column('dept_note_book', 'created_at')
    # ### end Alembic commands ###
