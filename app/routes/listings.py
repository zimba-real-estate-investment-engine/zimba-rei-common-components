from typing import List
#
# from fastapi import APIRouter, Depends
# from app.schemas.ListingSchema import ListingSchema
#
# # from app.domain.user import UserCreate, UserRead
# # from app.crud.user import create_user, get_user
# # from app.core.database import get_db
# # from sqlalchemy.orm import Session
#
# router = APIRouter()
#
#
# # @router.post("/listings", response_model=ListingSchema)
# # def create_listing_route(listing: ListingSchema, db: Session = Depends(get_db)):
# #     return create_user(db=db, user=user)
#
#
# @router.get("/listings/{listing_id}", response_model=List[ListingSchema])
# def get_listings_route(listing_id: str, db: Session = Depends(get_db)):
#     return get_user(db=db, user_id=user_id)
#
# # @router.get("/listings/{listing_id}", response_model=List[ListingSchema])
# # def get_listings_route(listing_id: str, db: Session = Depends(get_db)):
# #     return get_user(db=db, user_id=user_id)