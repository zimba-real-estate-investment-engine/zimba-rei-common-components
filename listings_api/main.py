from datetime import datetime, timezone
from fastapi import FastAPI
from rei_models import Listing

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello from Listings API!"}


@app.get("/listings")
async def get_listings():
    return _all_listings()


def _all_listings():
    current_time_string = str(datetime.now().timestamp())
    deal_date = datetime.now()
    listing = Listing(id=current_time_string, price=300000.34, email="email@example.com",
                      year_built=datetime(2000, 1, 1), baths=3,
                      listing_date=datetime(2024, 4, 1),
                      square_feet=2500)

    return listing
