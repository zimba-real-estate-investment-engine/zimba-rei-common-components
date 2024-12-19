from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel

from app.schemas.DealSchema import DealSchema


class ProjectionSchema(BaseModel):
    id: Optional[int] = None
    projection_json: Optional[str] = ''
    created_date: Optional[datetime] = None
    caching_code: Optional[str] = None
    deal: Optional[DealSchema] = None

    class Config:
        orm_mode = True
        from_attributes = True
