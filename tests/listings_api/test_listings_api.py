from fastapi.testclient import TestClient
from listings_api.main import app
from deals_api.rei_models.Listing import Listing


def test_get_listings():
    client = TestClient(app)
    response = client.get("/listings")
    assert response.status_code == 200
    listing = Listing(**response.json())  # will confirm that object can be instantiated from json
