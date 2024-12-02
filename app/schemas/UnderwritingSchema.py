from typing import Optional

from pydantic import BaseModel
from app.schemas.InvestorProfileSchema import InvestorProfileSchema
from app.schemas.RealEstatePropertySchema import RealEstatePropertySchema


class UnderwritingSchema(BaseModel):
    id: Optional[int] = None
    real_estate_property: Optional[RealEstatePropertySchema] = None
    investor_profile: Optional[InvestorProfileSchema] = None
    #TODO more to be added from data dictionary as necessary

    class Config:
        orm_mode = True
        from_attributes = True