from itertools import chain
from typing import List

from app.domain.Financing import Financing
from app.domain.Mortgage import Mortgage
from app.schemas.InvestorProfileSchema import InvestorProfileSchema


class InvestorProfile(InvestorProfileSchema):

    def add_mortgage(self, mortgage: Mortgage):
        financing = Financing()
        financing.mortgages = [mortgage]

        if self.financing_sources is None:
            self.financing_sources = [financing]
        else:
            financing_source = self.financing_sources[0]  # we'll focus on first financing source for now
            if financing_source:
                financing_source.mortgages.append(mortgage)
            else:
                self.financing_sources = [financing]

    def get_mortgages(self) -> List[Mortgage]:
        mortgages: List[Mortgage] = []
        if self.financing_sources is None:
            return mortgages
        else:
            mortgages = list(chain.from_iterable(
                financing.mortgages for financing in self.financing_sources
            ))
            # for financing in self.financing_sources:
            #     financing_mortgages = financing.mortgages
            #     mortgages += financing_mortgages

            return mortgages
