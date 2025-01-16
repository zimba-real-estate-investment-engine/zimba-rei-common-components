import copy
from datetime import datetime

from app.services.AddressService import AddressService
from app.services.DropdownOptionService import DropdownOptionService


# def test_save_address(get_test_db, get_test_address_schema):
#     db = get_test_db
#     test_address = get_test_address_schema
# 
#     dropdown_option_service = AddressService(db)
# 
#     newly_saved_address = dropdown_option_service.save_address(test_address)
# 
#     # db.commit() Only commit if you want to actually save in db.
#     assert newly_saved_address


def test_get_all_optimistic(get_test_db, get_test_address_schema):
    db = get_test_db

    dropdown_option_service = DropdownOptionService(db)

    dropdown_options = dropdown_option_service.get_all()

    assert len(dropdown_options) >= 3   # There must be at least 2 records

    # This list might get too big for testing
    assert len(dropdown_options) < 10000, f'We want to make sure this list is too long for testing purposes'


def test_get_by_dropdown_name(get_test_db):
    db = get_test_db
    dropdown_name = "real_estate_property_monthly_cashflow"

    dropdown_option_service = DropdownOptionService(db)
    option_list = dropdown_option_service.get_by_dropdown_name(dropdown_name=dropdown_name)

    assert len(option_list) > 3

    for option in option_list:
        assert option.dropdown_name == dropdown_name
