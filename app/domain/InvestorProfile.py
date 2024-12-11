from typing import List

from app.domain.Financing import Financing
from app.domain.Mortgage import Mortgage
from app.schemas.InvestorProfileSchema import InvestorProfileSchema
from app.schemas.MortgageSchema import MortgageSchema


class InvestorProfile(InvestorProfileSchema):

    def add_mortgage(self, mortgage: Mortgage):
        financing = Financing()
        financing.mortgages = mortgage

        if self.financing_sources is None:
            self.financing_sources = [financing]
        else:
            self.financing_sources.append(financing)


    def get_mortgages(self) -> List[Mortgage]:
        mortgages: List[Mortgage] = []
        if self.financing_sources is None:
            return mortgages
        else:
            for financing in self.financing_sources:
                mortgages.append(financing.mortgages)

            return mortgages
