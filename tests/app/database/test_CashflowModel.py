import copy

from app.database.models import RealEstatePropertyModel, CashflowModel
from app.repositories.BaseRepository import BaseRepository


def test_crud_cashflow_with_real_estate_property(get_test_real_estate_property_model,
                                                 get_test_cashflow_model, get_test_db):
    session = get_test_db
    new_real_estate_property_model = get_test_real_estate_property_model
    new_cashflow_model = get_test_cashflow_model

    new_cashflow_model_2 = copy.deepcopy(new_cashflow_model)
    new_cashflow_model_3 = copy.deepcopy(new_cashflow_model)

    # ensure multiple cashflows can be populated
    new_real_estate_property_model.cashflow_sources = [new_cashflow_model, new_cashflow_model_2, new_cashflow_model_3]

    repo = BaseRepository[RealEstatePropertyModel](session, RealEstatePropertyModel)

    # CREATE
    results = repo.add(new_real_estate_property_model)
    assert results
    session.flush()

    # READ
    newly_created = repo.get_by_id(results.id)
    assert len(newly_created.cashflow_sources) == 3

    # Make sure new ids were assigned to the cashflows when saved
    for cashflow in newly_created.cashflow_sources:
        assert cashflow.id != 0
    # assert newly_created.id == results.id
    # assert newly_created.state == results.state

    # DELETE and commit, we'll need to clean up test data
    # repo.delete(results.id)
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
