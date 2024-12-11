from typing import Optional, List, Any

from app.domain.Address import Address
from app.domain.Expense import Expense
from app.domain.Listing import Listing
from app.schemas.AddressSchema import AddressSchema
from app.schemas.RealEstatePropertySchema import RealEstatePropertySchema


class RealEstateProperty(RealEstatePropertySchema):

    def __init__(self, /, listings: Optional[List[Listing]] = None,
                 expenses: Optional[List[Expense]] = None, address: Optional[Address] = None, **data: Any):
        super().__init__(**data)
        self.expenses = expenses
        self.listings = listings
        self.address = address
