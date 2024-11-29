from app.database.models import AddressModel, ListingModel
from app.repositories.BaseRepository import BaseRepository
from app.database.models import SubscriptionModel


def test_crud_list_model(get_test_listing_model, get_test_db):
    session = get_test_db
    new_listing_model = get_test_listing_model

    repo = BaseRepository[ListingModel](session, ListingModel)

    # CREATE
    results = repo.add(new_listing_model)
    assert results
    session.commit()

    # READ
    newly_created = repo.get_by_id(results.id)
    assert newly_created.id == results.id

    # DELETE and commit, we'll need to clean up test data
    repo.delete(results.id)
    # session.commit()

    #
    #
    # repository.
    #
    # repository.add(test_subscription)
    #
    # id = test_subscription.id
    #
    # returned_instance = repository.get(id)
    # assert returned_instance


def test_crud_list_model_cascade_to_address(get_test_listing_model, get_test_address_model, get_test_db):
    session = get_test_db
    test_listing_model = get_test_listing_model
    test_address_model = get_test_address_model

    test_listing_model.address = test_address_model

    repo = BaseRepository[ListingModel](session, ListingModel)

    # CREATE
    results = repo.add(test_listing_model)
    assert results
    session.flush()

    # READ
    newly_created_listing = repo.get_by_id(results.id)
    assert newly_created_listing.address.street_address == test_address_model.street_address

    # DELETE and commit, we'll need to clean up test data
    # repo.delete(results.id)
    session.commit()
