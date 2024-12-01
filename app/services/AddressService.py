import logging
from typing import List

from sqlalchemy.orm import Session

from app.database.models import SubscriptionModel, ListingModel, AddressModel
from app.repositories.BaseRepository import BaseRepository
from app.schemas.AddressSchema import AddressSchema
from app.schemas.ListingSchema import ListingSchema

logger = logging.getLogger(__name__)


class AddressService:
    def __init__(self, db: Session):
        self.logger = logger
        self.db = db
        self.repository = BaseRepository[AddressModel](self.db, AddressModel)

    def save_address(self, address_data: AddressSchema) -> AddressSchema:

        try:
            address_model = BaseRepository.pydantic_to_sqlalchemy(address_data, AddressModel)

            new_address_model = self.repository.add(address_model)
            self.db.flush()   # to make sure the newly created ID is passed back

            new_address_schema = BaseRepository.sqlalchemy_to_pydantic(new_address_model, AddressSchema)

            self.db.commit()

            return new_address_schema  # Convert to response schema
        except Exception as e:
            self.logger.error(f'Error saving {address_data}:: {str(e)}')
            raise

    def get_all(self) -> List[AddressSchema]:
        address_model_list = self.repository.get_all()

        address_schema_list = \
            [BaseRepository.sqlalchemy_to_pydantic(x, AddressSchema) for x in address_model_list]
        return address_schema_list
