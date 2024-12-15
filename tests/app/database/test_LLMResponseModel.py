import json
from datetime import datetime

from app.database.models import LLMResponseModel
from app.repositories.BaseRepository import BaseRepository


def test_llm_response_crud(test_sample_listing_openai_response_redfin_ca_json_string,
                           test_sample_raw_text, get_test_db, test_llm_response_model_no_listing_json):
    session = get_test_db

    test_llm_response = test_llm_response_model_no_listing_json
    test_llm_response.llm_response_json = test_sample_listing_openai_response_redfin_ca_json_string

    repo = BaseRepository[LLMResponseModel](session, LLMResponseModel)

    newly_created_response = repo.add(test_llm_response)
    session.flush()

    assert newly_created_response.id and newly_created_response.id != 0

    # session.commit()


