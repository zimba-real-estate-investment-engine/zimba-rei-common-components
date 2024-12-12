from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AmortizationScheduleSchema(BaseModel):
    id: Optional[int] = None
    amortization_schedule_json: str = ''
    created_date: Optional[datetime] = None
    caching_code: Optional[str] = None
    principal: float
    annual_interest_rate: float
    amortization_period: int

    class Config:
        orm_mode = True
        from_attributes = True
