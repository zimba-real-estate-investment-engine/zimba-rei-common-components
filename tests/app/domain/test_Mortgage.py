from app.domain.Mortgage import Mortgage
from app.services.MortgageService import MortgageService


def test_init(get_test_mortgage):
    mortgage = get_test_mortgage

    assert mortgage.monthly_payment
    assert mortgage.amortization_schedule


def test_persist_with_service(get_test_db, get_test_mortgage):
    db = get_test_db
    mortgage = get_test_mortgage

    mortgage_service = MortgageService(db)
    newly_saved_mortgage = mortgage_service.save_mortgage(mortgage)
    assert newly_saved_mortgage

