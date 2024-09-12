from pydantic import BaseModel
from datetime import datetime


class Deal(BaseModel):
    id: str
    listing_id: str
    investor_id: str
    deal_date: datetime
    deal_status: str
    offer_price: int
    sale_price: int
    closing_date: datetime
    thumbnail: str
    #TODO more to be added from data dictionary as necessary
