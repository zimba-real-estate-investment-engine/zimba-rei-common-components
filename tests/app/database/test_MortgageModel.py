from app.database.models import RealEstatePropertyModel, ExpenseModel, InvestorProfileModel, FinancingModel, \
    MortgageModel
from app.repositories.BaseRepository import BaseRepository


def test_crud_mortgage_with_pre_existing_investor_profile_and_financing(get_test_investor_profile_model,
                                                                        get_test_financing_model_minimum,
                                                                        get_test_mortgage_model,
                                                                        get_test_db):
    session = get_test_db
    test_investor_profile_model = get_test_investor_profile_model
    test_financing_model = get_test_financing_model_minimum
    test_mortgage_model = get_test_mortgage_model

    # Build the investor profile
    test_investor_profile_model.financing_sources = [test_financing_model]

    repository = BaseRepository[InvestorProfileModel](session, InvestorProfileModel)

    # First create the investor profile
    results = repository.add(test_investor_profile_model)
    assert results
    # session.commit()
    session.flush()
    # session.close()
    #
    # session.begin()
    # READ
    newly_created_investor_profile = repository.get_by_id(results.id)
    assert newly_created_investor_profile

    # Now create mortgage record
    repository = BaseRepository[MortgageModel](session, MortgageModel)
    test_mortgage_model.financing_id = newly_created_investor_profile.financing_sources[0].id
    test_mortgage_model.financing = newly_created_investor_profile.financing_sources[0]
    results_mortgage_model = repository.add(test_mortgage_model)
    assert results_mortgage_model
    session.flush()

    # # Check that new mortgage record was created
    newly_created_mortgage = repository.get_by_id(results_mortgage_model.id)
    assert newly_created_mortgage

    session.commit()

    # DELETE and commit, we'll need to clean up test data
    # repo.delete(results.id)
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


def test_crud_financing_with_pre_existing_investor_profile_and_mortgages(
        get_test_investor_profile_model, get_test_financing_model_minimum, get_test_mortgage_model, get_test_db):
    test_investor_profile = get_test_investor_profile_model
    test_financing = get_test_financing_model_minimum
    test_mortgage = get_test_mortgage_model

    test_financing.mortgages = [test_mortgage]
    test_investor_profile.financing_sources = [test_financing]
