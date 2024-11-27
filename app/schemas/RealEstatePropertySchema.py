from typing import Optional, List

from pydantic import BaseModel

from app.schemas.ExpenseSchema import ExpenseSchema
from app.schemas.ListingSchema import ListingSchema


class RealEstatePropertySchema(BaseModel):
    id: Optional[int] = None
    listings: Optional[List[ListingSchema]] = None  # many listing sites might have the same property
    target_listing: Optional[ListingSchema] = None  # this property that will be used in underwriting
    # expenses: Optional[List[ExpenseSchema]] = None
    #TODO more to be added from data dictionary as necessary
