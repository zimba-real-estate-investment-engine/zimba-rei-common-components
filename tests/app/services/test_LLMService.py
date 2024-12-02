import pytest

from app.services.LLMService import LLMService


@pytest.mark.skip(reason="Will be reviewed after adding mock")
def test_extract_listing_details_from_html(test_sample_html):
    results = LLMService.extract_listing_details(test_sample_html, content_type='html')
    print(results)


@pytest.mark.skip(reason="Will be reviewed after adding mock")
def test_is_inference_up():
    results = LLMService.is_inference_up()
    assert results


@pytest.mark.skip(reason="Will be reviewed after adding mock")
def test_models_response():
    models_response = LLMService.models_response()
    assert models_response   #TODO run some more tests here