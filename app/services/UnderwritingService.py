import logging
from typing import List

from sqlalchemy.orm import Session

from app.database.models import UnderwritingModel, InvestorProfileModel, RealEstatePropertyModel
from app.repositories.BaseRepository import BaseRepository
from app.schemas.UnderwritingSchema import UnderwritingSchema

logger = logging.getLogger(__name__)


class UnderwritingService:
    def __init__(self, db: Session):
        self.logger = logger
        self.db = db
        self.repository = BaseRepository[UnderwritingModel](self.db, UnderwritingModel)

    def save_underwriting(self, underwriting_data: UnderwritingSchema) -> UnderwritingSchema:

        try:
            underwriting_model = BaseRepository.pydantic_to_sqlalchemy(underwriting_data, UnderwritingModel)

            # if we don't do this, saving underwriting will try to recreate the already saved investor profile
            if underwriting_model.investor_profile:
                existing_id = underwriting_model.investor_profile.id
                existing_investor_profile = self.db.query(InvestorProfileModel).filter_by(id=existing_id).first()
                underwriting_model.investor_profile = existing_investor_profile

            # if we don't do this, saving underwriting will try to recreate the already saved real estate property
            if underwriting_model.real_estate_property:
                existing_id = underwriting_model.real_estate_property.id
                existing_real_estate_property = self.db.query(RealEstatePropertyModel).filter_by(id=existing_id).first()
                underwriting_model.real_estate_property = existing_real_estate_property

            new_underwriting_model = self.repository.add(underwriting_model)
            self.db.flush()   # Makes sure the id is auto-incremented

            underwriting_schema = BaseRepository.sqlalchemy_to_pydantic(new_underwriting_model, UnderwritingSchema)

            self.db.commit()

            return underwriting_schema  # Convert to response schema
        except Exception as e:
            self.logger.error(f'Error saving {underwriting_data}:: {str(e)}')
            raise

    def get_all(self) -> List[UnderwritingSchema]:
        underwriting_model_list = self.repository.get_all()

        underwriting_schema_list = \
            [BaseRepository.sqlalchemy_to_pydantic(x, UnderwritingSchema) for x in underwriting_model_list]
        return underwriting_schema_list


