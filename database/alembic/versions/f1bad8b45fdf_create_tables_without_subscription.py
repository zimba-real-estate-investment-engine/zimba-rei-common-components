"""create_tables_without_subscription

Revision ID: f1bad8b45fdf
Revises: 6ed7265ab218
Create Date: 2024-11-24 01:19:31.941184

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1bad8b45fdf'
down_revision: Union[str, None] = '6ed7265ab218'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    
    # Create Address table first since it's referenced by Property
    op.create_table('address',
    sa.Column('id', sa.String(255), primary_key=True),
    sa.Column('street_address', sa.String(255)),
    sa.Column('city', sa.String(255)),
    sa.Column('state', sa.String(255)),
    sa.Column('postal_code', sa.String(255)),
    sa.Column('country', sa.String(255)),
    sa.Column('long_lat_location', sa.String(255)),
    schema='zimba_rei_micro'
    )

    # Create Property table
    op.create_table('property',
        sa.Column('id', sa.String(255), primary_key=True),
        sa.Column('address_id', sa.String(255), sa.ForeignKey('zimba_rei_micro.address.id')),
        schema='zimba_rei_micro'
    )

    # # Create Subscription table
    # op.create_table('subscription',
    #     sa.Column('id', sa.String(255), primary_key=True, nullable=False),
    #     sa.Column('email', sa.String(255), nullable=False),
    #     sa.Column('name', sa.String(255)),
    #     sa.Column('service_subscribed_to', sa.String(255)),
    #     sa.Column('source_url', sa.String(255)),
    #     sa.Column('subscribed', sa.Boolean),
    #     sa.Column('form_id', sa.String(255)),
    #     sa.Column('unsubscribed_date', sa.TIMESTAMP, server_default=sa.text('CURRENT_TIMESTAMP')),
    #     sa.Column('unsubscribe_token', sa.String(255)),
    #     sa.Column('created_date', sa.TIMESTAMP, server_default=sa.text('CURRENT_TIMESTAMP')),
        
    #     schema='zimba_rei_micro'
    # )

    # Create Deal table
    op.create_table('deal',
        sa.Column('id', sa.String(255), primary_key=True),
        sa.Column('down_payment', sa.Float),
        sa.Column('term', sa.Integer),
        sa.Column('interest_rate', sa.Float),
        sa.Column('monthly_cost', sa.Float),
        sa.Column('after_repair_value', sa.Float),
        sa.Column('time_horizon', sa.Integer),
        sa.Column('roi', sa.Float),
        sa.Column('capital_invested', sa.Float),
        sa.Column('property_value', sa.Float),
        schema='zimba_rei_micro'
    )

    # Create InvestorProfile table
    op.create_table('investor_profile',
        sa.Column('id', sa.String(255), primary_key=True),
        sa.Column('budget_min', sa.Float),
        sa.Column('budget_max', sa.Float),
        sa.Column('preferred_property', sa.String(255)),
        sa.Column('bedrooms_min', sa.Integer),
        sa.Column('bedrooms_max', sa.Integer),
        sa.Column('assigned_parking', sa.Boolean),
        sa.Column('air_conditioning_required', sa.Boolean),
        sa.Column('min_roi', sa.Float),
        
        schema='zimba_rei_micro'
    )

    # Create UnderwritingProcess table
    op.create_table('underwriting_process',
        sa.Column('id', sa.String(255), primary_key=True),
        sa.Column('investor_profile_id', sa.String(255), sa.ForeignKey('zimba_rei_micro.investor_profile.id')),
        sa.Column('property_id', sa.String(255), sa.ForeignKey('zimba_rei_micro.property.id')),
        
        schema='zimba_rei_micro'
    )

    # Create Listing table
    op.create_table('listing',
        sa.Column('id', sa.String(255), primary_key=True),
        sa.Column('property_id', sa.String(255), sa.ForeignKey('zimba_rei_micro.property.id')),
        sa.Column('beds', sa.Integer),
        sa.Column('baths', sa.Float),
        sa.Column('air_conditioning', sa.Boolean),
        sa.Column('parking_spaces', sa.Integer),
        sa.Column('balcony', sa.Boolean),
        sa.Column('hardwood_floor', sa.Boolean),
        sa.Column('dishwasher', sa.Boolean),
        sa.Column('year_built', sa.TIMESTAMP),
        sa.Column('basement', sa.Boolean),
        sa.Column('square_feet', sa.Float),
        
        
        
        schema='zimba_rei_micro'
    )

    # Create Expense table
    op.create_table('expense',
        sa.Column('id', sa.String(255), primary_key=True),
        sa.Column('property_id', sa.String(255), sa.ForeignKey('zimba_rei_micro.property.id')),
        sa.Column('type', sa.String(255)),
        sa.Column('monthly_cost', sa.Float),
        
        schema='zimba_rei_micro'
    )

    # Create Financing table
    op.create_table('financing',
        sa.Column('id', sa.String(255), primary_key=True),
        
        schema='zimba_rei_micro'
    )

    # Create Mortgage table
    op.create_table('mortgage',
        sa.Column('id', sa.String(255), primary_key=True),
        sa.Column('financing_id', sa.String(255), sa.ForeignKey('zimba_rei_micro.financing.id')),
        sa.Column('appraisal_value', sa.Float),
        sa.Column('principal', sa.Float),
        sa.Column('pre_qualified', sa.Boolean),
        sa.Column('pre_approved', sa.Boolean),
        sa.Column('loan_to_value', sa.Float),
        sa.Column('term', sa.Integer),
        sa.Column('amortization', sa.Integer),
        sa.Column('monthly_payment', sa.Float),
        sa.Column('owner_occupied', sa.Boolean),
        sa.Column('insurance', sa.Float),
        
        schema='zimba_rei_micro'
    )

def downgrade() -> None:
    # Drop tables in reverse order to avoid foreign key conflicts
    op.drop_table('mortgage', schema='zimba_rei_micro')
    op.drop_table('financing', schema='zimba_rei_micro')
    op.drop_table('expense', schema='zimba_rei_micro')
    op.drop_table('listing', schema='zimba_rei_micro')
    op.drop_table('underwriting_process', schema='zimba_rei_micro')
    op.drop_table('investor_profile', schema='zimba_rei_micro')
    op.drop_table('deal', schema='zimba_rei_micro')
    # op.drop_table('subscription', schema='zimba_rei_micro')
    op.drop_table('property', schema='zimba_rei_micro')
    op.drop_table('address', schema='zimba_rei_micro')
    