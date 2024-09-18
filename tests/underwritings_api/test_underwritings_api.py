from fastapi.testclient import TestClient
from underwritings_api.main import app
from underwritings_api.rei_models.Underwriting import Underwriting


def test_get_underwritings():
    client = TestClient(app)
    response = client.get("/underwritings")
    assert response.status_code == 200
    listing = Underwriting(**response.json())  # will confirm that object can be instantiated from json
