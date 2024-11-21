from datetime import datetime

from app.domain.Listing import Listing


def test_init_from_schema(get_test_listing_schema):
    test_listing_schema = get_test_listing_schema
    listing = Listing(**get_test_listing_schema.dict())
    assert test_listing_schema.listing_date == listing.listing_date
