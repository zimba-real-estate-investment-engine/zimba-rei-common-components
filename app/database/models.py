from __future__ import annotations  # Ensures cyclical references are handled correctly
from datetime import datetime
from typing import List, Annotated, Optional

from sqlalchemy import Boolean, Column, String, TIMESTAMP, text, Integer, ForeignKey, Float, Table
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
    beds = Column(Integer)
    baths = Column(Float)
    air_conditioning = Column(Boolean)
    parking_spaces = Column(String(255))
    balcony = Column(Boolean)
    hardwood_floor = Column(String(255))
    dishwasher = Column(Boolean)
    year_built = Column(TIMESTAMP)
    basement = Column(String(255))
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
            baths: float,
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
            address: Annotated[Optional[AddressModel], "could be missing"] = None,
            id: int | None = None,  # Allow none so the migrations creates it for new objects.
    ):
        self.address = address
        self.id = id
        self.email = email
        self.beds = beds
        self.price = price
        self.baths = baths
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


# class CapitalInvestedModel(Base):
#     __tablename__ = 'capital_invested'
#
#     id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
#     real_estate_property_id = Column(Integer, ForeignKey('real_estate_property.id'))
#     investment_type = Column(String(255))
#     investment_amount = Column(Float)
#
#     real_estate_property = relationship("RealEstatePropertyModel", back_populates="capital_invested")
#
#     def __init__(self, investment_type: str, investment_amount: float,
#                  id: int | None = None,  # Allow none so the migrations creates it for new objects.
#     ):
#         self.id = id
#         self.investment_type = investment_type
#         self.investment_amount = investment_amount
#
#     def __repr__(self):
#         return f"<CapitalInvestment(id={self.id}, type={self.investment_type}, investment_amount=${self.investment_amount:,.2f})>"
#

class RealEstatePropertyModel(Base):
    __tablename__ = 'real_estate_property'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    address_id = Column(Integer, ForeignKey('address.id'))
    listing_id = Column(Integer, ForeignKey('listing.id'))

    address = relationship("AddressModel", uselist=False)
    listing = relationship("ListingModel", uselist=False)
    expenses = relationship("ExpenseModel", back_populates="real_estate_property")
    cashflow_sources = relationship("CashflowModel", back_populates="real_estate_property")
    # capital_investments = relationship("CapitalInvestmentModel", back_populates="real_estate_property")

    def __init__(
            self,
            listing: Annotated[Optional[ListingModel], 'could be missing'] = None,
            address: Annotated[Optional[AddressModel], 'could be yet to be filled'] = None,
            expenses: Annotated[Optional[List[ExpenseModel]], 'could be yet to be filled'] = None,
            cashflow_sources: Annotated[Optional[List[CashflowModel]], 'could be yet to be filled'] = None,
            # capital_investments: Annotated[Optional[List[CapitalInvestedModel]], 'could be yet to be filled'] = None,
            id: int | None = None,  # Allow none so the migrations creates it for new objects.
    ):
        self.id = id
        self.listing = listing
        self.address = address
        self.expenses = expenses if expenses else []
        self.cashflow_sources = cashflow_sources if cashflow_sources else []
        # self.capital_investments = capital_investments if capital_investments else []

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
    appraisal_value = Column(Float)
    principal = Column(Float)
    down_payment = Column(Float)
    issued_date = Column(TIMESTAMP)
    pre_qualified = Column(Boolean)
    pre_approved = Column(Boolean)
    loan_to_value = Column(Float)
    interest_rate = Column(Float)
    term = Column(Integer)
    amortization_period = Column(Integer)
    monthly_payment = Column(Float)
    owner_occupied = Column(Boolean)
    insurance = Column(Float)

    financing = relationship("FinancingModel", back_populates="mortgages")

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
            interest_rate: float,
            amortization_period: int,
            monthly_payment: float,
            owner_occupied: bool,
            insurance: float,
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
        self.interest_rate = interest_rate
        self.amortization_period = amortization_period
        self.monthly_payment = monthly_payment
        self.owner_occupied = owner_occupied
        self.insurance = insurance
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
            thumbnail: str = '',
            risk_assessment: str = '',
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
        self.thumbnail = thumbnail
        self.risk_assessment = risk_assessment

    def __repr__(self):
        return f"<Deal(id={self.id}, property_value=${self.property_value:,.2f}, roi={self.roi}%)>"


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
    caching_code = Column(String(255))
    principal = Column(Float)
    annual_interest_rate = Column(Float)
    amortization_period = Column(Integer)
    created_date = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

    def __init__(
            self,
            amortization_schedule_json: str,
            created_date: datetime,
            caching_code: str,
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
        return f"<AmortizationSchedule(id={self.id} caching_code={self.caching_code})>"
