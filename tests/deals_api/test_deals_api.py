from fastapi.testclient import TestClient
from deals_api.main import app
from deals_api.rei_models.Deal import Deal


def test_get_deals():
    client = TestClient(app)
    response = client.get("/deals")
    assert response.status_code == 200
    deal = Deal(**response.json())  # will confirm that object can be instantiated from json
