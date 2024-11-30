import copy
from datetime import datetime

from app.services.AddressService import AddressService


def test_save_address(get_test_db, get_test_address_schema):
    db = get_test_db
    test_address = get_test_address_schema

    address_service = AddressService(db)

    newly_saved_address = address_service.save_address(test_address)

    # db.commit() Only commit if you want to actually save in db.
    assert newly_saved_address


def test_get_all(get_test_db, get_test_address_schema):
    db = get_test_db

    test_address_1 = get_test_address_schema
    test_address_2 = copy.deepcopy(test_address_1)
    test_address_3 = copy.deepcopy(test_address_2)

    test_address_2.id = get_test_address_schema.id + 1
    test_address_2.street_address = 'street_' + str(datetime.now())
    test_address_3.id = get_test_address_schema.id + 2
    test_address_3.street_address = 'street_' + str(datetime.now())

    address_service = AddressService(db)

    newly_saved_address_1 = address_service.save_address(test_address_1)
    newly_saved_address_2 = address_service.save_address(test_address_2)
    newly_saved_address_3 = address_service.save_address(test_address_3)

    assert newly_saved_address_1
    assert newly_saved_address_2
    assert newly_saved_address_3

    db.flush()

    addresss_list = address_service.get_all()

    assert len(addresss_list) >= 3   # There must be at least 2 records

    # This list might get too big for testing
    assert len(addresss_list) < 10000, f'We want to make sure this list is too long for testing purposes'





    # db.commit() Only commit if you want to actually save in db.
    # db = get_test_db
    # test_address_1 = get_test_address_schema
    # test_address_2 = get_test_address_schema.street_address = "make sure the addresses are not duplicates"
    #
    # test_address_1 = get_test_address_schema
    # test_address_1.address = test_address_1
    #
    # test_address_2 = get_test_address_schema
    # test_address_2.price = 1234343.22  # make sure the addresss are not duplicates
    # test_address_2.address = test_address_2
    #
    # address_service = AddressService(db)
    #
    # newly_saved_address_1 = address_service.save_address(test_address_1)
    # newly_saved_address_2 = address_service.save_address(test_address_2)
    #
    # db.flush()
    #
    # addresss = address_service.get_all()
