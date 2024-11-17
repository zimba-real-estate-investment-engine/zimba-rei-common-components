from datetime import datetime, timezone
from typing import List

from fastapi import FastAPI, HTTPException, Depends
from app.core import database
from app.schemas.SubscriptionSchema import SubscriptionSchema
from sqlalchemy.orm import Session

from app.services.SubscriptionService import SubscriptionService

# Create the FastAPI app
app = FastAPI()


def get_db():
    return database.get_db()

# Initialize database tables
# Base.metadata.create_all(bind=engine)


@app.post("/subscriptions/", response_model=SubscriptionSchema)
async def create_subscription(subscription: SubscriptionSchema, db: Session = Depends(get_db)):
    subscription_service = SubscriptionService(db)
    newly_saved_subscription = subscription_service.save_subscription(subscription)
    return newly_saved_subscription


@app.get("/subscriptions/", response_model=List[SubscriptionSchema])
async def get_subscriptions(db: Session = Depends(get_db)):

    subscription_service = SubscriptionService(db)
    subscription_schema_list = subscription_service.get_all()
    subscription_json_list = list(map(lambda x: x.model_dump(), subscription_schema_list))
    return subscription_json_list

# Include the routes if external
# app.include_router(users.router, prefix="/users", tags=["Users"])

# Additional routes can be included as needed
# app.include_router(other_route.router, prefix="/other", tags=["Other"])
