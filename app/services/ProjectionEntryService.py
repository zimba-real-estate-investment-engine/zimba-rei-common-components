import logging
from typing import List

from sqlalchemy.orm import Session

from app.database.models import SubscriptionModel, ListingModel, ProjectionEntryModel, UnderwritingModel
from app.repositories.BaseRepository import BaseRepository
from app.schemas.DealSchema import DealSchema
from app.schemas.ListingSchema import ListingSchema
from app.schemas.ProjectionEntrySchema import ProjectionEntrySchema

logger = logging.getLogger(__name__)


class ProjectionEntryService:
    def __init__(self, db: Session):
        self.logger = logger
        self.db = db
        self.repository = BaseRepository[ProjectionEntryModel](self.db, ProjectionEntryModel)

    def save_projection_entry(self, projection_entry_data: ProjectionEntrySchema) -> ProjectionEntrySchema:

        try:
            projection_entry_model = BaseRepository.pydantic_to_sqlalchemy(projection_entry_data, ProjectionEntryModel)

            # if we don't do this, saving underwriting will try to recreate the already saved real estate property
            if projection_entry_model.underwriting:
                existing_id = projection_entry_model.underwriting.id
                existing_underwriting = self.db.query(UnderwritingModel).filter_by(id=existing_id).first()
                projection_entry_model.underwriting = existing_underwriting

            new_projection_entry_model = self.repository.add(projection_entry_model)

            self.db.flush()   # to make sure the newly created ID is passed back

            new_projection_entry_schema = BaseRepository.sqlalchemy_to_pydantic(new_projection_entry_model,
                                                                                ProjectionEntrySchema)

            self.db.commit()

            return new_projection_entry_schema  # Convert to response schema
        except Exception as e:
            self.logger.error(f'Error saving {projection_entry_data}:: {str(e)}')
            raise

    def get_all(self) -> List[ProjectionEntrySchema]:
        projection_entry_model_list = self.repository.get_all()

        projection_entry_schema_list = \
            [BaseRepository.sqlalchemy_to_pydantic(x, ProjectionEntrySchema) for x in projection_entry_model_list]
        return projection_entry_schema_list

    def get_by_id(self, id: int) -> ProjectionEntrySchema:
        projection_entry_model = self.repository.get_by_id(id)
        projection_entry_schema = BaseRepository.sqlalchemy_to_pydantic(projection_entry_model, ProjectionEntrySchema)
        return projection_entry_schema
