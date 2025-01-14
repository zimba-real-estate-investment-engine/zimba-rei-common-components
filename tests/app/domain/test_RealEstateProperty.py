from datetime import datetime

from app.domain.Cashflow import Cashflow
from app.domain.InvestorProfile import InvestorProfile
from app.domain.RealEstateProperty import RealEstateProperty
from app.schemas.RealEstatePropertySchema import RealEstatePropertySchema


# def test_init_from_schema(get_test_investor_profile_schema):
#     test_investor_profile_schema = get_test_investor_profile_schema
#     investor_profile = InvestorProfile(**test_investor_profile_schema.dict())
#     assert test_investor_profile_schema.email == investor_profile.email


def test_real_estate_property_init(get_test_address_schema, get_test_expense_schema, get_test_listing_schema):
    test_listings = [get_test_listing_schema]
    test_expenses = [get_test_expense_schema]

    test_real_estate_property_schema \
        = RealEstatePropertySchema(listing=test_listings[0], expenses=test_expenses)

    print("The dict()")
    print(test_real_estate_property_schema.dict())

    real_estate_property = RealEstateProperty(**test_real_estate_property_schema.dict())

    assert real_estate_property.listing
    # assert real_estate_property.expenses[0].monthly_cost == test_expenses[0].monthly_cost


def test_get_total_monthly_cashflow(get_test_expense_schema, get_test_listing_schema):
    value_1 = 300
    value_2 = 35.67
    value_3 = 3455.88
    cashflow_1 = Cashflow(cashflow_type='monthly_rental', monthly_cashflow=value_1)
    cashflow_2 = Cashflow(cashflow_type='monthly_parking', monthly_cashflow=value_2)
    cashflow_3 = Cashflow(cashflow_type='monthly_storage', monthly_cashflow=value_3)

    real_estate_property = RealEstateProperty(cashflow_sources=[cashflow_1, cashflow_2, cashflow_3])

    assert real_estate_property.get_total_monthly_cashflow() == (value_1 + value_2 + value_3)
