from typing import Optional

from pydantic import BaseModel, EmailStr
from datetime import datetime


class Listing(BaseModel):
    id: str
    price: int
    email: Optional[EmailStr]
    year_built: datetime
    baths: int
    listing_date: datetime
    square_feet: int
    #TODO more to be added from data dictionary
