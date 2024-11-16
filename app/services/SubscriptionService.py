from sqlalchemy.orm import Session
# from app.models.user import User
# from app.schemas.user import UserCreate, UserRead
# from app.crud.user import get_user_by_email, create_user
# from typing import Optional
# from fastapi import HTTPException, status

from app.models.SubscriptionModel import SubscriptionModel
from app.repositories.BaseRepository import BaseRepository
from app.schemas.SubscriptionSchema import SubscriptionSchema


class SubscriptionService:
    def __init__(self, db: Session):
        self.db = db

    def save_subscription(self, subscription_data: SubscriptionSchema) -> SubscriptionSchema:
        #TODO  Check if a user with the same email already exists
        # existing_subscription = get_user_by_email(self.db, email=subscription_data.email)
        # if existing_subscription:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="Email already registered"
        #     )
        subscription_model = SubscriptionModel(**subscription_data.model_dump())

        repo = BaseRepository[SubscriptionModel](self.db, SubscriptionModel)
        new_subscription_model = repo.add(subscription_model)
        new_subscription_schema = repo.sqlalchemy_to_pydantic(new_subscription_model, SubscriptionSchema)

        self.db.commit()

        return new_subscription_schema  # Convert to response schema


