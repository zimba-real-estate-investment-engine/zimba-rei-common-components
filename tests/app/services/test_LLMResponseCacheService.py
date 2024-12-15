import copy
from datetime import datetime

from app.database.models import RealEstatePropertyModel
from app.repositories.BaseRepository import BaseRepository
from app.services.CashflowService import CashflowService
from app.services.LLMResponseCacheService import LLMResponseCacheService
from app.services.RealEstatePropertyService import RealEstatePropertyService


def test_save_llm_response(get_test_db, test_llm_response_schema_no_listing_json):
    db = get_test_db
    test_llm_response = test_llm_response_schema_no_listing_json

    llm_response_service = LLMResponseCacheService(db)
    newly_saved_llm_response = llm_response_service.save_llm_response(test_llm_response)

    db.flush()
    # db.commit() Only commit if you want to actually save in db.

    assert newly_saved_llm_response.id and newly_saved_llm_response.id != 0


def test_find_by_listing_url_and_llm_service(get_test_db, test_llm_response_schema_no_listing_json):
    db = get_test_db
    test_llm_response = test_llm_response_schema_no_listing_json

    llm_response_service = LLMResponseCacheService(db)
    newly_saved_llm_response = llm_response_service.save_llm_response(test_llm_response)

    db.flush()

    # Now query after the flush
    results = llm_response_service.find_by_listing_url_and_llm_service_api_url(
        test_llm_response.listing_url,
        test_llm_response.llm_service_api_url
    )

    assert results
    assert results[0].listing_url == test_llm_response.listing_url
    assert results[0].llm_service_api_url == test_llm_response.llm_service_api_url


#
# def test_get_all(get_test_db, get_test_cashflow_schema):
#     db = get_test_db
#     test_cashflow_1 = get_test_cashflow_schema
#     test_cashflow_2 = copy.deepcopy(test_cashflow_1)
#
#     cashflow_service = CashflowService(db)
#
#     newly_saved_cashflow_1 = cashflow_service.save_cashflow(test_cashflow_1)
#     newly_saved_cashflow_2 = cashflow_service.save_cashflow(test_cashflow_2)
#
#     assert newly_saved_cashflow_1.id and newly_saved_cashflow_1.id != 0
#     assert newly_saved_cashflow_2.id and newly_saved_cashflow_2.id != 0
#
#     cashflows_list = cashflow_service.get_all()
#
#     assert len(cashflows_list) >= 2
#
#     # We don't want this list to grow tooo long for testing
#     assert len(cashflows_list) < 20000
#
