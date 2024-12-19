import logging
from typing import List

from sqlalchemy.orm import Session

from app.database.models import SubscriptionModel, ListingModel, ProjectionModel, UnderwritingModel, DealModel
from app.repositories.BaseRepository import BaseRepository
from app.schemas.ProjectionSchema import ProjectionSchema
from app.schemas.ListingSchema import ListingSchema

logger = logging.getLogger(__name__)


class ProjectionService:
    def __init__(self, db: Session):
        self.logger = logger
        self.db = db
        self.repository = BaseRepository[ProjectionModel](self.db, ProjectionModel)

    def save_projection(self, projection_data: ProjectionSchema) -> ProjectionSchema:

        try:
            projection_model = BaseRepository.pydantic_to_sqlalchemy(projection_data, ProjectionModel)

            # if we don't do this, saving projection will try to recreate the already saved deal
            if projection_model.deal:
                existing_id = projection_model.deal.id
                existing_deal = self.db.query(DealModel).filter_by(id=existing_id).first()
                projection_model.deal = existing_deal

            new_projection_model = self.repository.add(projection_model)

            self.db.flush()  # to make sure the newly created ID is passed back

            new_projection_schema = BaseRepository.sqlalchemy_to_pydantic(new_projection_model, ProjectionSchema)

            self.db.commit()

            return new_projection_schema  # Convert to response schema
        except Exception as e:
            self.logger.error(f'Error saving {projection_data}:: {str(e)}')
            raise

    def get_all(self) -> List[ProjectionSchema]:
        projection_model_list = self.repository.get_all()

        projection_schema_list = \
            [BaseRepository.sqlalchemy_to_pydantic(x, ProjectionSchema) for x in projection_model_list]
        return projection_schema_list

    def get_by_id(self, id: int) -> ProjectionSchema:
        projection_model = self.repository.get_by_id(id)
        projection_schema = BaseRepository.sqlalchemy_to_pydantic(projection_model, ProjectionSchema)
        return projection_schema

    def get_projections_by_deal_id(self, deal_id: int) -> List[ProjectionSchema]:
        projection_model_list = (self.db.query(ProjectionModel)
                                 .join(DealModel)
                                 .filter(DealModel.id == deal_id)
                                 .all())

        projection_schema_list = \
            [BaseRepository.sqlalchemy_to_pydantic(x, ProjectionSchema) for x in projection_model_list]
        return projection_schema_list

