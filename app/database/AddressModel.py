from sqlalchemy import Boolean, Column, String, TIMESTAMP, text, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


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
