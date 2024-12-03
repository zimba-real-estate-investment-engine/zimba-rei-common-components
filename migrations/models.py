
from sqlalchemy import Boolean, Column, String, TIMESTAMP, Float, Integer, ForeignKey, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional, List
from datetime import datetime


Base = declarative_base()

class Subscription(Base):
    __tablename__ = 'subscription'
    __table_args__ = {'schema': 'zimba-rei-micro'}

    id = Column(String(255), primary_key=True, nullable=False)
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


class Deal(Base):
    __tablename__ = 'deal'
    __table_args__ = {'schema': 'zimba-rei-micro'}

    id = Column(String(255), primary_key=True)
    down_payment = Column(Float)
    term = Column(Integer)
    interest_rate = Column(Float)
    monthly_cost = Column(Float)
    after_repair_value = Column(Float)
    time_horizon = Column(Integer)
    roi = Column(Float)
    capital_invested = Column(Float)
    property_value = Column(Float)

    def __init__(
        self,
        id: str,
        down_payment: float,
        term: int,
        interest_rate: float,
        monthly_cost: float,
        after_repair_value: float,
        time_horizon: int,
        roi: float,
        capital_invested: float,
        property_value: float
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
        self.property_value = property_value

    def __repr__(self):
        return f"<Deal(id={self.id}, property_value=${self.property_value:,.2f}, roi={self.roi}%)>"

class UnderwritingProcess(Base):
    __tablename__ = 'underwriting_process'
    __table_args__ = {'schema': 'zimba-rei-micro'}

    id = Column(String(255), primary_key=True)
    investor_profile_id = Column(String(255), ForeignKey(f'{__table_args__["schema"]}.investor_profile.id'))
    property_id = Column(String(255), ForeignKey(f'{__table_args__["schema"]}.property.id'))
    
    investor_profile = relationship("InvestorProfile")
    property = relationship("Property")

    def __init__(self, id: str, investor_profile_id: str, property_id: str):
        self.id = id
        self.investor_profile_id = investor_profile_id
        self.property_id = property_id

    def __repr__(self):
        return f"<UnderwritingProcess(id={self.id})>"

class InvestorProfile(Base):
    __tablename__ = 'investor_profile'
    __table_args__ = {'schema': 'zimba-rei-micro'}

    id = Column(String(255), primary_key=True)
    budget_min = Column(Float)
    budget_max = Column(Float)
    preferred_property = Column(String(255))
    bedrooms_min = Column(Integer)
    bedrooms_max = Column(Integer)
    assigned_parking = Column(Boolean)
    air_conditioning_required = Column(Boolean)
    min_roi = Column(Float)

    def __init__(
        self,
        id: str,
        budget_min: float,
        budget_max: float,
        preferred_property: str,
        bedrooms_min: int,
        bedrooms_max: int,
        assigned_parking: bool,
        air_conditioning_required: bool,
        min_roi: float
    ):
        self.id = id
        self.budget_min = budget_min
        self.budget_max = budget_max
        self.preferred_property = preferred_property
        self.bedrooms_min = bedrooms_min
        self.bedrooms_max = bedrooms_max
        self.assigned_parking = assigned_parking
        self.air_conditioning_required = air_conditioning_required
        self.min_roi = min_roi

    def __repr__(self):
        return f"<InvestorProfile(id={self.id}, budget_range=${self.budget_min:,.2f}-${self.budget_max:,.2f})>"

class Property(Base):
    __tablename__ = 'property'
    __table_args__ = {'schema': 'zimba-rei-micro'}

    id = Column(String(255), primary_key=True)
    address_id = Column(String(255), ForeignKey(f'{__table_args__["schema"]}.address.id'))
    
    address = relationship("Address")
    listings = relationship("Listing", back_populates="property")
    expenses = relationship("Expense", back_populates="property")

    def __init__(self, id: str, address_id: str):
        self.id = id
        self.address_id = address_id

    def __repr__(self):
        return f"<Property(id={self.id})>"

class Listing(Base):
    __tablename__ = 'listing'
    __table_args__ = {'schema': 'zimba-rei-micro'}

    id = Column(String(255), primary_key=True)
    property_id = Column(String(255), ForeignKey(f'{__table_args__["schema"]}.property.id'))
    beds = Column(Integer)
    baths = Column(Float)
    air_conditioning = Column(Boolean)
    parking_spaces = Column(Integer)
    balcony = Column(Boolean)
    hardwood_floor = Column(Boolean)
    dishwasher = Column(Boolean)
    year_built = Column(TIMESTAMP)
    basement = Column(Boolean)
    square_feet = Column(Float)

    property = relationship("Property", back_populates="listings")

    def __init__(
        self,
        id: str,
        property_id: str,
        beds: int,
        baths: float,
        air_conditioning: bool,
        parking_spaces: int,
        balcony: bool,
        hardwood_floor: bool,
        dishwasher: bool,
        year_built: datetime,
        basement: bool,
        square_feet: float
    ):
        self.id = id
        self.property_id = property_id
        self.beds = beds
        self.baths = baths
        self.air_conditioning = air_conditioning
        self.parking_spaces = parking_spaces
        self.balcony = balcony
        self.hardwood_floor = hardwood_floor
        self.dishwasher = dishwasher
        self.year_built = year_built
        self.basement = basement
        self.square_feet = square_feet

    def __repr__(self):
        return f"<Listing(id={self.id}, beds={self.beds}, baths={self.baths})>"

class Expense(Base):
    __tablename__ = 'expense'
    __table_args__ = {'schema': 'zimba-rei-micro'}

    id = Column(String(255), primary_key=True)
    property_id = Column(String(255), ForeignKey(f'{__table_args__["schema"]}.property.id'))
    type = Column(String(255))
    monthly_cost = Column(Float)

    property = relationship("Property", back_populates="expenses")

    def __init__(self, id: str, property_id: str, type: str, monthly_cost: float):
        self.id = id
        self.property_id = property_id
        self.type = type
        self.monthly_cost = monthly_cost

    def __repr__(self):
        return f"<Expense(id={self.id}, type={self.type}, monthly_cost=${self.monthly_cost:,.2f})>"

class Address(Base):
    __tablename__ = 'address'
    __table_args__ = {'schema': 'zimba-rei-micro'}

    id = Column(String(255), primary_key=True)
    street_address = Column(String(255))
    city = Column(String(255))
    state = Column(String(255))
    postal_code = Column(String(255))
    country = Column(String(255))
    long_lat_location = Column(String(255))

    def __init__(
        self,
        id: str,
        street_address: str,
        city: str,
        state: str,
        postal_code: str,
        country: str,
        long_lat_location: str
    ):
        self.id = id
        self.street_address = street_address
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.country = country
        self.long_lat_location = long_lat_location

    def __repr__(self):
        return f"<Address(id={self.id}, city={self.city}, state={self.state})>"

class Financing(Base):
    __tablename__ = 'financing'
    __table_args__ = {'schema': 'zimba-rei-micro'}

    id = Column(String(255), primary_key=True)
    mortgages = relationship("Mortgage", back_populates="financing")

    def __init__(self, id: str):
        self.id = id

    def get_total_available(self) -> float:
        return sum(mortgage.appraisal_value for mortgage in self.mortgages)

    def __repr__(self):
        return f"<Financing(id={self.id}, total_available=${self.get_total_available():,.2f})>"

class Mortgage(Base):
    __tablename__ = 'mortgage'
    __table_args__ = {'schema': 'zimba-rei-micro'}

    id = Column(String(255), primary_key=True)
    financing_id = Column(String(255), ForeignKey(f'{__table_args__["schema"]}.financing.id'))
    appraisal_value = Column(Float)
    principal = Column(Float)
    pre_qualified = Column(Boolean)
    pre_approved = Column(Boolean)
    loan_to_value = Column(Float)
    term = Column(Integer)
    amortization = Column(Integer)
    monthly_payment = Column(Float)
    owner_occupied = Column(Boolean)
    insurance = Column(Float)

    financing = relationship("Financing", back_populates="mortgages")

    def __init__(
        self,
        id: str,
        financing_id: str,
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
        self.financing_id = financing_id
        self.appraisal_value = appraisal_value
        self.principal = principal
        self.pre_qualified = pre_qualified
        self.pre_approved = pre_approved
        self.loan_to_value = loan_to_value
        self.term = term
        self.amortization_period = amortization_period
        self.monthly_payment = monthly_payment
        self.owner_occupied = owner_occupied
        self.insurance = insurance

    def __repr__(self):
        return f"<Mortgage(id={self.id}, principal=${self.principal:,.2f}, term={self.term}mo)>"
