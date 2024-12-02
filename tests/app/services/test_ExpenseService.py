import copy
from datetime import datetime

from app.database.models import RealEstatePropertyModel
from app.repositories.BaseRepository import BaseRepository
from app.services.ExpenseService import ExpenseService
from app.services.RealEstatePropertyService import RealEstatePropertyService


def test_save_expense(get_test_db, get_test_expense_schema):
    db = get_test_db
    test_expense = get_test_expense_schema

    expense_service = ExpenseService(db)
    newly_saved_expense = expense_service.save_expense(test_expense)

    # db.commit() Only commit if you want to actually save in db.

    assert newly_saved_expense.id and newly_saved_expense.id != 0


def test_get_all(get_test_db, get_test_expense_schema):
    db = get_test_db
    test_expense_1 = get_test_expense_schema
    test_expense_2 = copy.deepcopy(test_expense_1)

    expense_service = ExpenseService(db)

    newly_saved_expense_1 = expense_service.save_expense(test_expense_1)
    newly_saved_expense_2 = expense_service.save_expense(test_expense_2)

    assert newly_saved_expense_1.id and newly_saved_expense_1.id != 0
    assert newly_saved_expense_2.id and newly_saved_expense_2.id != 0

    expenses_list = expense_service.get_all()

    assert len(expenses_list) >= 2

    # We don't want this list to grow tooo long for testing
    assert len(expenses_list) < 20000

