from tests.conftest import get_current_time_in_seconds_string


def test_get_current_time_in_seconds_string(get_current_time_in_seconds_string):
    assert len(get_current_time_in_seconds_string) > 0


def test_get_test_listing_object(get_test_listing_object):
    assert get_test_listing_object.square_feet != 0;
    assert get_test_listing_object.listing_date is not None


def test_investor_profile_object(get_test_investor_profile_object):
    assert get_test_investor_profile_object.first_name;
    assert get_test_investor_profile_object.last_name;


def test_deal_object(get_test_deal_object):
    assert get_test_deal_object.deal_date


def test_mortgage_object(get_test_mortgage_object):
    assert get_test_mortgage_object.principal
    assert get_test_mortgage_object.issued_date
