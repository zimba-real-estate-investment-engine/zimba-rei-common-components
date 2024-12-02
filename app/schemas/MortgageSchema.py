from typing import Optional

from pydantic import BaseModel
from datetime import datetime, timedelta


class MortgageSchema(BaseModel):
    id: Optional[int] = None
    appraisal_value: float
    principal: float
    issued_date: datetime
    pre_qualified: bool
    pre_approved: bool
    loan_to_value: float
    interest_rate: float
    term: int
    amortization_period: int
    monthly_payment: float
    owner_occupied: bool
    insurance: float
    #TODO more to be added from data dictionary as necessary

    class Config:
        orm_mode = True
        from_attributes = True