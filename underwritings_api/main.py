from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from fastapi import FastAPI
from rei_models import Underwriting

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello from App 1"}


@app.get("/underwritings")
async def get_underwritings():
    return _all_underwritings()


def _all_underwritings():
    current_time_string = str(datetime.now().timestamp())
    underwriting_date = datetime.now() + relativedelta(months=2)

    underwriting = Underwriting(
        underwriting_id=current_time_string, appraisal_value=320000, loan_amount=240000,
        loan_to_value=0.8, interest_rate=5, underwriting_date=underwriting_date,
        approval_status="approved", risk_assessment="low",
    )

    return underwriting
