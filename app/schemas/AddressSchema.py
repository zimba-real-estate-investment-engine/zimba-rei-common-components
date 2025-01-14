import json
from typing import Optional

from pydantic import BaseModel

class GlobalPydanticEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BaseModel):
            return obj.model_dump()
        return super().default(obj)

# Set this as the default encoder globally
json.JSONEncoder = GlobalPydanticEncoder


class AddressSchema(BaseModel):
    id: Optional[int] = None
    street_address:  Optional[str] = ''
    street_address_two: Optional[str] = ''
    city:   Optional[str] = ''
    postal_code:  Optional[str] = ''
    country:   Optional[str] = ''
    long_lat_location:  Optional[str] = ''
    state:   Optional[str] = ''
    full_address: str
    #TODO more to be added from data dictionary as necessary


    def __repr__(self):
        return str(self.model_dump())

    class Config:
        orm_mode = True
        from_attributes = True

    def default(self):
        return json.dumps(self.dict())


    def __str__(self):
        return json.dumps(self.dict())

class AddressStrictSchema(BaseModel):
    id: Optional[int] = None
    street_address: str
    street_address_two: Optional[str] = ''
    city: str
    postal_code: str
    country: str
    long_lat_location:  Optional[str] = None
    full_address:  Optional[str] = None
    state: str
    #TODO more to be added from data dictionary as necessary

    class Config:
        orm_mode = True
        from_attributes = True