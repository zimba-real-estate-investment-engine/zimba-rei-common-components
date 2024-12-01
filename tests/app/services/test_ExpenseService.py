import copy
from datetime import datetime

from app.database.models import RealEstatePropertyModel
from app.repositories.BaseRepository import BaseRepository
from app.services.ExpenseService import ExpenseService


def test_save_expense(get_test_db, get_test_expense_schema):
    db = get_test_db
    test_expense = get_test_expense_schema

    expense_service = ExpenseService(db)

    newly_saved_expense = expense_service.save_expense(test_expense)

    db.flush()
    # db.commit() Only commit if you want to actually save in db.
    assert newly_saved_expense


def test_get_all(get_test_db, get_test_expense_schema, get_test_real_estate_property_model):
    db = get_test_db

    # We need a pre-existing RealEstateProperty
    real_estate_property = get_test_real_estate_property_model
    repository = BaseRepository[RealEstatePropertyModel](db, RealEstatePropertyModel)
    pre_saved_real_estate_property = repository.add(real_estate_property)
    db.flush()
    assert pre_saved_real_estate_property
    #
    # test_expense_1 = get_test_expense_schema
    # test_expense_2 = copy.deepcopy(test_expense_1)
    # test_expense_3 = copy.deepcopy(test_expense_2)
    #
    # test_expense_2.id = get_test_expense_schema.id + 1
    # test_expense_2.street_expense = 'street_' + str(datetime.now())
    # test_expense_3.id = get_test_expense_schema.id + 2
    # test_expense_3.street_expense = 'street_' + str(datetime.now())
    #
    # expense_service = ExpenseService(db)
    #
    # newly_saved_expense_1 = expense_service.save_expense(test_expense_1)
    # newly_saved_expense_2 = expense_service.save_expense(test_expense_2)
    # newly_saved_expense_3 = expense_service.save_expense(test_expense_3)
    #
    # assert newly_saved_expense_1
    # assert newly_saved_expense_2
    # assert newly_saved_expense_3
    #
    # db.flush()
    #
    # expenses_list = expense_service.get_all()
    #
    # assert len(expenses_list) >= 3   # There must be at least 2 records
    #
    # # This list might get too big for testing
    # assert len(expenses_list) < 10000, f'We want to make sure this list is too long for testing purposes'





    # db.commit() Only commit if you want to actually save in db.
    # db = get_test_db
    # test_expense_1 = get_test_expense_schema
    # test_expense_2 = get_test_expense_schema.street_expense = "make sure the expensees are not duplicates"
    #
    # test_expense_1 = get_test_expense_schema
    # test_expense_1.expense = test_expense_1
    #
    # test_expense_2 = get_test_expense_schema
    # test_expense_2.price = 1234343.22  # make sure the expenses are not duplicates
    # test_expense_2.expense = test_expense_2
    #
    # expense_service = ExpenseService(db)
    #
    # newly_saved_expense_1 = expense_service.save_expense(test_expense_1)
    # newly_saved_expense_2 = expense_service.save_expense(test_expense_2)
    #
    # db.flush()
    #
    # expenses = expense_service.get_all()
