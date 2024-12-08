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
        assert llm_json_response
        # listing = Listing()
        # return listing

    @staticmethod
    def extract_listing_from_json(json_string: str) -> Listing:
        listing_data = json.loads(json_string)
        address_data = listing_data['address']  # may need parsing

        fields_to_exclude = ["address"]  #

        filtered_data = {key: value for key, value in listing_data.items() if key not in fields_to_exclude}

        try:
            parsed_address = Listing.parse_address(address_data)
            listing = Listing(**filtered_data)
            listing.address = parsed_address
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
