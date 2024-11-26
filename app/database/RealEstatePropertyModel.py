from sqlalchemy import Boolean, Column, String, TIMESTAMP, text, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.database.AddressModel import AddressModel

Base = declarative_base()


class RealEstatePropertyModel(Base):
    __tablename__ = 'real_estate_property'

    id = Column(Integer, primary_key=True, nullable=False)
    address_id = Column(Integer, ForeignKey(f'{__tablename__}.address.id'))

    address = relationship("AddressModel")
    # listings = relationship("Listing", back_populates="realEstateProperty")
    # expenses = relationship("Expense", back_populates="realEstateProperty")

    def __init__(self):
        pass

    def __repr__(self):
        return f"<RealEstateProperty(id={self.id})>"
