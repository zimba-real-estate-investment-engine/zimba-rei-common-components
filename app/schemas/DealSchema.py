from typing import Optional

from pydantic import BaseModel

from app.domain.RealEstateProperty import RealEstateProperty
from app.schemas.UnderwritingSchema import UnderwritingSchema


class DealSchema(BaseModel):
    id: Optional[int] = None
    # down_payment: float
    # term: int
    # interest_rate: float
    # monthly_cost: float
    # after_repair_value: float
    # time_horizon: int
    # roi: float
    # capital_invested: float
    # real_estate_property_value: float
    down_payment: Optional[float] = 0
    term: int
    interest_rate: Optional[float] = 0
    monthly_cost: Optional[float] = 0
    after_repair_value: Optional[float] = 0
    time_horizon: Optional[int] = 0
    roi: Optional[float] = 0
    capital_invested: Optional[float] = 0
    real_estate_property_value: Optional[float] = 0
    real_estate_property: Optional[RealEstateProperty] = None
    underwriting: Optional[UnderwritingSchema] = None,
    thumbnail: str = '',
    risk_assessment: str = '',
    #TODO more to be added from data dictionary as necessary

    class Config:
        orm_mode = True
        from_attributes = True


class DealSearchSchema(BaseModel):
    id: int
