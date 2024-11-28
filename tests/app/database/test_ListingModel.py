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
