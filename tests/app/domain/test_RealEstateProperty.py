from datetime import datetime

from app.domain.InvestorProfile import InvestorProfile
from app.domain.RealEstateProperty import RealEstateProperty
from app.schemas.RealEstatePropertySchema import RealEstatePropertySchema


# def test_init_from_schema(get_test_investor_profile_schema):
#     test_investor_profile_schema = get_test_investor_profile_schema
#     investor_profile = InvestorProfile(**test_investor_profile_schema.dict())
#     assert test_investor_profile_schema.email == investor_profile.email


def test_real_estate_property_init(get_test_address_schema, get_test_expense_schema, get_test_listing_schema):

    test_listings = [get_test_listing_schema]
    test_target_listing = get_test_listing_schema
    test_expenses = [get_test_expense_schema]

    test_real_estate_property_schema \
        = RealEstatePropertySchema(listings=test_listings, expenses=test_expenses, target_listing=test_target_listing)

    real_estate_property = RealEstateProperty(**test_real_estate_property_schema.dict())

    assert len(real_estate_property.listings) > 0
    assert real_estate_property.expenses[0].monthly_cost == test_expenses[0].monthly_cost

