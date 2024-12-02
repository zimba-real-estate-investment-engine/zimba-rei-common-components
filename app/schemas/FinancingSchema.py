from __future__ import annotations
from typing import Optional, List

from pydantic import BaseModel

from app.schemas.MortgageSchema import MortgageSchema


class FinancingSchema(BaseModel):
    id: Optional[int] = None
    # investor_profile: Optional[InvestorProfileSchema] = None # Causes cyclical reference
    mortgages: Optional[List[MortgageSchema]] = None

    #TODO more to be added from data dictionary as necessary

    class Config:
        orm_mode = True
        from_attributes = True
