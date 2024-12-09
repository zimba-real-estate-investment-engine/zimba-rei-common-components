from typing import Optional, Union

from pydantic import BaseModel, EmailStr, validator
from datetime import datetime

from app.schemas.AddressSchema import AddressSchema


class ListingSchema(BaseModel):
    id: Optional[int] = None
    price: Union[int, str, float]
    price_amount: Optional[Union[float, str]] = None
    price_currency_symbol: Optional[str] = None
    price_currency_iso_code: Optional[str] = None
    email: Optional[EmailStr] = None
    year_built: Union[datetime, str]
    baths: Optional[float] = None
    bathrooms: Optional[float] = None
    beds:  Optional[float] = None
    bedrooms: Optional[float] = None
    listing_date: Optional[datetime] = None
    listing_source: Optional[str] = None
    square_feet: Optional[Union[float, str]] = None
    parking_spaces: Optional[Union[int, str]] = None
    air_conditioning: Optional[str] = None
    balcony: Optional[bool] = None
    basement: Optional[str] = None
    dishwasher: Optional[bool] = None
    hardwood_floor: Optional[str] = None
    address: Optional[AddressSchema] = None
    # real_estate_property: Optional[RealEstatePropertySchema] = None
    #TODO more to be added from data dictionary

    @validator("year_built", pre=True, always=True)
    def validate_year_built(cls, value):
        if not value:
            return datetime(1200, 12, 31, 12, 0, 0)
        return value

    class Config:
        orm_mode = True
        from_attributes = True