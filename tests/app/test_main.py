import time

from app.database.models import SubscriptionModel
from app.repositories.BaseRepository import BaseRepository
from app.schemas.InvestorProfileSchema import InvestorProfileSchema
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


def test_get_investor_profiles(test_fastapi_client, request):
    client = test_fastapi_client
    response = client.get("/investor-profiles/")
    assert response.status_code == 200


def test_create_investor_profile(test_fastapi_client, request, get_test_investor_profile_schema):
    test_investor_profile = get_test_investor_profile_schema
    request_json = test_investor_profile.json()

    client = test_fastapi_client
    response = client.post("/investor-profiles/", data=request_json)
    assert response.status_code == 200

    result_json = response.json()
    investor_profile_schema = InvestorProfileSchema(**result_json)  # Ensure we can instantiate the pydantic object
    assert investor_profile_schema.id and investor_profile_schema.id != 0


