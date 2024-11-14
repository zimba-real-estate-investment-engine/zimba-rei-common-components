from fastapi import APIRouter, Depends
from app.schemas.SubscriptionSchema import SubscriptionSchema

# from app.domain.user import UserCreate, UserRead
# from app.crud.user import create_user, get_user
# from app.core.database import get_db
# from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/subscriptions", response_model=SubscriptionSchema)
def create_listing_route(subscription: SubscriptionSchema, db: Session = Depends(get_db)):
    return create_subscription(db=db, user=user)


@router.get("/listings/{listing_id}", response_model=ListingSchema)
def get_listings_route(listing_id: str, db: Session = Depends(get_db)):
    return get_user(db=db, user_id=user_id)
