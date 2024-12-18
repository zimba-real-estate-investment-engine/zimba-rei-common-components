from typing import Optional, List

from pydantic import BaseModel

from app.domain.Cashflow import Cashflow
from app.schemas.AddressSchema import AddressSchema
from app.schemas.CapitalInvestmentSchema import CapitalInvestmentSchema
from app.schemas.ExpenseSchema import ExpenseSchema
from app.schemas.ListingSchema import ListingSchema


class RealEstatePropertySchema(BaseModel):
    id: Optional[int] = None
    # listings: Optional[List[ListingSchema]] = None  # many listing sites might have the same property
    expenses: Optional[List[ExpenseSchema]] = None
    address: Optional[AddressSchema] = None
    listing: Optional[ListingSchema] = None
    cashflow_sources: Optional[List[Cashflow]] = None
    capital_investments: Optional[List[CapitalInvestmentSchema]] = None
    #TODO more to be added from data dictionary as necessary

    class Config:
        orm_mode = True
        from_attributes = True