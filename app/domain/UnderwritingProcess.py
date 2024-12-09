import ast
import json
import logging
from typing import List

from pydantic import ValidationError

from app.domain.Deal import Deal
from app.domain.Expense import Expense
from app.domain.InvestorProfile import InvestorProfile
from app.domain.Listing import Listing
from app.domain.RealEstateProperty import RealEstateProperty
from app.domain.llm.WebsitePreprocessor import WebsitePreprocessor
from app.services.OpenAIService import OpenAIService


class UnderwritingProcess:
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)  # Set the logging level

    def create_deal(self, investor_profile: InvestorProfile, real_estate_property: RealEstateProperty) -> Deal:
        pass

    def extract_real_estate_property(self, listing: Listing, expenses: List[Expense]) -> RealEstateProperty:
        pass

    @staticmethod
    def extract_listing_from_url(uri: str) -> Listing:
        raw_text = UnderwritingProcess.raw_text_from_url(uri=uri)
        llm_json_response = OpenAIService.extract_listing_details(raw_text)
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
            # try:
            #     json.loads(ast_parsed)
            #     listing_data = ast_parsed
            # except Exception as e:
            #     logging.error(f'Invalid JSON {json_string}:  {e}')
            #     raise

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
