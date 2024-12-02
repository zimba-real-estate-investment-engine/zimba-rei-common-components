import logging
from typing import List

from sqlalchemy.orm import Session

from app.database.models import SubscriptionModel, ListingModel, FinancingModel
from app.repositories.BaseRepository import BaseRepository
from app.schemas.FinancingSchema import FinancingSchema

logger = logging.getLogger(__name__)


class FinancingService:
    def __init__(self, db: Session):
        self.logger = logger
        self.db = db
        self.repository = BaseRepository[FinancingModel](self.db, FinancingModel)

    def save_financing(self, financing_data: FinancingSchema) -> FinancingSchema:

        try:
            financing_model = BaseRepository.pydantic_to_sqlalchemy(financing_data, FinancingModel)

            new_financing_model = self.repository.add(financing_model)
            self.db.flush()   # Makes sure the id is auto-incremented

            new_financing_schema = BaseRepository.sqlalchemy_to_pydantic(new_financing_model, FinancingSchema)

            self.db.commit()

            return new_financing_schema  # Convert to response schema
        except Exception as e:
            self.logger.error(f'Error saving {financing_data}:: {str(e)}')
            raise

    def get_all(self) -> List[FinancingSchema]:
        financing_model_list = self.repository.get_all()

        financing_schema_list = \
            [BaseRepository.sqlalchemy_to_pydantic(x, FinancingSchema) for x in financing_model_list]
        return financing_schema_list
