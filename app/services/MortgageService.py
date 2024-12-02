import logging
from typing import List

from sqlalchemy.orm import Session

from app.database.models import SubscriptionModel, ListingModel, MortgageModel
from app.repositories.BaseRepository import BaseRepository
from app.schemas.MortgageSchema import MortgageSchema

logger = logging.getLogger(__name__)


class MortgageService:
    def __init__(self, db: Session):
        self.logger = logger
        self.db = db
        self.repository = BaseRepository[MortgageModel](self.db, MortgageModel)

    def save_mortgage(self, mortgage_data: MortgageSchema) -> MortgageSchema:

        try:
            mortgage_model = BaseRepository.pydantic_to_sqlalchemy(mortgage_data, MortgageModel)

            new_mortgage_model = self.repository.add(mortgage_model)
            self.db.flush()   # Makes sure the id is auto-incremented

            new_mortgage_schema = BaseRepository.sqlalchemy_to_pydantic(new_mortgage_model, MortgageSchema)

            self.db.commit()

            return new_mortgage_schema  # Convert to response schema
        except Exception as e:
            self.logger.error(f'Error saving {mortgage_data}:: {str(e)}')
            raise

    def get_all(self) -> List[MortgageSchema]:
        mortgage_model_list = self.repository.get_all()

        mortgage_schema_list = \
            [BaseRepository.sqlalchemy_to_pydantic(x, MortgageSchema) for x in mortgage_model_list]
        return mortgage_schema_list
