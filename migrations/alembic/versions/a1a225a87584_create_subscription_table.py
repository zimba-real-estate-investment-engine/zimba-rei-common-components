"""create_subscription_table

Revision ID: a1a225a87584
Revises: 
Create Date: 2024-10-31 16:12:30.117579

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'a1a225a87584'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subscription')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscription',
    sa.Column('id', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('email', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('name', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('service_subscribed_to', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('source_url', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('form_id', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('unsubscribed_date', mysql.TIMESTAMP(), server_default=sa.text('current_timestamp()'), nullable=True),
    sa.Column('unsubscribe_token', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('created_date', mysql.TIMESTAMP(), server_default=sa.text('current_timestamp()'), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='latin1_swedish_ci',
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
