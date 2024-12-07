from typing import List

from app.domain.Deal import Deal
from app.domain.Expense import Expense
from app.domain.InvestorProfile import InvestorProfile
from app.domain.Listing import Listing
from app.domain.RealEstateProperty import RealEstateProperty


class UnderwritingProcess():

    def create_deal(self, investor_profile: InvestorProfile, real_estate_property: RealEstateProperty) -> Deal:
        pass

    def extract_real_estate_property(self, listing: Listing, expenses: List[Expense]) -> RealEstateProperty:
        pass

    def extract_listing(self, uri: str) -> Listing:

        pass

    def _raw_text_from_url(self, uri: str) -> str:
        pass
    # def generate_underwriting(self, deal: Deal, investor: InvestorProfile,
    #                           real_estate_property: RealEstateProperty) -> Underwriting:
    #     pass
    #
    # def generate_project(self, uri: str) -> Projection:
    #     pass