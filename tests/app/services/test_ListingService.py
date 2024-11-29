from app.services.ListingService import ListingService
from app.services.SubscriptionService import SubscriptionService


def test_save_listing(get_test_db, get_test_listing_schema, get_test_address_schema):
    db = get_test_db
    test_listing = get_test_listing_schema
    test_listing.address = get_test_address_schema

    listing_service = ListingService(db)

    newly_saved_listing = listing_service.save_listing(test_listing)

    # db.commit() Only commit if you want to actually save in db.
    assert newly_saved_listing
    # assert newly_saved_listing.unsubscribe_token != test_listing.unsubscribe_token  # Generated at saving
