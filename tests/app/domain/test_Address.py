from app.domain.Address import Address
from app.domain.Deal import Deal


def test_address_init(get_test_address_schema):
    test_address = get_test_address_schema

    address = Address(**test_address.dict())

    assert address.street_address == test_address.street_address
