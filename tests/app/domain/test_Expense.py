from app.domain.Address import Address
from app.domain.Deal import Deal
from app.domain.Expense import Expense


def test_expense_init(get_test_expense_schema):
    test_expense = get_test_expense_schema

    expense = Expense(**test_expense.dict())

    assert expense.expense_type == test_expense.expense_type
