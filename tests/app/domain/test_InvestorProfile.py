from datetime import datetime

from app.domain.InvestorProfile import InvestorProfile


def test_init_from_schema(get_test_investor_profile_schema):
    test_investor_profile_schema = get_test_investor_profile_schema
    investor_profile = InvestorProfile(**test_investor_profile_schema.dict())
    assert test_investor_profile_schema.email == investor_profile.email


def test_mortgage_is_accessible(get_test_investor_profile_schema, get_test_mortgage_schema):
    test_investor_profile_schema = get_test_investor_profile_schema
    test_mortgage_schema = get_test_mortgage_schema

    test_investor_profile_schema.mortgage = test_mortgage_schema

    investor_profile = InvestorProfile(**test_investor_profile_schema.dict())

    assert investor_profile.mortgage.amortization_period == test_mortgage_schema.amortization_period
