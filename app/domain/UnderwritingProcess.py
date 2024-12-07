from typing import List

from app.domain.Deal import Deal
from app.domain.Expense import Expense
from app.domain.InvestorProfile import InvestorProfile
from app.domain.Listing import Listing
from app.domain.RealEstateProperty import RealEstateProperty
from app.domain.llm.WebsitePreprocessor import WebsitePreprocessor
from app.services.LLMService import LLMService


class UnderwritingProcess():

    def create_deal(self, investor_profile: InvestorProfile, real_estate_property: RealEstateProperty) -> Deal:
        pass

    def extract_real_estate_property(self, listing: Listing, expenses: List[Expense]) -> RealEstateProperty:
        pass
    @staticmethod
    def extract_listing_from_url(uri: str) -> Listing:
        raw_text =UnderwritingProcess.raw_text_from_url(uri=uri)
        llm_json_response = LLMService.extract_listing_details(raw_text, 'text')
        assert llm_json_response
        # listing = Listing()
        # return listing

    @staticmethod
    def raw_text_from_url(uri: str) -> str:
        website_processor = WebsitePreprocessor(url=uri)
        raw_text = website_processor.get_raw_text()
        return raw_text
    # def generate_underwriting(self, deal: Deal, investor: InvestorProfile,
    #                           real_estate_property: RealEstateProperty) -> Underwriting:
    #     pass
    #
    # def generate_project(self, uri: str) -> Projection:
    #     pass