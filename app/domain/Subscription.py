import secrets
import string

from app.schemas import SubscriptionSchema


class Subscription:
    """
        Domain entity contains business logic and inherits from pydantic schema
    """

    @staticmethod
    def generate_unsubscribe_token(self, length=32):
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    def __init__(self, data: SubscriptionSchema):
        self._data = data

    # Delegate Pydantic model attributes, these are returned automatically
    def __getattr__(self, name: str):
        return getattr(self._data, name)


