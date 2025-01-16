import logging
from typing import List

from sqlalchemy.orm import Session

from app.database.models import DropdownOptionModel
from app.repositories.BaseRepository import BaseRepository
from app.schemas.DropdownOptionSchema import DropdownOptionSchema

logger = logging.getLogger(__name__)


class DropdownOptionService:
    def __init__(self, db: Session):
        self.logger = logger
        self.db = db
        self.repository = BaseRepository[DropdownOptionModel](self.db, DropdownOptionModel)

    # def save_address(self, address_data: DropdownSchema) -> DropdownSchema:
    #
    #     try:
    #         address_model = BaseRepository.pydantic_to_sqlalchemy(address_data, DropdownModel)
    #
    #         new_address_model = self.repository.add(address_model)
    #         self.db.flush()   # to make sure the newly created ID is passed back
    #
    #         new_address_schema = BaseRepository.sqlalchemy_to_pydantic(new_address_model, DropdownSchema)
    #
    #         self.db.commit()
    #
    #         return new_address_schema  # Convert to response schema
    #     except Exception as e:
    #         self.logger.error(f'Error saving {address_data}:: {str(e)}')
    #         raise

    def get_all(self) -> List[DropdownOptionSchema]:
        address_model_list = self.repository.get_all()

        address_schema_list = \
            [BaseRepository.sqlalchemy_to_pydantic(x, DropdownOptionSchema) for x in address_model_list]
        return address_schema_list

    def get_by_dropdown_name(self, dropdown_name) -> List[DropdownOptionSchema]:
        dropdown_options_model_list = self.repository.dynamic_query_builder(
            filters=[DropdownOptionModel.dropdown_name == dropdown_name]
        ).all()

        dropdown_option_schema_list = \
            [BaseRepository.sqlalchemy_to_pydantic(x, DropdownOptionSchema) for x in dropdown_options_model_list]
        return dropdown_option_schema_list
