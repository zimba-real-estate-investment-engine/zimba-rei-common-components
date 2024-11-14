from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.crud.user import get_user_by_email, create_user
from typing import Optional
from fastapi import HTTPException, status
from app.core.security import hash_password, verify_password  # Security utilities


class SubscriptionService:
    def __init__(self, db: Session):
        self.db = db

    def register_user(self, user_data: UserCreate) -> UserRead:
        # Check if a user with the same email already exists
        existing_user = get_user_by_email(self.db, email=user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash the password before saving
        hashed_password = hash_password(user_data.password)
        user_data.password = hashed_password

        # Create a new user
        new_user = create_user(self.db, user=user_data)
        return UserRead.from_orm(new_user)  # Convert to response schema

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        # Retrieve user by email
        user = get_user_by_email(self.db, email=email)
        if not user or not verify_password(password, user.password):
            return None
        return user

    def get_user_by_id(self, user_id: int) -> Optional[UserRead]:
        # Retrieve user by ID
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return UserRead.from_orm(user)
