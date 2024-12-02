from typing import Optional, List

from pydantic import BaseModel

from app.schemas.AddressSchema import AddressSchema
from app.schemas.ExpenseSchema import ExpenseSchema
from app.schemas.ListingSchema import ListingSchema


class RealEstatePropertySchema(BaseModel):
    id: Optional[int] = None
    listing: Optional[ListingSchema] = None  # many listing sites might have the same property
    # target_listing: Optional[ListingSchema] = None  # this property that will be used in underwriting
    expenses: Optional[List[ExpenseSchema]] = None
    address: Optional[AddressSchema] = None
    #TODO more to be added from data dictionary as necessary

    class Config:
        orm_mode = True
        from_attributes = True