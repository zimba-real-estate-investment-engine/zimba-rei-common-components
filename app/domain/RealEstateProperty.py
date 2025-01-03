from typing import Optional, List, Any

from app.domain.Address import Address
from app.domain.Expense import Expense
from app.domain.Listing import Listing
from app.schemas.RealEstatePropertySchema import RealEstatePropertySchema


class RealEstateProperty(RealEstatePropertySchema):
    pass
    # def __init__(self, /, listing: Optional[List[Listing]] = None,
    #              expenses: Optional[List[Expense]] = None, address: Optional[Address] = None, **data: Any):
    #     super().__init__(**data)
    #     self.expenses = expenses
    #     self.listings = listings
    #     self.address = address

    def get_total_monthly_cashflow(self):
        cashflow_sources = self.cashflow_sources

        total_cashflow = sum(obj.monthly_cashflow for obj in cashflow_sources)

        return total_cashflow


