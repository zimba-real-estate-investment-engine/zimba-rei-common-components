import copy
from datetime import datetime

from app.services.RealEstatePropertyService import RealEstatePropertyService
from app.services.SubscriptionService import SubscriptionService


def test_save_real_estate_property(get_test_db, get_test_real_state_property_schema_unpopulated, get_test_address_schema):
    db = get_test_db
    test_real_estate_property = get_test_real_state_property_schema_unpopulated
    test_real_estate_property.address = get_test_address_schema

    real_estate_property_service = RealEstatePropertyService(db)

    newly_saved_real_estate_property = real_estate_property_service.save_real_estate_property(test_real_estate_property)

    db.commit()

    # db.commit() Only commit if you want to actually save in db.
    assert newly_saved_real_estate_property.id != 0


def test_get_all(get_test_db, get_test_real_state_property_schema_unpopulated, get_test_address_schema):
    db = get_test_db

    # Setup first real estate property
    test_real_estate_property_1 = get_test_real_state_property_schema_unpopulated
    test_address_1 = get_test_address_schema
    test_real_estate_property_1.address = test_address_1

    # Setup the second test real estate property
    test_real_estate_property_2 = copy.deepcopy(test_real_estate_property_1)
    test_real_estate_property_2.id = test_real_estate_property_1.id + 1
    test_address_2 = copy.deepcopy(test_address_1)
    test_address_2.id = test_address_1.id + 1
    test_address_2.street_address = 'street_address_' + str(datetime.now())

    test_real_estate_property_2.address = test_address_2

    real_estate_property_service = RealEstatePropertyService(db)

    newly_saved_real_estate_property_1 = real_estate_property_service.save_real_estate_property(test_real_estate_property_1)
    newly_saved_real_estate_property_2 = real_estate_property_service.save_real_estate_property(test_real_estate_property_2)

    assert newly_saved_real_estate_property_1
    assert newly_saved_real_estate_property_2
    db.flush()

    real_estate_properties = real_estate_property_service.get_all()

    assert len(real_estate_properties) >= 2   # There must be at least 2 records

    # This list might get too big for testing
    assert len(real_estate_properties) < 10000, f'We want to make sure this list is too long for testing purposes'

    # db.commit() Only commit if you want to actually save in db.
    # db = get_test_db
    # test_address_1 = get_test_address_schema
    # test_address_2 = get_test_address_schema.street_address = "make sure the addresses are not duplicates"
    #
    # test_real_estate_property_1 = get_test_real_estate_property_schema
    # test_real_estate_property_1.address = test_address_1
    #
    # test_real_estate_property_2 = get_test_real_estate_property_schema
    # test_real_estate_property_2.price = 1234343.22  # make sure the real_estate_propertys are not duplicates
    # test_real_estate_property_2.address = test_address_2
    #
    # real_estate_property_service = RealEstatePropertyService(db)
    #
    # newly_saved_real_estate_property_1 = real_estate_property_service.save_real_estate_property(test_real_estate_property_1)
    # newly_saved_real_estate_property_2 = real_estate_property_service.save_real_estate_property(test_real_estate_property_2)
    #
    # db.flush()
    #
    # real_estate_propertys = real_estate_property_service.get_all()
