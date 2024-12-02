from typing import Optional, List

from pydantic import BaseModel


class ExpenseSchema(BaseModel):
    id: Optional[int] = None
    expense_type: str
    monthly_cost: float
    #TODO more to be added from data dictionary as necessary

    class Config:
        orm_mode = True
        from_attributes = True