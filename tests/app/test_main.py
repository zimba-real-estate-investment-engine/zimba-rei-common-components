import time

from app.database.SubscriptionModel import SubscriptionModel
from app.repositories.BaseRepository import BaseRepository
from app.schemas.SubscriptionSchema import SubscriptionSchema


def test_create_subscription(get_test_subscription_schema, test_fastapi_client, get_test_db):
    test_subscription = get_test_subscription_schema
    client = test_fastapi_client
    test_db = get_test_db

    response = client.post("/subscriptions/", data=test_subscription.json())
    assert response.status_code == 200

    # Confirms that the returned value can be instantiated from the pydantic schema
    newly_created_subscription = SubscriptionSchema(**response.json())

    # Clean up to avoid bloated database. Using BaseRepository which uses SqlAlchemy database ¯\_(ツ)_/¯
    subscription_model = SubscriptionModel(**newly_created_subscription.model_dump())
    base_repo = BaseRepository(test_db, SubscriptionModel)
    base_repo.delete(subscription_model.id)
    test_db.commit()


def test_get_subscriptions(test_fastapi_client, request):

    client = test_fastapi_client
    response = client.get("/subscriptions/")
    assert response.status_code == 200

