from typing import Optional, List

from pydantic import BaseModel


class CapitalInvestmentSchema(BaseModel):
    id: Optional[int] = None
    capital_investment_type: str
    capital_investment_amount: float
    #TODO more to be added from data dictionary as necessary

    class Config:
        orm_mode = True
        from_attributes = True
