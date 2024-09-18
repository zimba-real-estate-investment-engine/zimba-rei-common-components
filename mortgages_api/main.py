from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from fastapi import FastAPI
from rei_models import Mortgage

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello from App 1"}


@app.get("/mortgages")
async def get_mortgages():
    return _all_mortgages()


def _all_mortgages():
    current_time_string = str(datetime.now().timestamp())
    issued_date = datetime.now()

    mortgage = Mortgage(
        id=current_time_string, appraisal_value=300000.00, principal=240000.03, issued_date=issued_date,
        pre_qualifid=True, pre_approved=True, loan_to_value=80.0, interest_rate=3.75,
        term=timedelta(days=3 * 365), amortization_period=timedelta(days=30 * 365), monthly_payment=3565.25,
        owner_occupied=True, insurance=3500.75,
    )
    return mortgage