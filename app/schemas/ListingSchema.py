from typing import Optional

from pydantic import BaseModel, EmailStr
from datetime import datetime

# from app.schemas.RealEstatePropertySchema import RealEstatePropertySchema


class ListingSchema(BaseModel):
    id: Optional[int] = None
    price: float
    email: Optional[EmailStr]
    year_built: datetime
    baths: float
    beds: float
    listing_date: Optional[datetime] = None
    square_feet: float
    parking_spaces: Optional[str] = None
    air_conditioning: bool
    balcony: Optional[bool]
    basement: Optional[str] = None
    dishwasher: Optional[bool] = None
    hardwood_floor: Optional[str] = None
    # real_estate_property: Optional[RealEstatePropertySchema] = None
    #TODO more to be added from data dictionary

