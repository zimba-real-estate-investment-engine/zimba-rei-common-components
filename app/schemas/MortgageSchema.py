from typing import Optional

from pydantic import BaseModel
from datetime import datetime, timedelta

from app.schemas.AmortizationScheduleSchema import AmortizationScheduleSchema


class MortgageSchema(BaseModel):
    id: Optional[int] = None
    appraisal_value: float
    down_payment: Optional[float] = 0
    principal: Optional[float] = 800000
    issued_date: datetime
    pre_qualified: bool
    pre_approved: bool
    loan_to_value: float
    interest_rate: Optional[float] = 5
    term: Optional[int] = 5
    amortization_period:  Optional[int] = 30
    monthly_payment: float
    owner_occupied: bool
    insurance: float
    amortization_schedule: AmortizationScheduleSchema
    #TODO more to be added from data dictionary as necessary

    class Config:
        orm_mode = True
        from_attributes = True