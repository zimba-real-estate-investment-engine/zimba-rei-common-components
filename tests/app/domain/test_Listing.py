from datetime import datetime

from app.domain.Listing import Listing


def test_init_from_schema_minimum(get_test_listing_schema):
    test_listing_schema = get_test_listing_schema
    listing = Listing(**test_listing_schema.dict())
    assert test_listing_schema.listing_date == listing.listing_date


def test_init_from_schema_with_address(get_test_listing_schema, get_test_address_schema):
    test_listing_schema = get_test_listing_schema
    test_address_schema = get_test_address_schema

    test_listing_schema.address = test_address_schema

    listing = Listing(**test_listing_schema.dict())
    assert listing.listing_date == test_listing_schema.listing_date
    assert listing.address.street_address == test_address_schema.street_address
