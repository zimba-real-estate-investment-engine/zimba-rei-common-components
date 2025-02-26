from app.repositories.BaseRepository import BaseRepository
from app.database.models import SubscriptionModel


def test_crud_subscription_model(get_test_subscription_model, get_test_db):
    session = get_test_db
    new_subscription_model = get_test_subscription_model

    repo = BaseRepository[SubscriptionModel](session, SubscriptionModel)

    # CREATE
    results = repo.add(new_subscription_model)
    assert results
    session.flush()

    # READ
    newly_created = repo.get_by_id(results.id)
    assert newly_created.id and newly_created.id != 0

    # Clean up. You can comment these out to create test data
    repo.delete(results.id)
    session.commit()

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
