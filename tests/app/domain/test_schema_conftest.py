# from tests.conftest import get_current_time_in_seconds_string

def test_get_test_listing_schema(get_test_listing_schema):
    assert get_test_listing_schema.square_feet != 0;
    assert get_test_listing_schema.listing_date is not None
#
#
# def test_investor_profile_schema(get_test_investor_profile_schema):
#     assert get_test_investor_profile_schema.first_name;
#     assert get_test_investor_profile_schema.last_name;
#
#
# def test_deal_schema(get_test_deal_schema):
#     assert get_test_deal_schema.deal_date
#
#
# def test_mortgage_schema(get_test_mortgage_schema):
#     assert get_test_mortgage_schema.principal
#     assert get_test_mortgage_schema.issued_date
#
#
# def test_underwriting_schema(get_test_underwriting_schema):
#     assert get_test_underwriting_schema.underwriting_date
#     assert get_test_underwriting_schema.approval_status
#
#
# def test_subscription_schema(get_test_subscription_schema):
#     assert get_test_subscription_schema.email
#     assert get_test_subscription_schema.form_id
