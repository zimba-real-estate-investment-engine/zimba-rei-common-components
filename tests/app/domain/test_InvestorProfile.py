from datetime import datetime

from app.domain.InvestorProfile import InvestorProfile
from app.domain.Mortgage import Mortgage


def test_init_from_schema(get_test_investor_profile_schema):
    test_investor_profile_schema = get_test_investor_profile_schema
    investor_profile = InvestorProfile(**test_investor_profile_schema.dict())
    assert test_investor_profile_schema.email == investor_profile.email


def test_mortgage_is_accessible(get_test_investor_profile_schema, get_test_mortgage_schema):
    test_investor_profile_schema = get_test_investor_profile_schema
    investor_profile = InvestorProfile(**test_investor_profile_schema.dict())
    test_mortgage_schema = get_test_mortgage_schema
    test_mortgage = Mortgage(**test_mortgage_schema.dict())
    investor_profile.add_mortgage(test_mortgage)

    mortgage = investor_profile.get_mortgages()[0]
    assert mortgage.amortization_period == test_mortgage.amortization_period
