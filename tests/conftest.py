from __future__ import annotations
import os
import time
from typing import List
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from time import timezone
from urllib.parse import quote_plus
from fastapi.testclient import TestClient
from app.main import app, get_db
from app.database.models import AddressModel, RealEstatePropertyModel, ListingModel, ExpenseModel, InvestorProfileModel, \
    FinancingModel, MortgageModel, SubscriptionModel, UnderwritingModel, DealModel, ProjectionEntryModel
from app.database.models import RealEstatePropertyModel
from datetime import datetime, timezone, timedelta

from dateutil.relativedelta import relativedelta

from app.schemas.ListingSchema import ListingSchema
from app.schemas.DealSchema import DealSchema
from app.schemas.FinancingSchema import FinancingSchema
from app.schemas.InvestorProfileSchema import InvestorProfileSchema
from app.schemas.ProjectionEntrySchema import ProjectionEntrySchema
from app.schemas.UnderwritingSchema import UnderwritingSchema
from app.schemas.MortgageSchema import MortgageSchema
from app.schemas.SubscriptionSchema import SubscriptionSchema
from app.schemas.EmailSchema import EmailSchema
from app.schemas.AddressSchema import AddressSchema
from app.schemas.ExpenseSchema import ExpenseSchema
from app.schemas.RealEstatePropertySchema import RealEstatePropertySchema

import pytest

engine = None


@pytest.fixture
def get_test_db():
    yield __test_db()


@pytest.fixture
def get_current_time_in_seconds_str() -> str:
    current_time = datetime.now(timezone.utc)
    mills = int(current_time.timestamp())
    return str(mills)


@pytest.fixture
def get_current_time_in_seconds_string() -> str:
    return __get_time_string()


@pytest.fixture
def get_test_listing_schema() -> ListingSchema:
    current_time_string = __get_time_string()
    listing_schema = ListingSchema(price=300000, email="email@example.com",
                                   year_built=datetime(2000, 1, 1), baths=3, beds=5,
                                   listing_date=datetime(2024, 4, 1),
                                   square_feet=2500, parking_spaces="4", air_conditioning=False, balcony=False,
                                   basement='crawl space only', dishwasher=True, hardwood_floor='ground floor')
    return listing_schema


@pytest.fixture
def get_test_listing_model() -> ListingModel:
    current_time_string = __get_time_string()
    listing_model = ListingModel(price=300000, email="email@example.com",
                                 year_built=datetime(2000, 1, 1), baths=3, beds=5,
                                 listing_date=datetime(2024, 4, 1),
                                 square_feet=2500, parking_spaces="4", air_conditioning=False, balcony=False,
                                 basement='crawl space only', dishwasher=True, hardwood_floor='ground floor')
    return listing_model


@pytest.fixture
def get_test_investor_profile_schema() -> InvestorProfileSchema:
    current_time_string = __get_time_string()
    f_name = "fname" + current_time_string
    l_name = "lname" + current_time_string

    investor_profile_schema = InvestorProfileSchema(
        price=300000, first_name=f_name, last_name=l_name,
        email="email@example.com", title="Ms.", phone="1-888-454-1234",
        preferred_property_types="rental", preferred_locations="SE, NE",
        bedrooms_max=8, bedrooms_min=2, bathrooms_min=2, bathrooms_max=3, budget_max=100000000, budget_min=200000,
        years_built_max=80, years_built_min=30, investment_purpose="rental",
        assigned_parking_required=True, central_heat_required=True, dishwasher_required=True,
        balcony_required=True
    )

    return investor_profile_schema


@pytest.fixture
def get_test_investor_profile_model() -> InvestorProfileModel:
    current_time_string = __get_time_string()
    f_name = "fname" + current_time_string
    l_name = "lname" + current_time_string

    investor_profile_model = InvestorProfileModel(
        price=300000, first_name=f_name, last_name=l_name,
        email="email@example.com", title="Ms.", phone="1-888-454-1234",
        budget_min=343.33, budget_max=2343.00, preferred_property_types="rental",
        bedrooms_max=8, bedrooms_min=2, bathrooms_min=2, bathrooms_max=3, investment_purpose="rental",
    )

    investor_profile_model.years_built_min = 5
    investor_profile_model.years_built_max = 30
    investor_profile_model.assigned_parking_required = True
    investor_profile_model.air_conditioning_required = True
    investor_profile_model.central_heat_required = True
    investor_profile_model.min_roi = 34000.23
    investor_profile_model.preferred_property_types = "Student Rental, Multi-family unit"
    investor_profile_model.preferred_locations = "SE, NE"
    investor_profile_model.dishwasher_required = True
    investor_profile_model.balcony_required = False

    return investor_profile_model


@pytest.fixture
def get_test_financing_model_minimum() -> FinancingModel:
    current_time_string = __get_time_string()

    financing_model = FinancingModel()

    return financing_model


@pytest.fixture
def get_test_financing_schema_minimum() -> FinancingSchema:
    current_time_string = __get_time_string()

    financing_schema = FinancingSchema()

    return financing_schema


@pytest.fixture
def get_test_underwriting_schema() -> UnderwritingSchema:

    underwriting_schema = UnderwritingSchema()

    return underwriting_schema


@pytest.fixture
def get_test_mortgage_schema() -> MortgageSchema:
    issued_date = datetime.now()

    mortgage_schema = MortgageSchema(
        appraisal_value=300000.00, principal=240000.03, issued_date=issued_date,
        pre_qualified=True, pre_approved=True, loan_to_value=80.0, interest_rate=3.75,
        term=3, amortization_period=30, monthly_payment=3565.25,
        owner_occupied=True, insurance=3500.75,
    )
    return mortgage_schema


@pytest.fixture
def get_test_mortgage_model() -> MortgageModel:
    issued_date = datetime.now()

    mortgage_model = MortgageModel(appraisal_value=345555, principal=234343.00, pre_qualified=True,
                                   pre_approved=False, loan_to_value=80.00, term=5, interest_rate=5.0,
                                   amortization_period=30, monthly_payment=2343.55,
                                   owner_occupied=True, insurance=200.00, issued_date=issued_date)

    return mortgage_model


@pytest.fixture
def get_test_address_schema() -> AddressSchema:
    current_time_string = __get_time_string()
    street_address = current_time_string + '_street_address'
    street_address_two = current_time_string + '_street_address_two'
    city = current_time_string + '_city'
    postal_code = current_time_string + '_postal_code'
    country = current_time_string + '_country'
    long_lat_location = current_time_string + '_long_lat_location'

    address_schema = AddressSchema(
        street_address=street_address, street_address_two=street_address_two,
        city=city, postal_code=postal_code, country=country, long_lat_location=long_lat_location, state="ON",
    )

    return address_schema


@pytest.fixture
def get_test_expense_schema() -> ExpenseSchema:
    current_time_string = __get_time_string()
    expense_type = current_time_string + '_expense_type'

    expense_schema = ExpenseSchema(
        expense_type=expense_type, monthly_cost=3343.23,
    )

    return expense_schema


@pytest.fixture
def get_test_expense_model() -> ExpenseModel:
    current_time_string = __get_time_string()
    expense_type = current_time_string + '_expense_type'

    expense_model = ExpenseModel(expense_type=expense_type, monthly_cost=3343.23,
                                 )

    return expense_model


@pytest.fixture
def get_test_email_schema() -> EmailSchema:
    current_time_string = __get_time_string()
    expense_type = current_time_string + '_expense_type'

    email_schema = EmailSchema(
        to_addresses=['rei@zimbasolutions.io'], subject='SES Email Unit Test', sender='rei@zimbasolutions.io',
        body_text='SES Unit Test Email body',
    )

    return email_schema


@pytest.fixture
def get_test_subscription_schema() -> SubscriptionSchema:
    current_time_string = __get_time_string()
    issued_date = datetime.now()
    user_email = current_time_string + '@example.com'
    user_name = current_time_string + '_firstname'
    user_unsubscribe_token = current_time_string + '_token'

    subscription_schema = SubscriptionSchema(
        email=user_email, name=user_name, service_subscribed_to='get_on_shortlist',
        source_url='index.html', form_id='subscribe_to_shortlist', subscribed=True, unsubscribed_date=issued_date,
        unsubscribe_token=user_unsubscribe_token
    )
    return subscription_schema


@pytest.fixture
def get_test_real_state_property_schema_unpopulated() -> RealEstatePropertySchema:
    current_time_string = __get_time_string()
    real_estate_property_schema = RealEstatePropertySchema()
    return real_estate_property_schema


@pytest.fixture
def get_test_real_estate_property_model() -> RealEstatePropertyModel:
    real_estate_property_model = RealEstatePropertyModel()
    return real_estate_property_model  # ensures mappings are correct


def __get_time_string() -> str:
    current_time = datetime.now(timezone.utc)
    mills = int(current_time.timestamp())
    return str(mills)


def __test_db():
    load_dotenv()
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_TEST_NAME')
    DATABASE_URL = f"mysql+pymysql://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    db = None

    try:
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,  # Enables automatic reconnection
            pool_size=20,  # Maximum number of connections to keep persistently
            max_overflow=10,  # Maximum number of connections that can be created beyond pool_size
            echo=True,
        )

        TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = TestSessionLocal()
        return db
    finally:
        db.close()


@pytest.fixture
def get_test_subscription_model() -> SubscriptionModel:
    current_time_string = __get_time_string()
    issued_date = datetime.now()
    user_email = current_time_string + '@example.com'
    user_name = current_time_string + '_firstname'
    user_unsubscribe_token = current_time_string + '_token'

    subscription_model = SubscriptionModel(
        email=user_email, name=user_name, service_subscribed_to='get_on_shortlist',
        source_url='index.html', form_id='subscribe_to_shortlist', subscribed=True, unsubscribed_date=issued_date,
        unsubscribe_token=user_unsubscribe_token
    )
    return subscription_model


@pytest.fixture
def get_test_address_model() -> AddressModel:
    current_time_string = __get_time_string()
    street_address = current_time_string + '_street_address'
    street_address_two = current_time_string + '_street_address_two'
    city = current_time_string + '_city'
    postal_code = current_time_string + '_postal_code'
    state = 'ON'
    country = current_time_string + '_country'
    long_lat_location = current_time_string + '_long_lat_location'

    address_model = AddressModel(
        street_address=street_address, street_address_two=street_address_two,
        city=city, postal_code=postal_code, state=state, country=country, long_lat_location=long_lat_location,
    )
    return address_model


@pytest.fixture
def get_test_underwriting_model_min() -> UnderwritingModel:
    underwriting_model = UnderwritingModel()
    return underwriting_model


@pytest.fixture
def get_test_deal_model() -> DealModel:
    deal_model = DealModel(
        down_payment=34343.33, term=5, interest_rate=5.73, monthly_cost=2333.00, after_repair_value=32424.33,
        time_horizon=23, roi=35.00, capital_invested=234343.00, real_estate_property_value=2343.22, risk_assessment='',
        thumbnail=''
    )
    return deal_model


@pytest.fixture
def get_test_projection_entry_model() -> ProjectionEntryModel:
    current_time_string = __get_time_string()
    project_entry_model = ProjectionEntryModel(
        projection_type=current_time_string + "_type", projection_value=53434.73, projection_position_in_list=0,
    )
    return project_entry_model


@pytest.fixture
def get_test_projection_entry_schema() -> ProjectionEntrySchema:
    current_time_string = __get_time_string()
    project_entry_schema = ProjectionEntrySchema(
        projection_type=current_time_string + "_type", projection_value=53434.73, projection_position_in_list=0,
    )
    return project_entry_schema

@pytest.fixture
def get_test_deal_schema() -> DealSchema:

    deal_schema = DealSchema(
        down_payment=34343.33, term=5, interest_rate=5.73, monthly_cost=2333.00, after_repair_value=32424.33,
        time_horizon=23, roi=35.00, capital_invested=234343.00, real_estate_property_value=2343.22, risk_assessment='',
        thumbnail=''
    )
    return deal_schema


@pytest.fixture
def test_fastapi_client():
    app.dependency_overrides[get_db] = __test_db  # Make sure we use test migrations
    client = TestClient(app)
    yield client


@pytest.fixture
def test_sample_html() -> str:
    DATA_FILE_PATH = Path(__file__).parent / "test_data" / "sample_html_text.html"

    with DATA_FILE_PATH.open() as file:
        html_content = file.read()
        yield html_content
