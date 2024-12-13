import copy
from datetime import datetime

from app.database.models import RealEstatePropertyModel
from app.repositories.BaseRepository import BaseRepository
from app.services.CapitalInvestmentService import CapitalInvestmentService
from app.services.RealEstatePropertyService import RealEstatePropertyService


def test_save_capital_investment(get_test_db, get_test_capital_investment_schema):
    db = get_test_db
    test_capital_investment = get_test_capital_investment_schema

    capital_investment_service = CapitalInvestmentService(db)
    newly_saved_capital_investment = capital_investment_service.save_capital_investment(test_capital_investment)

    # db.commit() Only commit if you want to actually save in db.

    assert newly_saved_capital_investment.id and newly_saved_capital_investment.id != 0


def test_get_all(get_test_db, get_test_capital_investment_schema):
    db = get_test_db
    test_capital_investment_1 = get_test_capital_investment_schema
    test_capital_investment_2 = copy.deepcopy(test_capital_investment_1)

    capital_investment_service = CapitalInvestmentService(db)

    newly_saved_capital_investment_1 = capital_investment_service.save_capital_investment(test_capital_investment_1)
    newly_saved_capital_investment_2 = capital_investment_service.save_capital_investment(test_capital_investment_2)

    assert newly_saved_capital_investment_1.id and newly_saved_capital_investment_1.id != 0
    assert newly_saved_capital_investment_2.id and newly_saved_capital_investment_2.id != 0

    capital_investments_list = capital_investment_service.get_all()

    assert len(capital_investments_list) >= 2

    # We don't want this list to grow tooo long for testing
    assert len(capital_investments_list) < 20000

