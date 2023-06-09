"""add stocks table

Revision ID: 43b99eaf0111
Revises: 
Create Date: 2023-03-11 20:29:31.834420

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '43b99eaf0111'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stocks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('stock_symbol', sa.String(), nullable=False),
    sa.Column('number_of_shares', sa.Integer(), nullable=False),
    sa.Column('purchase_price', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('stocks')
    # ### end Alembic commands ###
