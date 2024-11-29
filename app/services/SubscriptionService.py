import logging
from typing import List

from sqlalchemy.orm import Session

from app.domain.Subscription import Subscription
# from app.database.user import User
# from app.schemas.user import UserCreate, UserRead
# from app.crud.user import get_user_by_email, create_user
# from typing import Optional
# from fastapi import HTTPException, status

from app.database.models import SubscriptionModel
from app.repositories.BaseRepository import BaseRepository
from app.schemas.EmailSchema import EmailSchema
from app.schemas.SubscriptionSchema import SubscriptionSchema

logger = logging.getLogger(__name__)


class SubscriptionService:
    def __init__(self, db: Session):
        self.logger = logger
        self.db = db
        self.repo = BaseRepository[SubscriptionModel](self.db, SubscriptionModel)

    def save_subscription(self, subscription_data: SubscriptionSchema) -> SubscriptionSchema:
        #TODO  Check if a user with the same email already exists
        # existing_subscription = get_user_by_email(self.db, email=subscription_data.email)
        # if existing_subscription:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="Email already registered"
        #     )
        try:
            subscription_model = BaseRepository.pydantic_to_sqlalchemy(subscription_data, SubscriptionModel)

            subscription_model.unsubscribe_token = Subscription.generate_unsubscribe_token()

            new_subscription_model = self.repo.add(subscription_model)
            new_subscription_schema = BaseRepository.sqlalchemy_to_pydantic(new_subscription_model, SubscriptionSchema)

            self.db.commit()  # make sure commit to db was successful

            return new_subscription_schema

        except Exception as e:
            self.logger.error(f'Error saving {subscription_data}:: {str(e)}')
            raise

        #TODO # Also send confirmation message
        # message_subject = f'Welcome to our {subscription_data.service_subscribed_to}'
        # message_html_body = Subscription.generate_html_message_body().format(
        #     recipient_name=subscription_model.name, unsubscribe_token=subscription_model.unsubscribe_token,
        #     unsubscribe_api_endpoint='https://rei.zimbasoltuions.io/unsubcribe'
        # )
        #
        # email_schema = EmailSchema(
        #     to_addresses=['rei@zimbasolutions.io'], subject=message_subject, sender='rei@zimbasolutions.io',
        #     body_text='SES Unit Test Email body', body_html=message_html_body
        # )

    def get_all(self) -> List[SubscriptionSchema]:
        subscription_model_list = self.repo.get_all()

        subscription_schema_list = \
            [BaseRepository.sqlalchemy_to_pydantic(x, SubscriptionSchema) for x in subscription_model_list]
        return subscription_schema_list
