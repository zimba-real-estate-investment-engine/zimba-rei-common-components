import secrets
import string

from app.schemas.SubscriptionSchema import SubscriptionSchema


class Subscription(SubscriptionSchema):
    pass

    def generate_unsubscribe_token(self, length=32):
        alphabet = string.ascii_letters + string.digits
        token = ''.join(secrets.choice(alphabet) for _ in range(length))
        self.unsubscribe_token = token

        return token

    def unsubscribe(self):
        if self.unsubscribe_token.strip():
            raise ValueError("Missing unsubscribe token. Cannot unsubscribe without it")



