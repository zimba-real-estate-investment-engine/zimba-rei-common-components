from datetime import datetime

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
        # self.property_id = property_id
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

