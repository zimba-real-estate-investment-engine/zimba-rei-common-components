from typing import Optional, List

from pydantic import BaseModel
from datetime import datetime

# from app.schemas.InvestorProfileSchema import InvestorProfileSchema
from app.schemas.MortgageSchema import MortgageSchema


class FinancingSchema(BaseModel):
    id: Optional[int] = None
    # investor_profile: InvestorProfileSchema
    mortgages: List[MortgageSchema]

    #TODO more to be added from data dictionary as necessary

    class Config:
        orm_mode = True
        from_attributes = True
