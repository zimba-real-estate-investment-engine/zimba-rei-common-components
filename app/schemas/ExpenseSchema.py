from typing import Optional, List

from pydantic import BaseModel
from datetime import datetime

from app.schemas.ListingSchema import ListingSchema


class ExpenseSchema(BaseModel):
    id: Optional[int] = None
    expense_type: str
    monthly_cost: float
    #TODO more to be added from data dictionary as necessary
