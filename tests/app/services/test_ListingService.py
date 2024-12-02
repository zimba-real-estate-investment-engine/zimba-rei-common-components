import copy
from datetime import datetime

from app.services.ListingService import ListingService
from app.services.SubscriptionService import SubscriptionService


def test_save_listing(get_test_db, get_test_listing_schema, get_test_address_schema):
    db = get_test_db
    test_listing = get_test_listing_schema
    test_listing.address = get_test_address_schema

    listing_service = ListingService(db)

    newly_saved_listing = listing_service.save_listing(test_listing)

    assert newly_saved_listing.id and newly_saved_listing.id != 0

    # db.commit() Only commit if you want to actually save in db.
    assert newly_saved_listing


def test_get_all(get_test_db, get_test_listing_schema, get_test_address_schema):
    db = get_test_db

    test_address_1 = get_test_address_schema

    test_listing_1 = get_test_listing_schema
    test_listing_1.address = test_address_1

    listing_service = ListingService(db)

    newly_saved_listing_1 = listing_service.save_listing(test_listing_1)
    db.flush()

    assert newly_saved_listing_1.id and newly_saved_listing_1.id != 0

    test_address_2 = copy.deepcopy(test_address_1)
    test_address_2.street_address = '' + str(datetime.now())

    test_listing_2 = get_test_listing_schema
    test_listing_2.address = test_address_2

    newly_saved_listing_2 = listing_service.save_listing(test_listing_2)
    db.flush()

    assert newly_saved_listing_2.id and newly_saved_listing_2.id != 0

    listings = listing_service.get_all()

    assert len(listings) >= 2   # There must be at least 2 records

    # This list might get too big for testing
    assert len(listings) < 10000, f'We want to make sure this list is too long for testing purposes'

    # db.commit() Only commit if you want to actually save in db.
    # db = get_test_db
    # test_address_1 = get_test_address_schema
    # test_address_2 = get_test_address_schema.street_address = "make sure the addresses are not duplicates"
    #
    # test_listing_1 = get_test_listing_schema
    # test_listing_1.address = test_address_1
    #
    # test_listing_2 = get_test_listing_schema
    # test_listing_2.price = 1234343.22  # make sure the listings are not duplicates
    # test_listing_2.address = test_address_2
    #
    # listing_service = ListingService(db)
    #
    # newly_saved_listing_1 = listing_service.save_listing(test_listing_1)
    # newly_saved_listing_2 = listing_service.save_listing(test_listing_2)
    #
    # db.flush()
    #
    # listings = listing_service.get_all()
