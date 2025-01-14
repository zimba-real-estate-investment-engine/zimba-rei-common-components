import copy
from datetime import datetime

from app.database.models import RealEstatePropertyModel
from app.repositories.BaseRepository import BaseRepository
from app.services.CashflowService import CashflowService
from app.services.RealEstatePropertyService import RealEstatePropertyService


def test_save_cashflow(get_test_db, get_test_cashflow_schema):
    db = get_test_db
    test_cashflow = get_test_cashflow_schema

    cashflow_service = CashflowService(db)
    newly_saved_cashflow = cashflow_service.save_cashflow(test_cashflow)

    # db.commit() Only commit if you want to actually save in db.

    assert newly_saved_cashflow.id and newly_saved_cashflow.id != 0


def test_get_all(get_test_db, get_test_cashflow_schema):
    db = get_test_db
    test_cashflow_1 = get_test_cashflow_schema
    test_cashflow_2 = copy.deepcopy(test_cashflow_1)

    cashflow_service = CashflowService(db)

    newly_saved_cashflow_1 = cashflow_service.save_cashflow(test_cashflow_1)
    newly_saved_cashflow_2 = cashflow_service.save_cashflow(test_cashflow_2)

    assert newly_saved_cashflow_1.id and newly_saved_cashflow_1.id != 0
    assert newly_saved_cashflow_2.id and newly_saved_cashflow_2.id != 0

    cashflows_list = cashflow_service.get_all()

    assert len(cashflows_list) >= 2

    # We don't want this list to grow tooo long for testing
    assert len(cashflows_list) < 20000

