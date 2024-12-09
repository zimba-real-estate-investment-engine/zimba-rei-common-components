from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class REIPriceSchema(BaseModel):
    original: str
    amount: float
    currency_symbol: str
    currency_iso_code: str

    class Config:
        orm_mode = True
        from_attributes = True
