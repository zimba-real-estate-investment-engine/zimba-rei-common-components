from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel

from app.schemas.AmortizationScheduleSchema import AmortizationScheduleSchema
from app.schemas.DealSchema import DealSchema


class ProjectionSchema(BaseModel):
    id: Optional[int] = None
    projection_json: Optional[str] = ''
    created_date: Optional[datetime] = None
    deal: Optional[DealSchema] = None
    amortization_schedule: Optional[AmortizationScheduleSchema] = None
    property_value: Optional[float] = None
    passive_appreciation_percentage: Optional[float] = None
    active_appreciation: Optional[float] = None

    class Config:
        orm_mode = True
        from_attributes = True


class ProjectionFindByDealSchema(BaseModel):
    deal_id: int

