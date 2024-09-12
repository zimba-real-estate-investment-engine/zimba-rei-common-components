from datetime import datetime

from rei_models.rei_models.Listing import Listing
from tests.conftest import get_current_time_in_seconds_string


def test_create_listing(get_current_time_in_seconds_string):
    current_time_string = get_current_time_in_seconds_string
    listing = Listing(id=current_time_string, price="300000", email="email@example.com",
                      year_built=datetime(2000, 1, 1), baths=3,
                      listing_date=datetime(2024, 4, 1),
                      square_feet=2500)

    assert listing.id == current_time_string
    assert listing.price == 300000
    assert listing.email == 'email@example.com'
    assert listing.square_feet == 2500

