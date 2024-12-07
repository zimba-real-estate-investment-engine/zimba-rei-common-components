import os

from dotenv import load_dotenv

from app.services.OpenAIService import OpenAIService


def test_extract_listing(test_sample_raw_text):
    # entities_to_extract = ['address', 'price', 'bedrooms', 'bathrooms', 'square_footage', 'listing_type']
    load_dotenv()
    entities_to_extract = os.getenv('ENTITIES_TO_EXTRACT').strip().split(',')
    response = OpenAIService.extract_listing_details(test_sample_raw_text, entities_to_extract)
    assert response
    assert entities_to_extract

