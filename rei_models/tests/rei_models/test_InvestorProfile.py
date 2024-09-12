from datetime import datetime

from rei_models.rei_models.InvestorProfile import InvestorProfile
from tests.conftest import get_current_time_in_seconds_string


def test_create_investor_profile(get_current_time_in_seconds_string):
    current_time_string = get_current_time_in_seconds_string
    f_name = "Fname" + current_time_string
    l_name = "Lname" + current_time_string

    investor_profile = InvestorProfile(
        id=current_time_string, price=300000, first_name=f_name, last_name=l_name,
        email="email@example.com", title="Ms.", phone="1-888-454-1234",
        preferred_property_type="rental", preferred_locations=["SE", "NE"],
        bedrooms_max=8, bedrooms_min=2, bathrooms_min=2, bathrooms_max=3, budget_max=100000000, budget_min=200000,
        years_built_max=80, years_built_min=30, investment_purpose="rental",
        assigned_parking_required=True, central_heat_required=True, dishwasher_required=True,
        balcony_required=True
    )

    #TODO more validation to be added
    assert investor_profile.id == current_time_string
    assert investor_profile.price == 300000
    assert investor_profile.email == 'email@example.com'
