from app.domain.Deal import Deal
from app.domain.InvestorProfile import InvestorProfile
from app.domain.RealEstateProperty import RealEstateProperty


def test_deal(get_test_deal_schema, get_current_time_in_seconds_string, get_test_underwriting_schema):
    deal_data = get_test_deal_schema
    deal_data.underwriting = get_test_underwriting_schema

    deal = Deal(**deal_data.dict())

    assert deal


def test_deal_from_real_estate_property_and_investor_profile(get_test_real_state_property_schema_unpopulated,
                                                             get_test_investor_profile_schema):
    real_estate_property = RealEstateProperty(**get_test_real_state_property_schema_unpopulated.dict())
    investor_profile = InvestorProfile(**get_test_investor_profile_schema.dict())

    deal = Deal.from_real_estate_and_investor_profile(real_estate_property=real_estate_property,
                                                      investor_profile=investor_profile)

    assert deal  # we need to test that conditional instantiation works OK.
