from fastapi.testclient import TestClient
from subscription_api.main import app
from subscription_api.rei_models.Subscription import Subscription


def test_get_Subscriptions():
    client = TestClient(app)
    response = client.get("/subscriptions")
    assert response.status_code == 200
    deal = Subscription(**response.json())  # will confirm that object can be instantiated from json
