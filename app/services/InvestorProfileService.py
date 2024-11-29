import logging
from typing import List

from sqlalchemy.orm import Session

from app.database.models import InvestorProfileModel
from app.repositories.BaseRepository import BaseRepository
from app.schemas.InvestorProfileSchema import InvestorProfileSchema

logger = logging.getLogger(__name__)


class InvestorProfileService:
    def __init__(self, db: Session):
        self.logger = logger
        self.db = db
        self.repository = BaseRepository[InvestorProfileModel](self.db, InvestorProfileModel)

    def save_investor_profile(self, investor_profile_data: InvestorProfileSchema) -> InvestorProfileSchema:

        try:
            listing_model = BaseRepository.pydantic_to_sqlalchemy(investor_profile_data, InvestorProfileModel)

            new_listing_model = self.repository.add(listing_model)
            new_listing_schema = BaseRepository.sqlalchemy_to_pydantic(new_listing_model, InvestorProfileSchema)

            self.db.commit()

            return new_listing_schema  # Convert to response schema
        except Exception as e:
            self.logger.error(f'Error saving {investor_profile_data}:: {str(e)}')
            raise

    def get_all(self) -> List[InvestorProfileSchema]:
        investor_profile_model_list = self.repository.get_all()

        listing_schema_list = \
            [BaseRepository.sqlalchemy_to_pydantic(x, InvestorProfileSchema) for x in investor_profile_model_list]
        return listing_schema_list
