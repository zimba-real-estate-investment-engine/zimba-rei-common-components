"""Initial migration

Revision ID: d97c4dcd529d
Revises: 
Create Date: 2024-10-25 23:48:57.032142

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd97c4dcd529d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # This should now have actual table creation code
    op.create_table(
        'subscription',
        sa.Column('id', sa.String(length=255), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=255)),
        sa.Column('service_subscribed_to', sa.String(length=255)),
        sa.Column('source_url', sa.String(length=255)),
        sa.Column('subscribed', sa.Boolean()),
        sa.Column('form_id', sa.String(length=255)),
        sa.Column('unsubscribed_date', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('unsubscribe_token', sa.String(length=255)),
        sa.Column('created_date', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        schema='zimba-rei-micro'
    )


def downgrade() -> None:
    op.drop_table('subscription', schema='zimba-rei-micro')