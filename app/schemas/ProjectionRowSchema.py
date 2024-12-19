import json
from typing import Optional

from pydantic import BaseModel


class ProjectionRowSchema(BaseModel):
    id: Optional[int] = None
    projection_position: int
    monthly_value: float
    mortgage_value: float
    monthly_cashflow: float
    principal_recapture: float
    passive_appreciation: float

    #TODO more to be added from data dictionary as necessary

    class Config:
        orm_mode = True
        from_attributes = True
