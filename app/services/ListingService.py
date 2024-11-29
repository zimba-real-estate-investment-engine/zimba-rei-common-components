import logging
from typing import List

from sqlalchemy.orm import Session

from app.database.models import SubscriptionModel, ListingModel
from app.repositories.BaseRepository import BaseRepository
from app.schemas.ListingSchema import ListingSchema

logger = logging.getLogger(__name__)


class ListingService:
    def __init__(self, db: Session):
        self.logger = logger
        self.db = db
        self.repository = BaseRepository[ListingModel](self.db, ListingModel)

    def save_listing(self, listing_data: ListingSchema) -> ListingSchema:

        try:
            listing_model = BaseRepository.pydantic_to_sqlalchemy(listing_data, ListingModel)

            new_listing_model = self.repository.add(listing_model)
            new_listing_schema = BaseRepository.sqlalchemy_to_pydantic(new_listing_model, ListingSchema)

            self.db.commit()

            return new_listing_schema  # Convert to response schema
        except Exception as e:
            self.logger.error(f'Error saving {listing_data}:: {str(e)}')
            raise

    def get_all(self) -> List[ListingSchema]:
        listing_model_list = self.repository.get_all()

        listing_schema_list = \
            [self.repository.sqlalchemy_to_pydantic(x, ListingSchema) for x in listing_model_list]
        return listing_schema_list
