from pydantic import BaseModel


class AmortizationScheduleRowSchema(BaseModel):
    payment_number: int
    monthly_payment: float
    interest_payment: float
    principal_recapture: float
    remaining_balance: float

    class Config:
        orm_mode = True
        from_attributes = True
