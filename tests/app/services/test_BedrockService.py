from app.services.BedrockService import BedrockService


#
# def test_extract_listing_details_from_html(test_sample_html):
#     results = LLMService.extract_listing_details(test_sample_html, content_type='html')
#     print(results)
#
#
# def test_is_inference_up():
#     results = LLMService.is_inference_up()
#     assert results
#
#
# def test_models_response():
#     models_response = LLMService.models_response()
#     assert models_response   #TODO run some more tests here

def test_extract_listing_details(test_sample_raw_text):
    response = BedrockService.extract_listing_details(test_sample_raw_text)
    assert response