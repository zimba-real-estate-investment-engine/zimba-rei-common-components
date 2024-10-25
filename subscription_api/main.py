from datetime import datetime, timezone
from fastapi import FastAPI
from rei_models import Subscription

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello from App 1"}


@app.get("/subscriptions")
async def get_subscriptions():
    return _all_subscriptions()


def _all_subscriptions():
    current_time_string = str(datetime.now().timestamp())
    issued_date = datetime.now()
    user_email = current_time_string + '@example.com'
    user_name = current_time_string + '_firstname'
    user_unsubscribe_token = current_time_string + '_token'

    subscription = Subscription(
        id=current_time_string, email=user_email, name=user_name, service_subscribed_to='get_on_shortlist',
        source_url='index.html', form_id='subscribe_to_shortlist', subscribed=True, unsubscribed_date=issued_date,
        unsubscribe_token=user_unsubscribe_token
    )
    return subscription
