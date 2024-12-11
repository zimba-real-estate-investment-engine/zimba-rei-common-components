from typing import Any, Optional

from app.domain.InvestorProfile import InvestorProfile
from app.domain.Mortgage import Mortgage
from app.domain.RealEstateProperty import RealEstateProperty
from app.schemas.DealSchema import DealSchema


class Deal(DealSchema):

    @classmethod
    def from_real_estate_and_investor_profile(cls, real_estate_property: RealEstateProperty,
                                              investor_profile: InvestorProfile):
        cls.real_estate_property = real_estate_property
        cls.investor_profile = investor_profile

        if investor_profile.get_mortgages():
            mortgage: Mortgage = investor_profile.get_mortgages()[0]  # Initially only one mortgage per investor
            cls.down_payment = mortgage.down_payment
            cls.monthly_cost = mortgage.monthly_payment
            cls.interest_rate = mortgage.interest_rate
            cls.time_horizon = mortgage.term

        if real_estate_property.listings[0] and real_estate_property.listings[0].price_amount:
            cls.real_estate_property_value = real_estate_property.listings[0].price_amount

        return cls
