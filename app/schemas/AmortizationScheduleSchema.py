from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel

from app.schemas.AmortizationCachingCodeSchema import AmortizationCachingCodeSchema


class AmortizationScheduleSchema(BaseModel):
    id: Optional[int] = None
    amortization_schedule_json: Optional[str] = ''
    created_date: Optional[datetime] = datetime.now()
    caching_code: Optional[AmortizationCachingCodeSchema] = None
    principal: float
    annual_interest_rate: float
    amortization_period: int

    class Config:
        orm_mode = True
        from_attributes = True
