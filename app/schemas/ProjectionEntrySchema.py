from typing import Optional

from pydantic import BaseModel

from app.schemas.UnderwritingSchema import UnderwritingSchema


class ProjectionEntrySchema(BaseModel):
    id: Optional[int] = None
    projection_type: str
    projection_value: float
    projection_position_in_list: int
    underwriting: Optional[UnderwritingSchema] = None
    #TODO more to be added from data dictionary as necessary

    class Config:
        orm_mode = True
        from_attributes = True

class ProjectionEntrySearchSchema(BaseModel):
    id: int