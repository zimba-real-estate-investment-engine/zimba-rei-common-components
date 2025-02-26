from __future__ import annotations  # Ensures cyclical references are handled correctly

import json
from datetime import datetime
from typing import List, Annotated, Optional, Union

from sqlalchemy import Boolean, Column, String, TIMESTAMP, text, Integer, ForeignKey, Float, Table, TypeDecorator, TEXT, \
    JSON, func, UniqueConstraint, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, declarative_mixin

Base = declarative_base()


@declarative_mixin
class ModelMixin:
    __table__ = None

    @classmethod
    def __declare_first__(cls):
        cls.__table__ = Table(cls.__name__, cls.metadata,
                              Column('id', Integer, primary_key=True))


class JSONType(TypeDecorator):
    """
    This will be handling objects that we want saved as JSON in the database
    """
    impl = TEXT

    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class AmortizationScheduleRowModel(dict):
    def __init__(self, payment_number: int, monthly_payment: float, interest_payment: float, principal_recapture: float,
                 remaining_balance: float, caching_code: AmortizationCachingCodeModel):
        self.payment_number = payment_number
        self.monthly_payment = monthly_payment
        self.interest_payment = interest_payment
        self.principal_recapture = principal_recapture
        self.remaining_balance = remaining_balance
        self.caching_code = caching_code
        dict.__init__(self, payment_number=payment_number, monthly_payment=monthly_payment, interest_payment=interest_payment,
                      principal_recapture=principal_recapture, remaining_balance=remaining_balance,
                      caching_code=caching_code)


class AmortizationCachingCodeModel(dict):
    def __init__(self, principal: float, annual_interest_rate: float, amortization_period: int):
        self.principal = principal
        self.annual_interest_rate = annual_interest_rate
        self.amortization_period = amortization_period
        dict.__init__(self, principal=principal, annual_interest_rate=annual_interest_rate,
                      amortization_period=amortization_period)


class SubscriptionModel(Base):
    __tablename__ = 'subscription'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(255), nullable=False)
    name = Column(String(255))
    service_subscribed_to = Column(String(255))
    source_url = Column(String(255))
    subscribed = Column(Boolean)
    form_id = Column(String(255))
    unsubscribed_date = Column(
        TIMESTAMP,
        server_default=text('CURRENT_TIMESTAMP')
    )
    unsubscribe_token = Column(String(255))
    created_date = Column(
        TIMESTAMP,
        server_default=text('CURRENT_TIMESTAMP')
    )

    def __repr__(self):
        return f"<Subscription(id={self.id}, email={self.email}, subscribed={self.subscribed})>"


class AddressModel(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    street_address = Column(String(255))
    street_address_two = Column(String(255))
    city = Column(String(255))
    state = Column(String(255))
    postal_code = Column(String(255))
    country = Column(String(255))
    long_lat_location = Column(String(255))
    full_address = Column(String(255))

    def __init__(
            self,
            street_address: str,
            street_address_two: str,
            city: str,
            state: str,
            postal_code: str,
            country: str,
            long_lat_location: str,
            full_address: str,
            id: int | None = None,  # Allow none so the migrations creates it for new objects.
    ):
        self.id = id
        self.street_address = street_address
        self.street_address_two = street_address_two
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.country = country
        self.long_lat_location = long_lat_location
        self.full_address = full_address

    def __repr__(self):
        return f"<Address(id={self.id}, city={self.city}, state={self.state})>"


class ListingModel(Base):
    __tablename__ = 'listing'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    address_id = Column(Integer, ForeignKey('address.id'))
    email = Column(String(255))
    price = Column(Float)
    price_amount = Column(Float)
    price_currency_symbol = Column(String(255))
    price_currency_iso_code = Column(String(255))
    beds = Column(TEXT)
    bedrooms = Column(TEXT)
    baths = Column(TEXT)
    bathrooms = Column(TEXT)
    air_conditioning = Column(TEXT)
    parking_spaces = Column(TEXT)
    balcony = Column(Boolean)
    hardwood_floor = Column(String(255))
    dishwasher = Column(TEXT)
    year_built = Column(TIMESTAMP)
    basement = Column(TEXT)
    square_feet = Column(Float)
    listing_date = Column(TIMESTAMP)
    listing_source = Column(String(255))

    address = relationship("AddressModel", uselist=False)

    # def __init__(self, **kwargs):
    #     pass
    def __init__(
            self,
            email: str,
            price: float,
            # property_id: str,
            beds: int,
            bedrooms: int,
            baths: float,
            bathrooms: float,
            air_conditioning: bool,
            parking_spaces: str,
            balcony: bool,
            hardwood_floor: str,
            dishwasher: bool,
            year_built: datetime,
            basement: str,
            square_feet: float,
            listing_date: datetime,
            listing_source: str,
            price_amount: float | None = None,
            price_currency_symbol: str | None = None,
            price_currency_iso_code: str | None = None,
            address: Annotated[Optional[AddressModel], "could be missing"] = None,
            id: int | None = None,  # Allow none so the migrations creates it for new objects.
    ):
        self.address = address
        self.id = id
        self.email = email
        self.beds = beds
        self.bedrooms = bedrooms
        self.price = price
        self.baths = baths
        self.bathrooms = bathrooms
        self.air_conditioning = air_conditioning
        self.parking_spaces = parking_spaces
        self.balcony = balcony
        self.hardwood_floor = hardwood_floor
        self.dishwasher = dishwasher
        self.year_built = year_built
        self.basement = basement
        self.square_feet = square_feet
        self.listing_date = listing_date
        self.listing_source = listing_source
        self.price_amount = price_amount
        self.price_currency_symbol = price_currency_symbol
        self.price_currency_iso_code = price_currency_iso_code
        self.address = address

    def __repr__(self):
        return f"<Listing(id={self.id}, beds={self.beds}, baths={self.baths})>"


class ExpenseModel(Base):
    __tablename__ = 'expense'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    real_estate_property_id = Column(Integer, ForeignKey('real_estate_property.id'))
    expense_type = Column(String(255))
    monthly_cost = Column(Float)

    real_estate_property = relationship("RealEstatePropertyModel", back_populates="expenses")

    def __init__(self, expense_type: str, monthly_cost: float,
                 id: int | None = None,  # Allow none so the migrations creates it for new objects.
                 ):
        self.id = id
        self.expense_type = expense_type
        self.monthly_cost = monthly_cost

    def __repr__(self):
        return f"<Expense(id={self.id}, type={self.expense_type}, monthly_cost=${self.monthly_cost:,.2f})>"


class CashflowModel(Base):
    __tablename__ = 'cashflow'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    real_estate_property_id = Column(Integer, ForeignKey('real_estate_property.id'))
    cashflow_type = Column(String(255))
    monthly_cashflow = Column(Float)

    real_estate_property = relationship("RealEstatePropertyModel", back_populates="cashflow_sources")

    def __init__(self, cashflow_type: str, monthly_cashflow: float,
                 id: int | None = None,  # Allow none so the migrations creates it for new objects.
                 ):
        self.id = id
        self.cashflow_type = cashflow_type
        self.monthly_cashflow = monthly_cashflow

    def __repr__(self):
        return f"<Cashflow(id={self.id}, type={self.cashflow_type}, monthly_cashflow=${self.monthly_cashflow:,.2f})>"


class CapitalInvestmentModel(Base):
    __tablename__ = 'capital_investment'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    real_estate_property_id = Column(Integer, ForeignKey('real_estate_property.id'))
    capital_investment_type = Column(String(255))
    capital_investment_amount = Column(Float)

    real_estate_property = relationship("RealEstatePropertyModel", back_populates="capital_investments")

    def __init__(self, capital_investment_type: str, capital_investment_amount: float,
                 id: int | None = None,  # Allow none so the migrations creates it for new objects.
    ):
        self.id = id
        self.capital_investment_type = capital_investment_type
        self.capital_investment_amount = capital_investment_amount

    def __repr__(self):
        return (f"<CapitalInvestment(id={self.id}, type={self.capital_investment_type}, "
                f"investment_amount=${self.capital_investment_amount:,.2f})>")


class RealEstatePropertyModel(Base):
    __tablename__ = 'real_estate_property'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    address_id = Column(Integer, ForeignKey('address.id'))
    listing_id = Column(Integer, ForeignKey('listing.id'))
    value = Column(Float)

    address = relationship("AddressModel", uselist=False)
    listing = relationship("ListingModel", uselist=False)
    expenses = relationship("ExpenseModel", back_populates="real_estate_property")
    cashflow_sources = relationship("CashflowModel", back_populates="real_estate_property")
    capital_investments = relationship("CapitalInvestmentModel", back_populates="real_estate_property")

    def __init__(
            self,
            listing: Annotated[Optional[ListingModel], 'could be missing'] = None,
            address: Annotated[Optional[AddressModel], 'could be yet to be filled'] = None,
            expenses: Annotated[Optional[List[ExpenseModel]], 'could be yet to be filled'] = None,
            cashflow_sources: Annotated[Optional[List[CashflowModel]], 'could be yet to be filled'] = None,
            capital_investments: Annotated[Optional[List[CapitalInvestmentModel]], 'could be yet to be filled'] = None,
            value: Annotated[Optional[float], 'yet to be filled'] = None,
            id: int | None = None,  # Allow none so the migrations creates it for new objects.
    ):
        self.id = id
        self.listing = listing
        self.address = address
        self.expenses = expenses if expenses else []
        self.cashflow_sources = cashflow_sources if cashflow_sources else []
        self.capital_investments = capital_investments if capital_investments else []
        self.value = value

    def __repr__(self):
        return f"<RealEstateProperty(id={self.id})>"


class FinancingModel(Base):
    __tablename__ = 'financing'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    investor_profile_id = Column(Integer, ForeignKey('investor_profile.id'))

    mortgages = relationship("MortgageModel", back_populates="financing")
    investor_profile = relationship("InvestorProfileModel", back_populates='financing_sources')

    def __init__(
            self,
            mortgages: Annotated[Optional[List[MortgageModel]], 'could be yet to be filled'] = None,
            id: int | None = None,  # Allow none so the migrations creates it for new objects.
    ):
        self.id = id
        self.mortgages = mortgages if mortgages else []

    # def get_total_available(self) -> float:
    #     return sum(mortgage.appraisal_value for mortgage in self.mortgages)

    def __repr__(self):
        return f"<Financing(id={self.id})>"
        # return f"<Financing(id={self.id}, total_available=${self.get_total_available():,.2f})>"


class InvestorProfileModel(Base):
    __tablename__ = 'investor_profile'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    price = Column(Float)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255))
    title = Column(String(255))
    phone = Column(String(255))
    budget_min = Column(Float)
    budget_max = Column(Float)
    bedrooms_min = Column(Integer)
    bedrooms_max = Column(Integer)
    bathrooms_max = Column(Integer)
    bathrooms_min = Column(Integer)
    years_built_min = Column(Integer)
    years_built_max = Column(Integer)
    investment_purpose = Column(String(255))
    assigned_parking_required = Column(Boolean)
    air_conditioning_required = Column(Boolean)
    central_heat_required = Column(Boolean)
    min_roi = Column(Float)
    preferred_property_types = Column(String(255))
    preferred_locations = Column(String(255))
    dishwasher_required = Column(Boolean)
    balcony_required = Column(Boolean)

    financing_sources = relationship("FinancingModel", back_populates="investor_profile")

    def __init__(
            self,
            price: int = 0,
            first_name: str = '',
            last_name: str = '',
            email: str = '',
            title: str = '',
            phone: str = '',
            budget_min: float = 0,
            budget_max: float = 0,
            preferred_property_types: str = '',
            preferred_locations: str = '',
            assigned_parking_required: bool = False,
            bedrooms_min: int = 1,
            bedrooms_max: int = 1,
            bathrooms_min: int = 1,
            bathrooms_max: int = 0,
            years_built_min: int = 0,
            years_built_max: int = 0,
            investment_purpose: str = '',
            central_heat_required: bool = False,
            dishwasher_required: bool = False,
            balcony_required: bool = False,
            financing_sources: Annotated[Optional[List[FinancingModel]], 'could be yet to be filled'] = None,
            id: int | None = None,  # Allow none so the migrations creates it for new objects.
    ):
        self.id = id
        self.price = price
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.title = title
        self.phone = phone
        self.budget_min = budget_min
        self.budget_max = budget_max
        self.preferred_property_types = preferred_property_types
        self.preferred_locations = preferred_locations
        self.assigned_parking_required = assigned_parking_required
        self.bedrooms_min = bedrooms_min
        self.bedrooms_max = bedrooms_max
        self.bathrooms_min = bathrooms_min
        self.bathrooms_max = bathrooms_max
        self.years_built_max = years_built_max
        self.years_built_min = years_built_min
        self.investment_purpose = investment_purpose
        self.central_heat_required = central_heat_required
        self.dishwasher_required = dishwasher_required
        self.balcony_required = balcony_required
        self.financing_sources = financing_sources if financing_sources else []

    def __repr__(self):
        return f"<InvestorProfile(id={self.id})>"
        # return f"<InvestorProfile(id={self.id}, budget_range=${self.budget_min:,.2f}-${self.budget_max:,.2f})>"


class MortgageModel(Base):
    __tablename__ = 'mortgage'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    financing_id = Column(String(255), ForeignKey('financing.id'))
    amortization_schedule_id = Column(Integer, ForeignKey('amortization_schedule.id'))
    appraisal_value = Column(Float)
    principal = Column(Float)
    down_payment = Column(Float)
    issued_date = Column(TIMESTAMP)
    pre_qualified = Column(Boolean)
    pre_approved = Column(Boolean)
    loan_to_value = Column(Float)
    annual_interest_rate = Column(Float)
    term = Column(Integer)
    amortization_period = Column(Integer)
    monthly_payment = Column(Float)
    owner_occupied = Column(Boolean)
    insurance = Column(Float)

    financing = relationship("FinancingModel", back_populates="mortgages")
    amortization_schedule = relationship("AmortizationScheduleModel")

    def __init__(
            self,
            appraisal_value: float,
            principal: float,
            down_payment: float,
            issued_date: datetime,
            pre_qualified: bool,
            pre_approved: bool,
            loan_to_value: float,
            term: int,
            annual_interest_rate: float,
            amortization_period: int,
            monthly_payment: float,
            owner_occupied: bool,
            insurance: float,
            amortization_schedule: Annotated[Optional[AmortizationScheduleModel], "populate before saving"] = None,
            financing: Annotated[Optional[FinancingModel], 'could be yet to be filled'] = None,
            id: int | None = None,  # Allow none so the migrations creates it for new objects.
    ):
        self.id = id
        self.appraisal_value = appraisal_value
        self.principal = principal
        self.down_payment = down_payment
        self.issued_date = issued_date
        self.pre_qualified = pre_qualified
        self.pre_approved = pre_approved
        self.loan_to_value = loan_to_value
        self.term = term
        self.annual_interest_rate = annual_interest_rate
        self.amortization_period = amortization_period
        self.monthly_payment = monthly_payment
        self.owner_occupied = owner_occupied
        self.insurance = insurance
        self.amortization_schedule = amortization_schedule
        self.financing = financing

    def __repr__(self):
        return f"<Mortgage(id={self.id}, principal=${self.principal:,.2f}, term={self.term}mo)>"


class UnderwritingModel(Base):
    __tablename__ = 'underwriting'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    investor_profile_id = Column(Integer, ForeignKey('investor_profile.id'))
    real_estate_property_id = Column(Integer, ForeignKey('real_estate_property.id'))

    investor_profile = relationship("InvestorProfileModel")
    real_estate_property = relationship("RealEstatePropertyModel")
    deals = relationship("DealModel", back_populates="underwriting")
    projection_entries = relationship("ProjectionEntryModel", back_populates="underwriting")

    def __init__(
            self,
            investor_profile: Annotated[Optional[InvestorProfileModel], 'could be yet to be filled'] = None,
            real_estate_property: Annotated[Optional[RealEstatePropertyModel], 'could be yet to be filled'] = None,
            deals: Annotated[Optional[DealModel], 'could be yet to be filled'] = None,
            id: int | None = None,  # Allow none so the migrations creates it for new objects.
    ):
        self.id = id
        self.investor_profile = investor_profile
        self.real_estate_property = real_estate_property
        self.deals = deals if deals else []

    def __repr__(self):
        return f"<UnderwritingProcess(id={self.id})>"


class DealModel(Base):
    __tablename__ = 'deal'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    underwriting_id = Column(Integer, ForeignKey('underwriting.id'))
    real_estate_property_id = Column(Integer, ForeignKey('real_estate_property.id'))
    down_payment = Column(Float)
    term = Column(Integer)
    interest_rate = Column(Float)
    monthly_cost = Column(Float)
    after_repair_value = Column(Float)
    time_horizon = Column(Integer)
    roi = Column(Float)
    capital_invested = Column(Float)
    real_estate_property_value = Column(Float)
    thumbnail = Column(String(255))
    risk_assessment = Column(String(255))

    underwriting = relationship("UnderwritingModel")
    real_estate_property = relationship("RealEstatePropertyModel")

    def __init__(
            self,
            down_payment: float,
            term: int,
            interest_rate: float,
            monthly_cost: float,
            after_repair_value: float,
            time_horizon: int,
            roi: float,
            capital_invested: float,
            real_estate_property_value: float,
            underwriting: Annotated[Optional[UnderwritingModel], 'should be populated before saving to db'] = None,
            real_estate_property: Annotated[Optional[RealEstatePropertyModel], 'populate before saving to db'] = None,
            thumbnail: str = "placeholder_thumbnail_url",
            risk_assessment: str = "default_risk_assessment",
            id: int | None = None,  # Allow none so the migrations creates it for new objects.
    ):
        self.id = id
        self.down_payment = down_payment
        self.term = term
        self.interest_rate = interest_rate
        self.monthly_cost = monthly_cost
        self.after_repair_value = after_repair_value
        self.time_horizon = time_horizon
        self.roi = roi
        self.capital_invested = capital_invested
        self.real_estate_property_value = real_estate_property_value
        self.underwriting = underwriting
        self.real_estate_property = real_estate_property
        self.thumbnail = thumbnail
        self.risk_assessment = risk_assessment

    def __repr__(self):
        return (f"<Deal(id={self.id}, real_estate_property_value=${self.real_estate_property_value:,.2f}, "
                f"roi={self.roi}%)>")


class ProjectionEntryModel(Base):
    __tablename__ = 'projection_entry'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    underwriting_id = Column(Integer, ForeignKey('underwriting.id'))
    projection_type = Column(String(255))
    projection_value = Column(Float)
    projection_position_in_list = Column(Integer)

    underwriting = relationship("UnderwritingModel")

    def __init__(
            self,
            projection_type: str,
            projection_value: float,
            projection_position_in_list: int,
            underwriting: Annotated[Optional[UnderwritingModel], 'should be populated before saving to db'] = None,
            id: int | None = None,  # Allow none so the migrations creates it for new objects.
    ):
        self.id = id
        self.projection_type = projection_type
        self.projection_value = projection_value
        self.projection_position_in_list = projection_position_in_list
        self.underwriting = underwriting

    def __repr__(self):
        return f"<Projection(id={self.id})>"


class AmortizationScheduleModel(Base):
    __tablename__ = 'amortization_schedule'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    amortization_schedule_json = Column(String(255))
    caching_code: AmortizationCachingCodeModel = Column(JSON)
    # caching_code = Column(JSON)
    principal = Column(Float)
    annual_interest_rate = Column(Float)
    amortization_period = Column(Integer)
    created_date = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    def set_caching_code(self, caching_code_instance):
        self.caching_code = caching_code_instance.to_dict()


    def __init__(
            self,
            caching_code: AmortizationCachingCodeModel,
            amortization_schedule_json: str,
            created_date: datetime,
            principal: float,
            annual_interest_rate: float,
            amortization_period: int,
            id: int | None = None,  # Allow none so the migrations creates it for new objects.
    ):
        self.id = id
        self.amortization_schedule_json = amortization_schedule_json
        self.created_date = created_date
        self.caching_code = caching_code
        self.principal = principal
        self.annual_interest_rate = annual_interest_rate
        self.amortization_period = amortization_period

    def __repr__(self):
        return f"<AmortizationSchedule(id={self.id} amortization_caching_code={self.amortization_caching_code})>"


class LLMResponseModel(Base):
    __tablename__ = 'llm_response'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    listing_url = Column(String(255))
    listing_raw_text = Column(String(20000))
    llm_service_api_url = Column(String(255))
    llm_service_prompt = Column(String(20000))
    llm_response_json = Column(String(20000))
    created_date = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    def __init__(
            self,
            listing_url: str,
            listing_raw_text: str,
            llm_service_api_url: str,
            llm_service_prompt: str,
            llm_response_json: str,
            created_date: datetime,
            id: int | None = None,  # Allow none so the migrations creates it for new objects.
    ):
        self.id = id
        self.listing_url = listing_url
        self.listing_raw_text = listing_raw_text
        self.llm_service_api_url = llm_service_api_url
        self.llm_service_prompt = llm_service_prompt
        self.llm_response_json = llm_response_json
        self.created_date = created_date

    def __repr__(self):
        return f"<LLMResponse(id={self.id} listing_url={self.listing_url})>"


class ProjectionModel(Base):
    __tablename__ = 'projection'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    deal_id = Column(Integer, ForeignKey('deal.id'))
    amortization_schedule_id = Column(Integer, ForeignKey('amortization_schedule.id'))
    projection_json = Column(String(255))
    created_date = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    property_value = Column(Float)
    passive_appreciation_percentage = Column(Float)
    active_appreciation_percentage = Column(Float)
    deal = relationship("DealModel")
    amortization_schedule = relationship("AmortizationScheduleModel")

    def __init__(
            self,
            projection_json: str,
            created_date: datetime,
            deal: Annotated[Optional[DealModel], 'should be populated before saving to db'] = None,
            amortization_schedule: Annotated[Optional[AmortizationScheduleModel], 'populate before saving'] = None,
            property_value: Annotated[Optional[float], 'populate before saving'] = None,
            passive_appreciation_percentage: Annotated[Optional[float], 'populate before saving'] = None,
            active_appreciation: Annotated[Optional[float], 'populate before saving'] = None,
            id: int | None = None,  # Allow none so the migrations creates it for new objects.
    ):
        self.id = id
        self.deal = deal
        self.projection_json = projection_json
        self.created_date = created_date
        self.amortization_schedule = amortization_schedule
        self.property_value = property_value
        self.passive_appreciation_percentage = passive_appreciation_percentage
        self.active_appreciation = active_appreciation

    def __repr__(self):
        return f"<Projection(id={self.id} deal={self.deal.id})>"


class DropdownOptionModel(Base):
    __tablename__ = 'dropdown_option'

    id = Column(Integer, primary_key=True, autoincrement=True)
    dropdown_name = Column(String(100), nullable=False)
    value = Column(String(255), nullable=False)
    label = Column(String(255), nullable=True)
    order_index = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, default=func.current_timestamp(), onupdate=func.current_timestamp())

   # Indexes
    __table_args__ = (
        UniqueConstraint('dropdown_name', 'value', name='unique_key_dropdown_value'),
        Index('idx_dropdown_value', 'dropdown_name', 'value'),
        Index('idx_label', 'label'),
        Index('idx_order', 'dropdown_name', 'order_index'),
    )


    def __init__(
            self,
            dropdown_name: str,
            value: str,
            label: str,
            is_active: bool,
            order_index: Annotated[Optional[int], 'populate before saving'] = None,
            id: int | None = None,  # Allow none so the migrations creates it for new objects.
    ):
        self.id = id
        self.dropdown_name = dropdown_name
        self.value = value
        self.label = label
        self.order_index = order_index
        self.is_active = is_active

    def __repr__(self):
        return f"<DropdownOption(id={self.id}, dropdown_name='{self.dropdown_name}', label='{self.label}, value='{self.value}')>"
