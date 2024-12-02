from pydantic import BaseModel
from datetime import datetime


class UnderwritingSchema(BaseModel):
    underwriting_id: str
    appraisal_value: int
    loan_amount: int
    loan_to_value: float
    interest_rate: float
    underwriting_date: datetime
    approval_status: str
    risk_assessment: str
    #TODO more to be added from data dictionary as necessary

    class Config:
        orm_mode = True
        from_attributes = True