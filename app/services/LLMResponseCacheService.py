import logging
from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.database.models import LLMResponseModel
from app.repositories.BaseRepository import BaseRepository
from app.schemas.LLMResponseSchema import LLMResponseSchema

logger = logging.getLogger(__name__)


class LLMResponseCacheService:
    def __init__(self, db: Session):
        self.logger = logger
        self.db = db
        self.repository = BaseRepository[LLMResponseModel](self.db, LLMResponseModel)

    def save_llm_response(self, llm_response_data: LLMResponseSchema) -> LLMResponseSchema:

        try:
            llm_response_model: LLMResponseModel = BaseRepository.pydantic_to_sqlalchemy(llm_response_data,
                                                                                         LLMResponseModel)

            if llm_response_model.listing_url is None or llm_response_model.llm_service_api_url is None:
                raise ValueError(f'listing_url: {llm_response_model.listing_url} and '
                                 f'llm_service_api_url: {llm_response_model.llm_service_api_url} cannot be null')

            else:  # If already saved don't attempt to create another one
                results = self.find_by_listing_url_and_llm_service_api_url(llm_response_model.listing_url,
                                                                           llm_response_model.llm_service_api_url)

                if len(results) > 0 and results[0]:
                    single_result = results[0]
                    pre_existing_llm_response = BaseRepository.sqlalchemy_to_pydantic(single_result,
                                                                                      LLMResponseSchema)
                    return pre_existing_llm_response
                else:
                    new_llm_response_model = self.repository.add(llm_response_model)
                    self.db.flush()  # Makes sure the id is auto-incremented

                    new_llm_response_schema = BaseRepository.sqlalchemy_to_pydantic(new_llm_response_model,
                                                                                    LLMResponseSchema)
                    self.db.commit()
                    return new_llm_response_schema  # Convert to response schema
        except Exception as e:
            self.logger.error(f'Error saving {llm_response_data}:: {str(e)}')
            raise

    def get_all(self) -> List[LLMResponseSchema]:
        llm_response_model_list = self.repository.get_all()

        llm_response_schema_list = \
            [BaseRepository.sqlalchemy_to_pydantic(x, LLMResponseSchema) for x in llm_response_model_list]
        return llm_response_schema_list

    def find_by_listing_url_and_llm_service_api_url(self, listing_url: str,
                                                    llm_service_api_url) -> List[LLMResponseSchema]:

        session = self.db
        llm_response_model_list = session.query(LLMResponseModel).filter(and_(
            LLMResponseModel.listing_url == listing_url,
            LLMResponseModel.llm_service_api_url == llm_service_api_url
        )).all()

        llm_response_schema_list = \
            [BaseRepository.sqlalchemy_to_pydantic(x, LLMResponseSchema) for x in llm_response_model_list]
        return llm_response_schema_list
