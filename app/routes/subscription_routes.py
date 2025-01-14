# from fastapi import APIRouter, Depends
# from app.schemas.SubscriptionSchema import SubscriptionSchema
# from app.core.migrations import get_db
# from sqlalchemy.orm import Session
# #
# # from app.services.SubscriptionService import SubscriptionService
# #
# router = APIRouter()
# #
# #
# @router.post("/subscriptions/", response_model=SubscriptionSchema)
# def create_subscription_route(subscription: str):
#     return "hello"
#     # service = SubscriptionService(db)
#     # new_saved_subscription = service.save_subscription(subscription)
#     # return new_saved_subscription
# #
# # @router.post("/subscriptions", response_model=SubscriptionSchema)
# # def create_subscription_route(subscription: SubscriptionSchema, db: Session = Depends(get_db)):
# #     service = SubscriptionService(db)
# #     new_saved_subscription = service.save_subscription(subscription)
# #     return new_saved_subscription
# #
# #
# # # @router.get("/listings/{listing_id}", response_model=ListingSchema)
# # # def get_listings_route(listing_id: str, db: Session = Depends(get_db)):
# # #     return get_user(db=db, user_id=user_id)
