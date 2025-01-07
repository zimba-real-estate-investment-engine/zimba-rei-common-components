import json
from typing import Optional

from pydantic import BaseModel


class ProjectionRowSchema(BaseModel):
    id: Optional[int] = None
    payment_number: int
    monthly_payment: float
    interest_payment: float
    principal_recapture: float
    remaining_balance: float
    monthly_value: float
    passive_appreciation: float
    monthly_cashflow: float

    class Config:
        orm_mode = True
        from_attributes = True