from app.database.models import AddressModel
from app.repositories.BaseRepository import BaseRepository
from app.database.models import SubscriptionModel


def test_crud_subscription_model(get_test_address_model, get_test_db):
    session = get_test_db
    new_address_model = get_test_address_model

    repo = BaseRepository[AddressModel](session, AddressModel)

    # CREATE
    results = repo.add(new_address_model)
    assert results
    session.flush()

    # READ
    newly_created = repo.get_by_id(results.id)
    assert newly_created.id == results.id
    assert newly_created.state == results.state

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
