import json

from pydantic import BaseModel, ConfigDict


class AmortizationCachingCodeSchema(BaseModel):
    principal: float
    annual_interest_rate: float
    amortization_period: int

    def __json__(self, *args, **kwargs):
        return self.model_dump()

    class Config:
        orm_mode = True
        from_attributes = True
