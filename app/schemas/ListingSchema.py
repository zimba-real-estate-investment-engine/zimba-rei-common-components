from typing import Optional

from pydantic import BaseModel, EmailStr
from datetime import datetime


class ListingSchema(BaseModel):
    id: str
    price: float
    email: Optional[EmailStr]
    year_built: datetime
    baths: int
    listing_date: datetime
    square_feet: int
    #TODO more to be added from data dictionary
