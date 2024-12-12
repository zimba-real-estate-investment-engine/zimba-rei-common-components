import copy

from app.database.models import RealEstatePropertyModel, CapitalInvestmentModel
from app.repositories.BaseRepository import BaseRepository


def test_crud_capital_investment_with_real_estate_property(get_test_real_estate_property_model,
                                                           get_test_capital_investment_model, get_test_db):
    session = get_test_db
    new_real_estate_property_model = get_test_real_estate_property_model
    new_capital_investment_model = get_test_capital_investment_model

    new_capital_investment_model_2 = copy.deepcopy(new_capital_investment_model)
    new_capital_investment_model_3 = copy.deepcopy(new_capital_investment_model)

    # ensure multiple capital_investments can be populated
    new_real_estate_property_model.capital_investments = [new_capital_investment_model,
                                                          new_capital_investment_model_2,
                                                          new_capital_investment_model_3]

    repo = BaseRepository[RealEstatePropertyModel](session, RealEstatePropertyModel)

    # CREATE
    results = repo.add(new_real_estate_property_model)
    assert results
    session.flush()

    # READ
    newly_created = repo.get_by_id(results.id)
    assert len(newly_created.capital_investments) == 3

    # Make sure new ids were assigned to the capital_investments when saved
    for capital_investment in newly_created.capital_investments:
        assert capital_investment.id != 0

    # DELETE and commit, we'll need to clean up test data
    # repo.delete(results.id)
    session.commit()
