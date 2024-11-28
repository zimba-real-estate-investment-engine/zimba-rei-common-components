from app.database.models import RealEstatePropertyModel, ExpenseModel
from app.repositories.BaseRepository import BaseRepository


def test_crud_expense_with_real_estate_property(get_test_real_estate_property_model,
                                                get_test_expense_model, get_test_db):
    session = get_test_db
    new_real_estate_property_model = get_test_real_estate_property_model
    new_expense_model = get_test_expense_model

    new_expense_model_2 = ExpenseModel(id=0,expense_type='gardening', monthly_cost=3434.33)
    new_expense_model_3 = ExpenseModel(id=0,expense_type='property management', monthly_cost=343.33)

    # ensure multiple expenses can be populated
    new_real_estate_property_model.expenses = [new_expense_model, new_expense_model_2, new_expense_model_3]

    repo = BaseRepository[RealEstatePropertyModel](session, RealEstatePropertyModel)

    # CREATE
    results = repo.add(new_real_estate_property_model)
    assert results
    session.commit()

    # READ
    newly_created = repo.get_by_id(results.id)
    assert len(newly_created.expenses) == 3

    # Make sure new ids were assigned to the expenses when saved
    for expense in newly_created.expenses:
        assert expense.id != 0
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


