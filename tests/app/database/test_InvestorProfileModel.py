from app.database.models import AddressModel, InvestorProfileModel
from app.repositories.BaseRepository import BaseRepository
from app.database.models import SubscriptionModel


def test_crud_investor_profile_model(get_test_investor_profile_model, get_test_db):
    session = get_test_db
    new_investor_profile_model = get_test_investor_profile_model

    repo = BaseRepository[InvestorProfileModel](session, InvestorProfileModel)

    # CREATE
    results = repo.add(new_investor_profile_model)
    assert results
    session.commit()

    # READ
    newly_created = repo.get_by_id(results.id)
    assert newly_created.id == results.id
    assert newly_created.central_heat_required == results.central_heat_required

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
