from typing import Optional

from pydantic import BaseModel
from datetime import datetime, timedelta

from app.schemas.AmortizationScheduleSchema import AmortizationScheduleSchema


class MortgageSchema(BaseModel):
    id: Optional[int] = None
    appraisal_value: Optional[float] = 0
    down_payment: Optional[float] = 0
    principal: Optional[float] = 800000
    issued_date: datetime = datetime.now()
    pre_qualified: Optional[bool] = False
    pre_approved: Optional[bool] = False
    loan_to_value: Optional[float] = None
    annual_interest_rate: float = 5
    term: Optional[int] = 5
    amortization_period:  int = 30
    monthly_payment: Optional[float] = None
    owner_occupied: bool = False
    insurance: float = 0
    amortization_schedule: Optional[AmortizationScheduleSchema] = None
    #TODO more to be added from data dictionary as necessary

    class Config:
        orm_mode = True
        from_attributes = True