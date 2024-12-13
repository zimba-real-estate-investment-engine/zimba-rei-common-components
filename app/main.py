import os
from datetime import datetime, timezone
from typing import List

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends
from starlette.middleware.cors import CORSMiddleware

from app.core import database
from app.database.models import SubscriptionModel
from app.domain.RealEstateProperty import RealEstateProperty
from app.schemas.AddressSchema import AddressSchema
from app.schemas.CapitalInvestmentSchema import CapitalInvestmentSchema
from app.schemas.CashflowSchema import CashflowSchema
from app.schemas.DealSchema import DealSchema, DealSearchSchema
from app.schemas.ExpenseSchema import ExpenseSchema
from app.schemas.FinancingSchema import FinancingSchema
from app.schemas.InvestorProfileSchema import InvestorProfileSchema, InvestorProfileSearchSchema
from app.schemas.ListingSchema import ListingSchema
from app.schemas.ProjectionEntrySchema import ProjectionEntrySchema, ProjectionEntrySearchSchema
from app.schemas.RealEstatePropertySchema import RealEstatePropertySchema
from app.schemas.SubscriptionSchema import SubscriptionSchema
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from urllib.parse import quote_plus

from app.schemas.UnderwritingSchema import UnderwritingSchema
from app.services.AddressService import AddressService
from app.services.CapitalInvestmentService import CapitalInvestmentService
from app.services.CashflowService import CashflowService
from app.services.DealService import DealService
from app.services.ExpenseService import ExpenseService
from app.services.FinancingService import FinancingService
from app.services.InvestorProfileService import InvestorProfileService
from app.services.ListingService import ListingService
from app.services.MortgageService import MortgageService
from app.services.ProjectionEntryService import ProjectionEntryService
from app.services.RealEstatePropertyService import RealEstatePropertyService
from app.services.SubscriptionService import SubscriptionService
from app.services.UnderwritingService import UnderwritingService

# Create the FastAPI app
app = FastAPI()

# Configure CORS
# origins = [
#     # List of allowed origins (domains)
#     "http://localhost:3000",  # Example: React development server
#     "https://yourdomain.com",
#     "https://www.yourdomain.com",
#     # Add more origins as needed
# ]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,  # Allows specified origins
    allow_origins=["*"],  # Allows specified origins
    allow_credentials=True,  # Allows cookies to be included in CORS requests
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)


def get_db():
    # db = migrations.get_db()
    # return db
    load_dotenv()

    # Database configuration
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_NAME')
    DB_ECHO_SQL_COMMANDS = os.getenv('DB_ECHO_SQL_COMMANDS', 'false').lower() == 'true'

    # Create the SQLAlchemy migrations URL
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

    # SessionLocal class will be used to create migrations sessions
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Initialize migrations tables
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


@app.get("/deals/", response_model=List[DealSchema])
async def get_deals(db: Session = Depends(get_db)):
    deal_service = DealService(db)
    deal_schema_list = deal_service.get_all()
    deal_json_list = list(map(lambda x: x.model_dump(), deal_schema_list))
    return deal_json_list


@app.post("/deals/find-by-id/", response_model=DealSchema, description='Find by ID, You need to submit ID')
async def get_deal(request: DealSearchSchema, db: Session = Depends(get_db)):
    id = request.id

    if id is None:
        raise ValueError("ID is required")

    try:
        deal_service = DealService(db)
        deal_schema: DealSchema = deal_service.get_by_id(id)

        return deal_schema
    except Exception as e:
        raise


@app.get("/investor-profiles/", response_model=List[InvestorProfileSchema])
async def get_investor_profiles(db: Session = Depends(get_db)):
    investor_profile_service = InvestorProfileService(db)
    investor_profile_schema_list = investor_profile_service.get_all()
    investor_profile_json_list = list(map(lambda x: x.model_dump(), investor_profile_schema_list))
    return investor_profile_json_list


@app.post("/investor-profiles/find-by-id/", response_model=InvestorProfileSchema,
          description='Find by ID, You need to submit ID')
async def get_investor_profile(request: InvestorProfileSearchSchema, db: Session = Depends(get_db)):
    id = request.id

    if id is None:
        raise ValueError("ID is required")

    try:
        investor_profile_service = InvestorProfileService(db)
        investor_profile_schema = investor_profile_service.get_by_id(id)

        return investor_profile_schema

    except Exception as e:
        raise


@app.post("/investor-profiles/", response_model=InvestorProfileSchema)
async def create_investor_profiles(investor_profile: InvestorProfileSchema, db: Session = Depends(get_db)):
    investor_profile_service = InvestorProfileService(db)
    newly_saved_investor_profile = investor_profile_service.save_investor_profile(investor_profile)
    return newly_saved_investor_profile


@app.get("/projection-entries/", response_model=List[ProjectionEntrySchema])
async def get_investor_profiles(db: Session = Depends(get_db)):
    projection_entry_service = ProjectionEntryService(db)
    projection_entry_schema_list = projection_entry_service.get_all()
    projection_entry_json_list = list(map(lambda x: x.model_dump(), projection_entry_schema_list))
    return projection_entry_json_list


@app.post("/projection-entries/find-by-id/", response_model=ProjectionEntrySchema,
          description='Find by ID, You need to submit ID')
async def get_projection_entry(request: ProjectionEntrySearchSchema, db: Session = Depends(get_db)):
    id = request.id

    if id is None:
        raise ValueError("ID is required")

    try:
        projection_entry_service = ProjectionEntryService(db)
        projection_entry_schema = projection_entry_service.get_by_id(id)

        return projection_entry_schema

    except Exception as e:
        raise


@app.post("/projection-entries", response_model=ProjectionEntrySchema)
async def create_projection_entry(projection_entry: ProjectionEntrySchema, db: Session = Depends(get_db)):
    projection_entry_service = ProjectionEntryService(db)
    newly_saved_projection_entry = projection_entry_service.save_projection_entry(projection_entry)
    return newly_saved_projection_entry


@app.get("/expenses/", response_model=List[ExpenseSchema])
async def get_expenses(db: Session = Depends(get_db)):
    expense_service = ExpenseService(db)
    expense_schema_list = expense_service.get_all()
    expense_json_list = list(map(lambda x: x.model_dump(), expense_schema_list))
    return expense_json_list


@app.get("/cashflow/", response_model=List[CashflowSchema])
async def get_cashflow_items(db: Session = Depends(get_db)):
    cashflow_service = CashflowService(db)
    cashflow_schema_list = cashflow_service.get_all()
    cashflow_json_list = list(map(lambda x: x.model_dump(), cashflow_schema_list))
    return cashflow_json_list


@app.get("/capital_investments/", response_model=List[CapitalInvestmentSchema])
async def get_capital_investments(db: Session = Depends(get_db)):
    capital_investment_service = CapitalInvestmentService(db)
    capital_investment_schema_list = capital_investment_service.get_all()
    capital_investment_json_list = list(map(lambda x: x.model_dump(), capital_investment_schema_list))
    return capital_investment_json_list

@app.get("/financing/", response_model=List[FinancingSchema])
async def get_financing(db: Session = Depends(get_db)):
    financing_service = FinancingService(db)
    financing_schema_list = financing_service.get_all()
    financing_json_list = list(map(lambda x: x.model_dump(), financing_schema_list))
    return financing_json_list


@app.get("/mortgages/", response_model=List[FinancingSchema])
async def get_mortgages(db: Session = Depends(get_db)):
    mortgage_service = MortgageService(db)
    mortgage_schema_list = mortgage_service.get_all()
    mortgage_json_list = list(map(lambda x: x.model_dump(), mortgage_schema_list))
    return mortgage_json_list


@app.get("/underwritings/", response_model=List[UnderwritingSchema])
async def get_underwritings(db: Session = Depends(get_db)):
    underwriting_service = UnderwritingService(db)
    underwriting_schema_list = underwriting_service.get_all()
    underwriting_json_list = list(map(lambda x: x.model_dump(), underwriting_schema_list))
    return underwriting_json_list


# Include the routes if external
# app.include_router(users.router, prefix="/users", tags=["Users"])

# Additional routes can be included as needed
# app.include_router(other_route.router, prefix="/other", tags=["Other"])


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
