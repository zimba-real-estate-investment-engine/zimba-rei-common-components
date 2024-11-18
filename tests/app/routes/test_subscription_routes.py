# # from app.schemas.user import UserCreate
# from app.routes.subscription_routes import router
# from fastapi.testclient import TestClient
# from fastapi import FastAPI
#
#
# def test_create_subscription_route(get_test_subscription_schema):
#
#     test_subscription_schema = get_test_subscription_schema
#     test_subscription_json = test_subscription_schema.json()
#     app = FastAPI()
#     app.include_router(router)
#     client = TestClient(app)
#     # response = client.post("/subscriptions", json=test_subscription_json)
#     response = client.post("/subscriptions/", json={"name": "Test", "age": 30})
#     # assert response.status_code == 200
#     assert response
