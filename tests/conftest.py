from datetime import datetime, timezone, timedelta

from dateutil.relativedelta import relativedelta

from rei_models import Listing
from rei_models import Deal
# from rei_models.rei_models.Underwriting import Underwriting
# from rei_models.rei_models.Mortgage import Mortgage

import pytest


@pytest.fixture
def get_current_time_in_seconds_string() -> str:
    return __get_time_string()


@pytest.fixture
def get_test_listing_object() -> Listing:
    current_time_string = __get_time_string()
    listing = Listing(id=current_time_string, price=300000, email="email@example.com",
                      year_built=datetime(2000, 1, 1), baths=3,
                      listing_date=datetime(2024, 4, 1),
                      square_feet=2500)
    return listing


# @pytest.fixture
# def get_test_investor_profile_object() -> InvestorProfile:
#     current_time_string = __get_time_string()
#     f_name = "fname" + current_time_string
#     l_name = "lname" + current_time_string
#
#     investor_profile = InvestorProfile(
#         id=current_time_string, price=300000, first_name=f_name, last_name=l_name,
#         email="email@example.com", title="Ms.", phone="1-888-454-1234",
#         preferred_property_type="rental", preferred_locations=["SE", "NE"],
#         bedrooms_max=8, bedrooms_min=2, bathrooms_min=2, bathrooms_max=3, budget_max=100000000, budget_min=200000,
#         years_built_max=80, years_built_min=30, investment_purpose="rental",
#         assigned_parking_required=True, central_heat_required=True, dishwasher_required=True,
#         balcony_required=True
#     )
#     return investor_profile
#

@pytest.fixture
def get_test_deal_object() -> Deal:
    current_time_string = __get_time_string()
    deal_date = datetime.now()
    closing_date = datetime.now() + relativedelta(months=3)
    underwriting_date = datetime.now() + relativedelta(months=2)

    deal = Deal(
        id=current_time_string, listing_id=current_time_string, investor_id=current_time_string,
        deal_date=deal_date , deal_status="open", offer_price=300000, sale_price=350000,
        closing_date=closing_date, underwriting_id=current_time_string,
        appraisal_value=320000, loan_amount=240000, loan_to_value=0.8,
        underwriting_date=underwriting_date, approval_status="approved", risk_assessment="low", thumbnail="example.com",
    )
    return deal

# @pytest.fixture
# def get_test_underwriting_object() -> Underwriting:
#     current_time_string = __get_time_string()
#     underwriting_date = datetime.now() + relativedelta(months=2)
#
#     underwriting = Underwriting(
#         underwriting_id=current_time_string, appraisal_value=320000, loan_amount=240000,
#         loan_to_value=0.8, interest_rate=5, underwriting_date=underwriting_date,
#         approval_status="approved", risk_assessment="low",
#     )
#
#     return underwriting
#
# @pytest.fixture
# def get_test_mortgage_object() -> Mortgage:
#     current_time_string = __get_time_string()
#     issued_date = datetime.now()
#
#     mortgage = Mortgage(
#         id=current_time_string, appraisal_value=300000.00, principal=240000.03, issued_date=issued_date,
#         pre_qualifid=True, pre_approved=True, loan_to_value=80.0, interest_rate=3.75,
#         term=timedelta(days=3 * 365), amortization_period=timedelta(days=30 * 365), monthly_payment=3565.25,
#         owner_occupied=True, insurance=3500.75,
#     )
#     return mortgage


def __get_time_string() -> str:
    current_time = datetime.now(timezone.utc)
    mills = int(current_time.timestamp())
    return str(mills)
