from fastapi.testclient import TestClient
from investor_profiles_api.main import app
from deals_api.rei_models.InvestorProfile import InvestorProfile


def test_get_investor_profiles():
    client = TestClient(app)
    response = client.get("/investor-profiles")
    assert response.status_code == 200
    listing = InvestorProfile(**response.json())  # will confirm that object can be instantiated from json
