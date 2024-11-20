import os

from dotenv import load_dotenv
from sqlalchemy import select
from sqlalchemy.engine.cursor import CursorResult


# def test_get_test_repository(get_test_repository):
#
#     repo = get_test_repository
#     # Make sure the repo has all CRUD methods
#     expected_methods = ['add', 'get', 'update', 'delete', 'get_all']
#
#     class_methods = [m for m in dir(repo) if callable(getattr(repo, m)) and not m.startswith('_')]
#     missing_methods = set(expected_methods) - set(class_methods)
#     assert not missing_methods, f"The class is missing the following methods: {', '.join(missing_methods)}"


def test_get_test_db(get_test_db):
    db = get_test_db
    load_dotenv()
    test_db_name = os.getenv('DB_TEST_NAME')

    # Make sure the db connection is targeting the test database.
    assert test_db_name in db.bind.url

    # Make sure we can execute some test sQL
    result = db.execute(select(1))
    assert result.rowcount > 0
    assert isinstance(result, CursorResult)
    assert not result.closed


def test_get_test_listing_schema(get_test_listing_schema):
    assert get_test_listing_schema.square_feet != 0;
    assert get_test_listing_schema.listing_date is not None


def test_investor_profile_schema(get_test_investor_profile_schema):
    assert get_test_investor_profile_schema.first_name;
    assert get_test_investor_profile_schema.last_name;


def test_deal_schema(get_test_deal_schema):
    assert get_test_deal_schema.deal_date


def test_mortgage_schema(get_test_mortgage_schema):
    assert get_test_mortgage_schema.principal
    assert get_test_mortgage_schema.issued_date


def test_underwriting_schema(get_test_underwriting_schema):
    assert get_test_underwriting_schema.underwriting_date
    assert get_test_underwriting_schema.approval_status


def test_subscription_schema(get_test_subscription_schema):
    assert get_test_subscription_schema.email
    assert get_test_subscription_schema.form_id


def test_address_schema(get_test_address_schema):
    assert get_test_address_schema.street_address
    assert get_test_address_schema.street_address_two


def test_expense_schema(get_test_expense_schema):
    assert get_test_expense_schema.expense_type
