from datetime import datetime

from app.domain.UnderwritingProcess import UnderwritingProcess

def test_extract_listing_from_json(test_sample_listing_openai_response_json_string):
    json_string = test_sample_listing_openai_response_json_string
    listing = UnderwritingProcess.extract_listing_from_json(json_string)

    assert listing.address.street_address == '1215 KLONDIKE ROAD'
    assert listing.address.city == 'Ottawa'
    assert listing.address.postal_code == 'K2W1E1'

    assert listing.price == 799900
    assert listing.year_built.year == 1970 # there is a problem converting this from 1960 TBD


def test_extract_listing_from_url():
    # url = 'https://www.realtor.com/realestateandhomes-detail/2551-Princeton-Dr_San-Bruno_CA_94066_M21198-61175'
    # url = "https://www.compass.com/listing/380-harrison-avenue-unit-1108-boston-ma-02118/1725626025069056057/"
    url = 'https://www.redfin.ca/on/ottawa/9-Camwood-Cres-K2H-7X1/home/151024056'
    listing = UnderwritingProcess.extract_listing_from_url(url)
    assert listing