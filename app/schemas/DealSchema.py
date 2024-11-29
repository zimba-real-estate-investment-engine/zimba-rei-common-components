from pydantic import BaseModel
from datetime import datetime


class DealSchema(BaseModel):
    id: str
    listing_id: str
    investor_id: str
    deal_date: datetime
    deal_status: str
    offer_price: int
    sale_price: int
    closing_date: datetime
    underwriting_id: str
    appraisal_value: float
    loan_amount: float
    loan_to_value: float
    underwriting_date: datetime
    approval_status: str
    risk_assessment: str
    thumbnail: str
    #TODO more to be added from data dictionary as necessary

    class Config:
        orm_mode = True