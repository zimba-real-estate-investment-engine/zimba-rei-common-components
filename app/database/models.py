from datetime import datetime
from typing import List

from sqlalchemy import Boolean, Column, String, TIMESTAMP, text, Integer, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


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

    id = Column(Integer, primary_key=True, nullable=False)
    street_address = Column(String(255))
    street_address_two = Column(String(255))
    city = Column(String(255))
    state = Column(String(255))
    postal_code = Column(String(255))
    country = Column(String(255))
    long_lat_location = Column(String(255))

    def __init__(
            self,
            id: int,
            street_address: str,
            street_address_two: str,
            city: str,
            state: str,
            postal_code: str,
            country: str,
            long_lat_location: str
    ):
        self.id = id
        self.street_address = street_address
        self.street_address_two = street_address_two
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.country = country
        self.long_lat_location = long_lat_location

    def __repr__(self):
        return f"<Address(id={self.id}, city={self.city}, state={self.state})>"


class ListingModel(Base):
    __tablename__ = 'listing'

    id = Column(Integer, primary_key=True, nullable=False)
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

    def __init__(
            self,
            id: int,
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
            listing_date: datetime
    ):
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

    def __repr__(self):
        return f"<Listing(id={self.id}, beds={self.beds}, baths={self.baths})>"


class RealEstatePropertyModel(Base):
    __tablename__ = 'real_estate_property'

    id = Column(Integer, primary_key=True, nullable=False)
    address_id = Column(Integer, ForeignKey('address.id'))
    listing_id = Column(Integer, ForeignKey('listing.id'))

    address = relationship("AddressModel", uselist=False)
    listing = relationship("ListingModel", uselist=False)
    expenses = relationship("ExpenseModel", back_populates="real_estate_property")

    def __init__(self):
        pass

    def __repr__(self):
        return f"<RealEstateProperty(id={self.id})>"


class ExpenseModel(Base):
    __tablename__ = 'expense'

    id = Column(Integer, primary_key=True, nullable=False)
    real_estate_property_id = Column(Integer, ForeignKey('real_estate_property.id'))
    expense_type = Column(String(255))
    monthly_cost = Column(Float)

    real_estate_property = relationship("RealEstatePropertyModel", back_populates="expenses")

    def __init__(self, id: int, expense_type: str, monthly_cost: float):
        self.id = id
        self.expense_type = expense_type
        self.monthly_cost = monthly_cost

    def __repr__(self):
        return f"<Expense(id={self.id}, type={self.expense_type}, monthly_cost=${self.monthly_cost:,.2f})>"


class InvestorProfileModel(Base):
    __tablename__ = 'investor_profile'

    id = Column(Integer, primary_key=True, nullable=False)
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
            bedrooms_min: int = 1,
            bedrooms_max: int = 1,
            bathrooms_min: int = 1,
            bathrooms_max: int = 0,
            investment_purpose: str = '',
    ):
        self.price = price
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.title = title
        self.phone = phone
        self.budget_min = budget_min
        self.budget_max = budget_max
        self.preferred_property_types = preferred_property_types
        self.bedrooms_min = bedrooms_min
        self.bedrooms_max = bedrooms_max
        self.bathrooms_min = bathrooms_min
        self.bathrooms_max = bathrooms_max
        self.investment_purpose = investment_purpose

    def __repr__(self):
        return f"<InvestorProfile(id={self.id}, budget_range=${self.budget_min:,.2f}-${self.budget_max:,.2f})>"


class FinancingModel(Base):
    __tablename__ = 'financing'

    id = Column(Integer, primary_key=True, nullable=False)
    investor_profile_id = Column(Integer, ForeignKey('investor_profile.id'))
    mortgages = relationship("MortgageModel", back_populates="financing")

    investor_profile = relationship("InvestorProfileModel", back_populates='financing_sources')

    def __init__(self):
        pass

    # def get_total_available(self) -> float:
    #     return sum(mortgage.appraisal_value for mortgage in self.mortgages)

    def __repr__(self):
        return f"<Financing(id={self.id}, total_available=${self.get_total_available():,.2f})>"



class MortgageModel(Base):
    __tablename__ = 'mortgage'

    id = Column(String(255), primary_key=True)
    financing_id = Column(String(255), ForeignKey('financing.id'))
    appraisal_value = Column(Float)
    principal = Column(Float)
    pre_qualified = Column(Boolean)
    pre_approved = Column(Boolean)
    loan_to_value = Column(Float)
    term = Column(Integer)
    amortization_period = Column(Integer)
    monthly_payment = Column(Float)
    owner_occupied = Column(Boolean)
    insurance = Column(Float)

    financing = relationship("FinancingModel", back_populates="mortgages")

    def __init__(
        self,
        id: int,
        appraisal_value: float,
        principal: float,
        pre_qualified: bool,
        pre_approved: bool,
        loan_to_value: float,
        term: int,
        amortization_period: int,
        monthly_payment: float,
        owner_occupied: bool,
        insurance: float
    ):
        self.id = id
        self.appraisal_value = appraisal_value
        self.principal = principal
        self.pre_qualified = pre_qualified
        self.pre_approved = pre_approved
        self.loan_to_value = loan_to_value
        self.term = term
        self.amortization = amortization_period
        self.monthly_payment = monthly_payment
        self.owner_occupied = owner_occupied
        self.insurance = insurance

    def __repr__(self):
        return f"<Mortgage(id={self.id}, principal=${self.principal:,.2f}, term={self.term}mo)>"