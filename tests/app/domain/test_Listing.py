from datetime import datetime

from app.domain.Listing import Listing


def test_listing(get_test_listing_schema, get_current_time_in_seconds_string):
    current_time_string = get_current_time_in_seconds_string
    listing_data = get_test_listing_schema

    listing = Listing(listing_data)

    assert listing.id == current_time_string
    assert listing.price == 300000
    assert listing.email == 'email@example.com'
    assert listing.square_feet == 2500