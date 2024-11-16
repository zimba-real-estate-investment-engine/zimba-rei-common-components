from datetime import datetime, timezone

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


@app.get("/subscriptions/")
async def get_subscriptions(db: Session = Depends(get_db)):
    current_time_string = str(datetime.now(timezone.utc).time())
    issued_date = datetime.now()
    user_email = current_time_string + '@example.com'
    user_name = current_time_string + '_firstname'
    user_unsubscribe_token = current_time_string + '_token'

    subscription_schema = SubscriptionSchema(
        id=current_time_string, email=user_email, name=user_name, service_subscribed_to='get_on_shortlist',
        source_url='index.html', form_id='subscribe_to_shortlist', subscribed=True, unsubscribed_date=issued_date,
        unsubscribe_token=user_unsubscribe_token
    )

    return subscription_schema.model_dump_json()

# Include the routes if external
# app.include_router(users.router, prefix="/users", tags=["Users"])

# Additional routes can be included as needed
# app.include_router(other_route.router, prefix="/other", tags=["Other"])
