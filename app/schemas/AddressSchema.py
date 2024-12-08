from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class AddressSchema(BaseModel):
    id: Optional[int] = None
    street_address: str
    street_address_two: Optional[str] = None
    city: str
    postal_code: str
    country: str
    long_lat_location:  Optional[str] = None
    state: str
    #TODO more to be added from data dictionary as necessary

    class Config:
        orm_mode = True
        from_attributes = True