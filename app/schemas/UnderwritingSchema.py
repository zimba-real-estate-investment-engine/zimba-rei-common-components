from typing import Optional

from pydantic import BaseModel, root_validator, model_validator
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


class UnderwritingCreateDealSchema(BaseModel):
    investor_profile_id: int
    real_estate_property_id: int
    listing_url: Optional[str] = None
    json_string: Optional[str] = None

    @model_validator(mode='after')
    def at_least_url_or_json_required(self):
        if not self.listing_url and not self.json_string:
            raise ValueError("At least one of 'url' or 'json_string' must be defined")
        return self


class UnderwritingCreateDealFromURLSchema(BaseModel):
    investor_profile_id: int
    listing_url: str
