from pydantic import BaseModel
from datetime import datetime, timedelta


class MortgageSchema(BaseModel):
    id: str
    appraisal_value: float
    principal: float
    issued_date: datetime
    pre_qualifid: bool
    pre_approved: bool
    loan_to_value: float
    interest_rate: float
    term: timedelta
    amortization_period: timedelta
    monthly_payment: float
    owner_occupied: bool
    insurance: float
    #TODO more to be added from data dictionary as necessary
