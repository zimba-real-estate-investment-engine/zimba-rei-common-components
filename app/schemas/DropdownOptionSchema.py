import json
from typing import Optional

from pydantic import BaseModel


class DropdownOptionSchema(BaseModel):
    id: Optional[int] = None
    dropdown_name: str
    value: str
    label: str
    is_active: bool
    order_index: int

    #TODO more to be added from data dictionary as necessary

    class Config:
        orm_mode = True
        from_attributes = True
