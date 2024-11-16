from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class SubscriptionSchema(BaseModel):
    id: str
    email: str
    name: str
    service_subscribed_to: str
    source_url: str
    form_id: str
    subscribed: bool
    unsubscribed_date:Optional[datetime]
    unsubscribe_token: str
    #TODO more to be added from data dictionary as necessary
