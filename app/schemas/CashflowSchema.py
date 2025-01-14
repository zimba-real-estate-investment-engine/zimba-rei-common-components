from typing import Optional, List

from pydantic import BaseModel


class CashflowSchema(BaseModel):
    id: Optional[int] = None
    cashflow_type: str
    monthly_cashflow: float
    #TODO more to be added from data dictionary as necessary

    class Config:
        orm_mode = True
        from_attributes = True
