from app.database.models import RealEstatePropertyModel, ExpenseModel, InvestorProfileModel, FinancingModel
from app.repositories.BaseRepository import BaseRepository


def test_crud_financing_with_pre_existing_investor_profile(get_test_investor_profile_model,
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

    # Now create financing record
    repository = BaseRepository[FinancingModel](session, FinancingModel)
    test_financing_model.investor_profile = newly_created_investor_profile
    test_financing_model.investor_profile_id = newly_created_investor_profile.id
    results_financing_model = repository.add(test_financing_model)
    assert results_financing_model
    session.commit()
    session.flush()
    #
    # # Check that new financing record was created
    # session.begin()
    # newly_created_financing = repository.get_by_id(results_financing_model.id)
    # assert newly_created_financing





    # assert newly_created.id == results.id
    # assert newly_created.state == results.state

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


