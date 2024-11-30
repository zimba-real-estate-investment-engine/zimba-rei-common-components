import logging
from typing import List

from sqlalchemy.orm import Session

from app.database.models import SubscriptionModel, RealEstatePropertyModel
from app.repositories.BaseRepository import BaseRepository
from app.schemas.RealEstatePropertySchema import RealEstatePropertySchema

logger = logging.getLogger(__name__)


class RealEstatePropertyService:
    def __init__(self, db: Session):
        self.logger = logger
        self.db = db
        self.repository = BaseRepository[RealEstatePropertyModel](self.db, RealEstatePropertyModel)

    def save_real_estate_property(self, real_estate_property_data: RealEstatePropertySchema) -> RealEstatePropertySchema:

        try:
            real_estate_property_model = BaseRepository.pydantic_to_sqlalchemy(real_estate_property_data,
                                                                               RealEstatePropertyModel)

            new_real_estate_property_model = self.repository.add(real_estate_property_model)
            new_real_estate_property_schema = BaseRepository.sqlalchemy_to_pydantic(new_real_estate_property_model,
                                                                                    RealEstatePropertySchema)

            self.db.commit()

            return new_real_estate_property_schema  # Convert to response schema
        except Exception as e:
            self.logger.error(f'Error saving {real_estate_property_data}:: {str(e)}')
            raise

    def get_all(self) -> List[RealEstatePropertySchema]:
        real_estate_property_model_list = self.repository.get_all()

        real_estate_property_schema_list = \
            [BaseRepository.sqlalchemy_to_pydantic(x, RealEstatePropertySchema) for x in real_estate_property_model_list]
        return real_estate_property_schema_list
