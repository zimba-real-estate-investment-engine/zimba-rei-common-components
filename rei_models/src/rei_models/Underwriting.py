from pydantic import BaseModel
from datetime import datetime


class Underwriting(BaseModel):
    underwriting_id: str
    appraisal_value: int
    loan_amount: int
    loan_to_value: float
    interest_rate: float
    underwriting_date: datetime
    approval_status: str
    risk_assessment: str
    #TODO more to be added from data dictionary as necessary
