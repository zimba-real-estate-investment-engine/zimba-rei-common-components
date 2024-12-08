from typing import Optional, Union

from pydantic import BaseModel, EmailStr
from datetime import datetime

from app.schemas.AddressSchema import AddressSchema


# from app.schemas.RealEstatePropertySchema import RealEstatePropertySchema


class ListingSchema(BaseModel):
    id: Optional[int] = None
    price: float
    email: Optional[EmailStr] = None
    year_built: datetime
    baths: Optional[float] = None
    bathrooms: Optional[float] = None
    beds:  Optional[float] = None
    bedrooms: Optional[float] = None
    listing_date: Optional[datetime] = None
    square_feet: Optional[float] = None
    parking_spaces: Optional[Union[int, str]] = None
    air_conditioning: Optional[str] = None
    balcony: Optional[bool] = None
    basement: Optional[str] = None
    dishwasher: Optional[bool] = None
    hardwood_floor: Optional[str] = None
    address: Optional[AddressSchema] = None
    # real_estate_property: Optional[RealEstatePropertySchema] = None
    #TODO more to be added from data dictionary

    class Config:
        orm_mode = True
        from_attributes = True