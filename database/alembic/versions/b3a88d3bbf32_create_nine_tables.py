"""create_nine_tables

Revision ID: b3a88d3bbf32
Revises: c045967c7472
Create Date: 2024-11-24 00:05:25.226202

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'b3a88d3bbf32'
down_revision: Union[str, None] = 'c045967c7472'
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
    sa.Column('subscribed', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='latin1_swedish_ci',
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
