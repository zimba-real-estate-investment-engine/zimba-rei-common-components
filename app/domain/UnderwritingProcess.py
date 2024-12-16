import ast
import json
import logging
import os
from datetime import datetime
from typing import List

from dotenv import load_dotenv
from pydantic import ValidationError

from app.domain.Deal import Deal
from app.domain.Expense import Expense
from app.domain.InvestorProfile import InvestorProfile
from app.domain.LLMResponse import LLMResponse
from app.domain.Listing import Listing
from app.domain.RealEstateProperty import RealEstateProperty
from app.domain.llm.WebsitePreprocessor import WebsitePreprocessor
from app.services.LLMResponseCacheService import LLMResponseCacheService
from app.services.OpenAIService import OpenAIService


class UnderwritingProcess:
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)  # Set the logging level

    @staticmethod
    def create_deal(investor_profile: InvestorProfile, real_estate_property: RealEstateProperty, url: str = None,
                    json_string: str = None) -> Deal:

        if url:
            listing = UnderwritingProcess.extract_listing_from_url(url)
            real_estate_property.listing = listing
            deal = Deal.from_real_estate_and_investor_profile(real_estate_property=real_estate_property,
                                                              investor_profile=investor_profile)
            return deal

        elif json_string:
            deal = UnderwritingProcess.create_deal_from_json(investor_profile=investor_profile,
                                                             real_estate_property=real_estate_property,
                                                             json_source=json_string)
            return deal
        else:
            raise ValueError(f"url or json_string need to be specified. Both can't be None")

    @staticmethod
    def create_deal_from_json(investor_profile: InvestorProfile, real_estate_property: RealEstateProperty,
                              json_source: str) -> Deal:
        listing = UnderwritingProcess.extract_listing_from_json(json_source)
        real_estate_property = real_estate_property
        real_estate_property.listings.append(listing)
        investor_profile = investor_profile

        deal = Deal.from_real_estate_and_investor_profile(real_estate_property=real_estate_property,
                                                          investor_profile=investor_profile)
        return deal

    @staticmethod
    def extract_real_estate_property(listing: Listing, expenses: List[Expense]) -> RealEstateProperty:
        listing = listing
        expenses = expenses

        real_estate_property = RealEstateProperty(listing=listing, expenses=expenses, address=listing.address)
        return real_estate_property

    @staticmethod
    def extract_listing_from_url(uri: str) -> Listing:
        llm_json_response = None
        load_dotenv()
        llm_service_api_url = os.getenv('LLM_OPENAI_API_URL')
        raw_text = UnderwritingProcess.raw_text_from_url(uri=uri)

        # Check if search was already run
        llm_cache_service = LLMResponseCacheService()
        result = llm_cache_service.find_by_listing_url_and_llm_service_api_url(
            listing_url=uri,
            llm_service_api_url=llm_service_api_url
        )

        if result and len(result) > 0:
            pre_existing_response = result[0]
            llm_response = LLMResponse(**pre_existing_response.dict())
            llm_json_response = llm_response.llm_response_json
        else:
            llm_json_response = OpenAIService.extract_listing_details(raw_text)

        llm_json_response_string = json.dumps(llm_json_response)

        new_llm_response = LLMResponse(listing_url=uri,
                                       listing_raw_text=raw_text,
                                       llm_service_api_url=llm_service_api_url,
                                       llm_service_prompt='',
                                       llm_response_json=llm_json_response_string,
                                       created_date=datetime.now())
        llm_cache_service.save_llm_response(new_llm_response)

        listing = UnderwritingProcess.extract_listing_from_json(llm_json_response)

        return listing

    @staticmethod
    def extract_listing_from_json(json_string: str) -> Listing:
        listing_data = json_string
        # Ensure both single quote and double quote json are processed
        try:
            listing_data = json.loads(json_string)
        except json.JSONDecodeError:
            listing_data = ast.literal_eval(json_string)

        # Parse pricing
        pre_parsed_price = listing_data["price"]
        parsed_price = Listing.parse_price_and_iso_currency(pre_parsed_price)
        if parsed_price:
            listing_data['price_amount'] = parsed_price.amount
            listing_data['price_currency_symbol'] = parsed_price.currency_symbol
            listing_data['price_currency_iso_code'] = parsed_price.currency_iso_code

        address_data = listing_data['address']  # this is a string that needs parsing to create Address object
        fields_to_exclude = ["address"]  #
        filtered_data = {key: value for key, value in listing_data.items() if key not in fields_to_exclude}

        try:
            parsed_address = Listing.parse_address(address_data)
            listing = Listing(**filtered_data)
            listing.address = parsed_address[0]
            return listing
        except ValidationError as e:
            UnderwritingProcess.logger.error("Validation Error in Listing JSON Data:")
            for err in e.errors():
                UnderwritingProcess.logger.error(f"Field: {err['loc']}, Error: {err['msg']}")

    @staticmethod
    def raw_text_from_url(uri: str) -> str:
        raw_text = WebsitePreprocessor.get_text_from_url(uri)
        return raw_text
    # def generate_underwriting(self, deal: Deal, investor: InvestorProfile,
    #                           real_estate_property: RealEstateProperty) -> Underwriting:
    #     pass
    #
    # def generate_project(self, uri: str) -> Projection:
    #     pass
