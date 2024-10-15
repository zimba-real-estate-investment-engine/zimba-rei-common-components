from typing import List

from pydantic import BaseModel, EmailStr, validator
from datetime import datetime


class InvestorProfile(BaseModel):
    id: str
    price: float
    first_name: str
    last_name: str
    email: EmailStr
    title: str
    phone: str
    preferred_property_type: str
    preferred_locations: List[str]
    bedrooms_max: int
    bedrooms_min: int
    bathrooms_max: int
    bathrooms_min: int
    budget_max: int
    budget_min: int
    years_built_min: int
    years_built_max: int
    investment_purpose: str
    assigned_parking_required: bool
    central_heat_required: bool
    dishwasher_required: bool
    balcony_required: bool
