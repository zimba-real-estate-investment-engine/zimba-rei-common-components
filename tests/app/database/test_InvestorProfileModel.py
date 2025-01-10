import copy

from app.database.models import AddressModel, InvestorProfileModel, FinancingModel
from app.repositories.BaseRepository import BaseRepository
from app.database.models import SubscriptionModel


def test_crud_investor_profile_model(get_test_investor_profile_model, get_test_db):
    session = get_test_db
    new_investor_profile_model = get_test_investor_profile_model

    repo = BaseRepository[InvestorProfileModel](session, InvestorProfileModel)

    # CREATE
    results = repo.add(new_investor_profile_model)
    assert results
    session.flush()

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


def test_crud_investor_profile_cascade_to_financing(get_test_investor_profile_model, get_test_db,
                                                    get_test_financing_model_minimum):
    session = get_test_db
    test_investor_profile_model = get_test_investor_profile_model

    financing_source_1 = get_test_financing_model_minimum
    financing_source_2 = copy.deepcopy(financing_source_1)
    financing_source_3 = copy.deepcopy(financing_source_1)

    test_investor_profile_model.financing_sources = [financing_source_1, financing_source_2, financing_source_3]

    repo = BaseRepository[InvestorProfileModel](session, InvestorProfileModel)

    # CREATE
    results = repo.add(test_investor_profile_model)
    assert results
    session.flush()

    # READ
    newly_created = repo.get_by_id(results.id)
    assert newly_created.id == results.id
    assert len(newly_created.financing_sources) == 3

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


def test_crud_investor_profile_cascade_to_mortgage(get_test_investor_profile_model, get_test_db,
                                                   get_test_mortgage_model, get_test_financing_model_minimum,
                                                   test_amortization_schedule_model_without_json):
    session = get_test_db
    test_investor_profile_model = get_test_investor_profile_model
    test_mortgage_model = get_test_mortgage_model
    test_mortgage_model.amortization_schedule = test_amortization_schedule_model_without_json

    test_financing_source = get_test_financing_model_minimum
    test_financing_source.mortgages = [test_mortgage_model]

    test_investor_profile_model.financing_sources = [test_financing_source]

    repository = BaseRepository[InvestorProfileModel](session, InvestorProfileModel)

    # CREATE
    results = repository.add(test_investor_profile_model)
    assert results
    session.flush()
    session.commit()

    # READ
    newly_created = repository.get_by_id(results.id)
    # assert newly_created.id == results.id
    # assert len(newly_created.financing_sources) == 3

    # DELETE and commit, we'll need to clean up test data
    # # repository.delete(results.id)
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
