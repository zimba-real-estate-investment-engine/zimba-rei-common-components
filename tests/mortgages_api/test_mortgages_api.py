from fastapi.testclient import TestClient
from mortgages_api.main import app
from deals_api.rei_models.Mortgage import Mortgage


def test_get_mortgages():
    client = TestClient(app)
    response = client.get("/mortgages")
    assert response.status_code == 200
    listing = Mortgage(**response.json())  # will confirm that object can be instantiated from json
