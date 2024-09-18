from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from fastapi import FastAPI
from rei_models import InvestorProfile

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello from App 1"}


@app.get("/investor-profiles")
async def get_investor_profiles():
    return _all_investor_profiles()


def _all_investor_profiles():
    current_time_string = str(datetime.now().timestamp())
    f_name = "fname" + current_time_string
    l_name = "lname" + current_time_string

    investor_profile = InvestorProfile(
        id=current_time_string, price=300000, first_name=f_name, last_name=l_name,
        email="email@example.com", title="Ms.", phone="1-888-454-1234",
        preferred_property_type="rental", preferred_locations=["SE", "NE"],
        bedrooms_max=8, bedrooms_min=2, bathrooms_min=2, bathrooms_max=3, budget_max=100000000, budget_min=200000,
        years_built_max=80, years_built_min=30, investment_purpose="rental",
        assigned_parking_required=True, central_heat_required=True, dishwasher_required=True,
        balcony_required=True
    )
    return investor_profile
