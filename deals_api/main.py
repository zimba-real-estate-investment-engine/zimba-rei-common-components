from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from fastapi import FastAPI
from rei_models import Deal

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello from App 1"}


@app.get("/deals")
async def get_deals():
    json_output = _all_deals().model_dump_json()
    return _all_deals()


def _all_deals():
    current_time_string = str(datetime.now().timestamp())
    deal_date = datetime.now()
    closing_date = datetime.now() + relativedelta(months=3)
    underwriting_date = datetime.now() + relativedelta(months=2)

    deal = Deal(
        id=current_time_string, listing_id=current_time_string, investor_id=current_time_string,
        deal_date=deal_date, deal_status="open", offer_price=300000, sale_price=350000,
        closing_date=closing_date, underwriting_id=current_time_string,
        appraisal_value=320000, loan_amount=240000, loan_to_value=0.8,
        underwriting_date=underwriting_date, approval_status="approved", risk_assessment="low",
        thumbnail="www.example.com",
    )

    return deal
