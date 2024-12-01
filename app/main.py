import os
from datetime import datetime, timezone
from typing import List

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from app.core import database
from app.database.models import SubscriptionModel
from app.domain.RealEstateProperty import RealEstateProperty
from app.schemas.AddressSchema import AddressSchema
from app.schemas.InvestorProfileSchema import InvestorProfileSchema
from app.schemas.ListingSchema import ListingSchema
from app.schemas.RealEstatePropertySchema import RealEstatePropertySchema
from app.schemas.SubscriptionSchema import SubscriptionSchema
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from urllib.parse import quote_plus

from app.services.AddressService import AddressService
from app.services.InvestorProfileService import InvestorProfileService
from app.services.ListingService import ListingService
from app.services.RealEstatePropertyService import RealEstatePropertyService
from app.services.SubscriptionService import SubscriptionService

# Create the FastAPI app
app = FastAPI()


def get_db():
    # db = database.get_db()
    # return db
    load_dotenv()

    # Database configuration
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    DB_ECHO_SQL_COMMANDS = os.getenv('DB_ECHO_SQL_COMMANDS', 'false').lower()=='true'

    # Create the SQLAlchemy database URL
    # We use quote_plus to properly encode the password
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Create the SQLAlchemy engine
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # Enables automatic reconnection
        pool_size=5,  # Maximum number of connections to keep persistently
        max_overflow=10,  # Maximum number of connections that can be created beyond pool_size
        echo=DB_ECHO_SQL_COMMANDS
    )

    # SessionLocal class will be used to create database sessions
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Initialize database tables
# Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "REI API Server"}


@app.get("/health")
async def root():
    return {"message": "REI API Server", "status": "healthy"}


@app.post("/subscriptions/", response_model=SubscriptionSchema)
async def create_subscription(subscription: SubscriptionSchema, db: Session = Depends(get_db)):
    subscription_service = SubscriptionService(db)
    newly_saved_subscription = subscription_service.save_subscription(subscription)
    return newly_saved_subscription


@app.get("/subscriptions/", response_model=List[SubscriptionSchema])
async def get_subscriptions(db: Session = Depends(get_db)):
    # subscription = db.execute.select(SubscriptionModel)).scalars())
    subscription_service = SubscriptionService(db)
    subscription_schema_list = subscription_service.get_all()
    subscription_json_list = list(map(lambda x: x.model_dump(), subscription_schema_list))
    return subscription_json_list


@app.get("/listings/", response_model=List[ListingSchema])
async def get_listings(db: Session = Depends(get_db)):
    listing_service = ListingService(db)
    listing_schema_list = listing_service.get_all()
    listing_json_list = list(map(lambda x: x.model_dump(), listing_schema_list))
    return listing_json_list


@app.get("/addresses/", response_model=List[AddressSchema])
async def get_addresses(db: Session = Depends(get_db)):
    address_service = AddressService(db)
    address_schema_list = address_service.get_all()
    address_json_list = list(map(lambda x: x.model_dump(), address_schema_list))
    return address_json_list


@app.get("/real-estate-properties/", response_model=List[RealEstatePropertySchema])
async def get_real_estate_properties(db: Session = Depends(get_db)):
    real_estate_property_service = RealEstatePropertyService(db)
    real_estate_property_schema_list = real_estate_property_service.get_all()
    real_estate_property_json_list = list(map(lambda x: x.model_dump(), real_estate_property_schema_list))
    return real_estate_property_json_list


@app.get("/investor-profiles/", response_model=List[InvestorProfileSchema])
async def get_investor_profiles(db: Session = Depends(get_db)):
    investor_profile_service = InvestorProfileService(db)
    investor_profile_schema_list = investor_profile_service.get_all()
    investor_profile_json_list = list(map(lambda x: x.model_dump(), investor_profile_schema_list))
    return investor_profile_json_list


@app.post("/investor-profiles/", response_model=InvestorProfileSchema)
async def create_investor_profiles(investor_profile: InvestorProfileSchema, db: Session = Depends(get_db)):
    investor_profile_service = InvestorProfileService(db)
    newly_saved_investor_profile = investor_profile_service.save_investor_profile(investor_profile)
    return newly_saved_investor_profile


# Include the routes if external
# app.include_router(users.router, prefix="/users", tags=["Users"])

# Additional routes can be included as needed
# app.include_router(other_route.router, prefix="/other", tags=["Other"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
