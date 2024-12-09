from datetime import datetime

from app.domain.Listing import Listing
from app.domain.REIPrice import REIPrice


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


def test_parse_canadian_address():
    address_text = "1215 KLONDIKE ROAD, Ottawa, Ontario K2W1E1"
    addresses = Listing.parse_address(address_text, country="CA")

    address = addresses[0]
    assert address.street_address == "1215 KLONDIKE ROAD"
    assert address.city == "Ottawa"
    assert address.postal_code == "K2W1E1"


def test_parse_us_address():
    address_text = "375 Shawmut Avenue Boston, MA 02118"
    addresses = Listing.parse_address(address_text, country="US")

    address = addresses[0]
    assert address.street_address == "375 Shawmut Avenue"
    assert address.city == "Boston"
    assert address.postal_code == "02118"


def test_parse_no_country():
    address_text = "375 Shawmut Avenue Boston, MA 02118"
    addresses = Listing.parse_address(address_text)

    address = addresses[0]
    assert address.street_address == "375 Shawmut Avenue"
    assert address.city == "Boston"
    assert address.postal_code == "02118"


def test_parse_price_and_iso_currency():
    test_prices = [
        '$19.99',
        'USD$19.99',
        'US$19.99',
        '€50.00',
        '£30.50',
        '1000 ¥',
        '¥ 1000',
        'CAD$ 25.75',
        'CA$ 25.75',
        'CAD 25.75',
        'A$ 45.60',
    ]

    for price_string in test_prices:
        parsed_price = Listing.parse_price_and_iso_currency(price_string)

        assert isinstance(parsed_price, REIPrice)
        assert parsed_price.amount
        assert parsed_price.currency_symbol
        assert parsed_price.currency_iso_code
        assert parsed_price.original
