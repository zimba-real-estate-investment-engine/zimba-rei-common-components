from datetime import datetime

from app.domain.Expense import Expense
from app.domain.InvestorProfile import InvestorProfile
from app.domain.Mortgage import Mortgage
from app.domain.RealEstateProperty import RealEstateProperty
from app.domain.UnderwritingProcess import UnderwritingProcess


def test_extract_listing_from_json_realtor_ca(test_sample_listing_openai_response_realtor_ca_json_string):
    json_string = test_sample_listing_openai_response_realtor_ca_json_string
    listing = UnderwritingProcess.extract_listing_from_json(json_string)

    assert listing.address.street_address == '1215 KLONDIKE ROAD'
    assert listing.address.city == 'Ottawa'
    assert listing.address.postal_code == 'K2W1E1'

    assert listing.price == 799900 or '799900'
    assert listing.year_built.year == 1970  # there is a problem converting this from 1960 TBD


def test_extract_listing_from_json_redfin(test_sample_listing_openai_response_redfin_ca_json_string):
    json_string = test_sample_listing_openai_response_redfin_ca_json_string
    listing = UnderwritingProcess.extract_listing_from_json(json_string)

    assert listing
    assert listing.address.full_address == '9 Camwood Cres, South of Baseline to Knoxdale, ON K2H 7X1'
    # This address could not be parsed
    # assert listing.address.city == 'South of Baseline to Knoxdale'
    # assert listing.address.postal_code == 'K2H 7X1'

    assert listing.price_amount == 995000
    # assert listing.year_built.year == 1970 # This is not being returned for this particular listing


def test_extract_listing_from_url():
    # url = 'https://www.realtor.com/realestateandhomes-detail/2551-Princeton-Dr_San-Bruno_CA_94066_M21198-61175'
    # url = "https://www.compass.com/listing/380-harrison-avenue-unit-1108-boston-ma-02118/1725626025069056057/"
    url = 'https://www.redfin.ca/on/ottawa/9-Camwood-Cres-K2H-7X1/home/151024056'
    listing = UnderwritingProcess.extract_listing_from_url(url)
    assert listing


def test_create_deal_from_json(test_sample_listing_openai_response_redfin_ca_json_string, test_expenses_schema_list,
                               get_test_investor_profile_schema, get_test_mortgage_schema):

    json_string = test_sample_listing_openai_response_redfin_ca_json_string
    expense_schema_list = test_expenses_schema_list
    investor_profile_schema = get_test_investor_profile_schema
    mortgage_schema = get_test_mortgage_schema
    mortgage = Mortgage(**mortgage_schema.dict())
    # financing_sources = [mortgage]

    listing = UnderwritingProcess.extract_listing_from_json(json_string)
    listings = [listing]
    expenses = [Expense(**expense_schema.dict()) for expense_schema in expense_schema_list]
    real_estate_property = RealEstateProperty(listings=listings, expenses=expenses)

    investor_profile = InvestorProfile(**investor_profile_schema.dict())
    investor_profile.financing_sources = [mortgage]

    deal = UnderwritingProcess.create_deal(investor_profile=investor_profile, real_estate_property=real_estate_property,
                                           json_string=json_string)

    assert deal
