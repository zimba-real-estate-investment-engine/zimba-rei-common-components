from __future__ import annotations

import json
import os
import random
import time
from typing import List
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from time import timezone
from urllib.parse import quote_plus
from fastapi.testclient import TestClient

from app.domain.Expense import Expense
from app.domain.Mortgage import Mortgage
from app.domain.underwriting.AmortizationCachingCode import AmortizationCachingCode
from app.domain.underwriting.AmortizationSchedule import AmortizationSchedule
from app.main import app, get_db
from app.database.models import AddressModel, RealEstatePropertyModel, ListingModel, ExpenseModel, InvestorProfileModel, \
    FinancingModel, MortgageModel, SubscriptionModel, UnderwritingModel, DealModel, ProjectionEntryModel, \
    AmortizationScheduleModel, CashflowModel, CapitalInvestmentModel, AmortizationCachingCodeModel, \
    AmortizationScheduleRowModel, LLMResponseModel, ProjectionModel
from app.database.models import RealEstatePropertyModel
from datetime import datetime, timezone, timedelta

from dateutil.relativedelta import relativedelta

from app.schemas.AmortizationCachingCodeSchema import AmortizationCachingCodeSchema
from app.schemas.CapitalInvestmentSchema import CapitalInvestmentSchema
from app.schemas.CashflowSchema import CashflowSchema
from app.schemas.LLMResponseSchema import LLMResponseSchema
from app.schemas.ListingSchema import ListingSchema
from app.schemas.DealSchema import DealSchema
from app.schemas.FinancingSchema import FinancingSchema
from app.schemas.InvestorProfileSchema import InvestorProfileSchema
from app.schemas.ProjectionEntrySchema import ProjectionEntrySchema
from app.schemas.ProjectionSchema import ProjectionSchema
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
                                   bathrooms=3, bedrooms=5, listing_date=datetime(2024, 4, 1),
                                   square_feet=2500, parking_spaces="4", air_conditioning=True, balcony=False,
                                   basement='crawl space only', dishwasher=True, hardwood_floor='ground floor',
                                   listing_source='http://default.com/' + current_time_string)
    return listing_schema


@pytest.fixture
def get_test_listing_model() -> ListingModel:
    current_time_string = __get_time_string()
    listing_model = ListingModel(price=300000, email="email@example.com",
                                 year_built=datetime(2000, 1, 1), baths=3, bathrooms=3, beds=5,
                                 bedrooms=5, listing_date=datetime(2024, 4, 1),
                                 square_feet=2500, parking_spaces="4", air_conditioning=False, balcony=False,
                                 basement='crawl space only', dishwasher=True, hardwood_floor='ground floor',
                                 listing_source='http://default.com/' + current_time_string)
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
        appraisal_value=300000.00, principal=240000.03, down_payment=27665, issued_date=issued_date,
        pre_qualified=True, pre_approved=True, loan_to_value=80.0, annual_interest_rate=3.75,
        term=3, amortization_period=30, monthly_payment=3565.25,
        owner_occupied=True, insurance=3500.75,
    )
    return mortgage_schema


@pytest.fixture
def get_test_mortgage_model() -> MortgageModel:
    issued_date = datetime.now()

    mortgage_model = MortgageModel(appraisal_value=345555, principal=234343.00, down_payment=27665, pre_qualified=True,
                                   pre_approved=False, loan_to_value=80.00, term=5, interest_rate=5.0,
                                   amortization_period=30, monthly_payment=2343.55,
                                   owner_occupied=True, insurance=200.00, issued_date=issued_date)

    return mortgage_model


@pytest.fixture
def get_test_mortgage() -> Mortgage:
    issued_date = datetime.now()
    principal = round(random.uniform(500000, 13000000), 2)
    annual_interest_rate = round(random.uniform(1.75, 45.0), 2)
    amortization_period = random.randint(1, 40)

    mortgage = Mortgage(principal=principal, annual_interest_rate=annual_interest_rate,
                        amortization_period=amortization_period)

    yield mortgage


@pytest.fixture
def get_test_address_schema() -> AddressSchema:
    current_time_string = __get_time_string()
    street_address = current_time_string + '_street_address'
    street_address_two = current_time_string + '_street_address_two'
    city = current_time_string + '_city'
    postal_code = current_time_string + '_postal_code'
    country = current_time_string + '_country'
    long_lat_location = current_time_string + '_long_lat_location'
    full_address = current_time_string + '_full_address'

    address_schema = AddressSchema(
        street_address=street_address, street_address_two=street_address_two,
        city=city, postal_code=postal_code, country=country, long_lat_location=long_lat_location, state="ON",
        full_address=full_address,
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

    expense_model = ExpenseModel(expense_type=expense_type, monthly_cost=3343.23)

    return expense_model


def CashflowModelModel(cashflow_type, monthly_cost):
    pass


@pytest.fixture
def get_test_cashflow_model() -> CashflowModel:
    current_time_string = __get_time_string()
    cashflow_type = current_time_string + '_cashflow_type'
    monthly_cashflow = round(random.uniform(50000, 130000), 2)

    cashflow_model = CashflowModel(cashflow_type=cashflow_type, monthly_cashflow=monthly_cashflow)

    return cashflow_model


@pytest.fixture
def get_test_cashflow_schema() -> CashflowSchema:
    current_time_string = __get_time_string()
    cashflow_type = current_time_string + '_cashflow_type'
    monthly_cashflow = round(random.uniform(50000, 130000), 2)

    cashflow_schema = CashflowSchema(cashflow_type=cashflow_type, monthly_cashflow=monthly_cashflow)

    return cashflow_schema


@pytest.fixture
def get_test_capital_investment_model() -> CapitalInvestmentModel:
    current_time_string = __get_time_string()
    capital_investment_type = current_time_string + '_cashflow_type'
    capital_investment_amount = round(random.uniform(50000, 130000), 2)

    capital_investment_model = CapitalInvestmentModel(capital_investment_type=capital_investment_type,
                                                      capital_investment_amount=capital_investment_amount)

    return capital_investment_model


@pytest.fixture
def get_test_capital_investment_schema() -> CapitalInvestmentSchema:
    current_time_string = __get_time_string()
    capital_investment_type = current_time_string + '_cashflow_type'
    capital_investment_amount = round(random.uniform(50000, 130000), 2)

    capital_investment_schema = CapitalInvestmentSchema(capital_investment_type=capital_investment_type,
                                                        capital_investment_amount=capital_investment_amount)

    return capital_investment_schema


@pytest.fixture
def get_test_email_schema() -> EmailSchema:
    current_time_string = __get_time_string()
    subject = current_time_string + '_SES Email Unit Test'

    email_schema = EmailSchema(
        to_addresses=['rei@zimbasolutions.io'], subject=subject, sender='rei@zimbasolutions.io',
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
    full_address = current_time_string + '_long_lat_location'

    address_model = AddressModel(
        street_address=street_address, street_address_two=street_address_two,
        city=city, postal_code=postal_code, state=state, country=country, long_lat_location=long_lat_location,
        full_address=full_address
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
    down_payment = round(random.uniform(130000, 150000000), 2)
    real_estate_property_value = round(random.uniform(130000, 150000000), 2)
    after_repair_value = round(random.uniform(13000, 15000000), 2)
    monthly_cost = round(random.uniform(1, 20000), 2)
    capital_invested = round(random.uniform(1, 100000000), 2)
    roi = round(random.uniform(1, 200), 2)
    annual_interest_rate = round(random.uniform(2, 50), 2)
    term = random.randint(1, 10)
    time_horizon = random.randint(1, 120)

    deal_schema = DealSchema(
        down_payment=down_payment, term=term, interest_rate=annual_interest_rate, monthly_cost=monthly_cost,
        after_repair_value=after_repair_value, time_horizon=time_horizon, roi=roi, capital_invested=capital_invested,
        real_estate_property_value=real_estate_property_value, risk_assessment='',
        thumbnail='', underwriting=None
    )
    return deal_schema


@pytest.fixture
def test_fastapi_client():
    app.dependency_overrides[get_db] = __test_db  # Make sure we use test migrations
    client = TestClient(app)
    yield client


@pytest.fixture
def test_sample_html() -> str:
    data_file_path = Path(__file__).parent / "test_data" / "sample_html_text.html"

    with data_file_path.open() as file:
        html_content = file.read()
        yield html_content


@pytest.fixture
def test_sample_realtor_ca_html() -> str:
    data_file_path = Path(__file__).parent / "test_data" / "sample_realtor_ca_listing.html"

    with data_file_path.open() as file:
        html_content = file.read()
        yield html_content


@pytest.fixture
def test_sample_raw_text() -> str:
    data_file_path = Path(__file__).parent / "test_data" / "sample_raw_text.txt"

    with data_file_path.open() as file:
        raw_text = file.read()
        yield raw_text


@pytest.fixture
def test_sample_listing_openai_response_realtor_ca_json_string() -> str:
    data_file_path = Path(__file__).parent / "test_data" / "sample_listing_openai_realtor_ca_response.json"

    with data_file_path.open() as file:
        json_string = file.read()
        yield json_string


@pytest.fixture
def test_sample_listing_openai_response_redfin_ca_json_string() -> str:
    data_file_path = Path(__file__).parent / "test_data" / "sample_listing_openai_redfin_ca_response_151024056.json"

    with data_file_path.open() as file:
        json_string = file.read()
        yield json_string


@pytest.fixture
def test_expenses_schema_list() -> List[ExpenseSchema]:
    expenses_list: List[ExpenseSchema] = [ExpenseSchema(expense_type='Parking', monthly_cost=20.0),
                                          ExpenseSchema(expense_type='Gardening', monthly_cost=50.0),
                                          ExpenseSchema(expense_type='Snow removal', monthly_cost=25.0),
                                          ExpenseSchema(expense_type='Cleaning', monthly_cost=200.0)]

    return expenses_list


@pytest.fixture
def test_amortization_json() -> str:
    data_file_path = Path(__file__).parent / "test_data" / "amortization_schedule.jsonl"

    with data_file_path.open() as file:
        json_string = file.read()
        yield json_string


@pytest.fixture
def test_amortization_schedule_model_without_json() -> AmortizationScheduleModel:
    principal = round(random.uniform(130000, 150000000), 2)
    annual_interest_rate = round(random.uniform(2, 50), 2)
    amortization_period = random.randint(1, 50)
    caching_code = f'{principal}:{annual_interest_rate}:{amortization_period}'
    caching_code = AmortizationCachingCodeModel(principal=principal, annual_interest_rate=annual_interest_rate,
                                                amortization_period=amortization_period)

    amortization_schedule_model = AmortizationScheduleModel(
        amortization_schedule_json='', created_date=datetime.now(), caching_code=caching_code,
        principal=principal, amortization_period=amortization_period, annual_interest_rate=annual_interest_rate
    )

    return amortization_schedule_model


@pytest.fixture
def test_amortization_schedule_without_json() -> AmortizationSchedule:
    principal = round(random.uniform(130000, 150000000), 2)
    annual_interest_rate = round(random.uniform(2, 50), 2)
    amortization_period = random.randint(1, 50)
    caching_code = f'{principal}:{annual_interest_rate}:{amortization_period}'
    caching_code = AmortizationCachingCode(principal=principal, annual_interest_rate=annual_interest_rate,
                                           amortization_period=amortization_period)

    amortization_schedule = AmortizationSchedule(
        amortization_schedule_json='', created_date=datetime.now(), caching_code=caching_code,
        principal=principal, amortization_period=amortization_period, annual_interest_rate=annual_interest_rate
    )

    return amortization_schedule


@pytest.fixture
def test_projection_model() -> ProjectionModel:
    json_list = data = \
        [
            {
                "projection_position": 0,
                "monthly_value": 234556.00,
                "mortgage_value": 232333.00,
                "monthly_cashflow": 2534.95,
                "principal_recapture": 504.34,
                "passive_appreciation": 2230.22
            },
            {
                "projection_position": 1,
                "monthly_value": 234556.00,
                "mortgage_value": 232333.00,
                "monthly_cashflow": 2534.95,
                "principal_recapture": 504.34,
                "passive_appreciation": 2230.22
            },
            {
                "projection_position": 2,
                "monthly_value": 234556.00,
                "mortgage_value": 232333.00,
                "monthly_cashflow": 2534.95,
                "principal_recapture": 504.34,
                "passive_appreciation": 2230.22
            }
        ]
    json_string = json.dumps(json_list)

    property_value = round(random.uniform(130000, 150000000), 2)
    active_appreciation = round(random.uniform(5, property_value), 2)
    projection_model = ProjectionModel(created_date=datetime.now(), projection_json=json_string,
                                       property_value=property_value, passive_appreciation_percentage=3.0,
                                       active_appreciation=active_appreciation)

    return projection_model


@pytest.fixture
def test_projection_schema() -> ProjectionSchema:
    json_list = data = \
        [
            {
                "projection_position": 0,
                "monthly_value": 234556.00,
                "mortgage_value": 232333.00,
                "monthly_cashflow": 2534.95,
                "principal_recapture": 504.34,
                "passive_appreciation": 2230.22
            },
            {
                "projection_position": 1,
                "monthly_value": 234556.00,
                "mortgage_value": 232333.00,
                "monthly_cashflow": 2534.95,
                "principal_recapture": 504.34,
                "passive_appreciation": 2230.22
            },
            {
                "projection_position": 2,
                "monthly_value": 234556.00,
                "mortgage_value": 232333.00,
                "monthly_cashflow": 2534.95,
                "principal_recapture": 504.34,
                "passive_appreciation": 2230.22
            }
        ]
    json_string = json.dumps(json_list)
    property_value = round(random.uniform(130000, 150000000), 2)
    active_appreciation = round(random.uniform(5, property_value), 2)
    projection_schema = ProjectionSchema(created_date=datetime.now(), projection_json=json_string,
                                         property_value=property_value, passive_appreciation_percentage=3.0,
                                         active_appreciation=active_appreciation)

    return projection_schema


@pytest.fixture
def test_amortization_caching_code_model() -> AmortizationCachingCodeModel:
    principal = round(random.uniform(130000, 150000000), 2)
    annual_interest_rate = round(random.uniform(2, 50), 2)
    amortization_period = random.randint(1, 50)
    caching_code = AmortizationCachingCodeModel(principal=principal, annual_interest_rate=annual_interest_rate,
                                                amortization_period=amortization_period)
    return caching_code


@pytest.fixture
def test_amortization_caching_code_schema() -> AmortizationCachingCodeSchema:
    principal = round(random.uniform(130000, 150000000), 2)
    annual_interest_rate = round(random.uniform(2, 50), 2)
    amortization_period = random.randint(1, 50)
    caching_code = AmortizationCachingCodeSchema(principal=principal, annual_interest_rate=annual_interest_rate,
                                                 amortization_period=amortization_period)
    return caching_code


@pytest.fixture
def test_amortization_schedule_row_model() -> AmortizationScheduleRowModel:
    principal = round(random.uniform(130000, 150000000), 2)
    annual_interest_rate = round(random.uniform(2, 50), 2)
    amortization_period = random.randint(1, 50)
    caching_code = AmortizationCachingCodeModel(principal=principal, annual_interest_rate=annual_interest_rate,
                                                amortization_period=amortization_period)

    payment_number = random.randint(1, 30)
    monthly_payment = round(random.uniform(5000, 25000), 2)
    interest_payment = round(random.uniform(1000, 250), 2)
    principal_recapture = round(random.uniform(0, 5000), 2)
    remaining_balance = round(random.uniform(0, 250000), 2)
    amortization_schedule_row = AmortizationScheduleRowModel(
        payment_number=payment_number, monthly_payment=monthly_payment, interest_payment=interest_payment,
        principal_recapture=principal_recapture, remaining_balance=remaining_balance,
        caching_code=caching_code
    )

    return amortization_schedule_row


@pytest.fixture
def test_llm_response_model_no_listing_json() -> LLMResponseModel:
    created_date = datetime.now()
    current_time_string = __get_time_string()

    test_llm_response = LLMResponseModel(
        listing_url='https://example.com/listing',
        listing_raw_text=current_time_string + '_test_sample_raw_text',
        llm_service_api_url='https://sample_llms_server.example.com/_' + current_time_string,
        llm_service_prompt=current_time_string + '_example_sample_response',
        llm_response_json=current_time_string + '_test_sample_listing_openai_response_redfin_ca_json_string',
        created_date=created_date
    )

    yield test_llm_response


@pytest.fixture
def test_llm_response_schema_no_listing_json() -> LLMResponseSchema:
    created_date = datetime.now()
    current_time_string = __get_time_string()

    test_llm_response = LLMResponseSchema(
        listing_url='https://example.com/listing',
        listing_raw_text=current_time_string + '_test_sample_raw_text',
        llm_service_api_url='https://sample_llms_server.example.com/_' + current_time_string,
        llm_service_prompt=current_time_string + '_example_sample_response',
        llm_response_json=current_time_string + '_test_sample_listing_openai_response_redfin_ca_json_string',
        created_date=created_date
    )

    yield test_llm_response
