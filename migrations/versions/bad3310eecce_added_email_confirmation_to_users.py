"""Added email confirmation to users

Revision ID: bad3310eecce
Revises: 160916e73ce9
Create Date: 2023-03-15 17:02:37.037646

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bad3310eecce'
down_revision = '160916e73ce9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('registered_on', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('email_confirmation_sent_on', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('email_confirmed', sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column('email_confirmed_on', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('email_confirmed_on')
        batch_op.drop_column('email_confirmed')
        batch_op.drop_column('email_confirmation_sent_on')
        batch_op.drop_column('registered_on')

    # ### end Alembic commands ###
