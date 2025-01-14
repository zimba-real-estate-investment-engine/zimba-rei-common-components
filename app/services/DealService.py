import logging
from typing import List

from sqlalchemy.orm import Session

from app.database.models import SubscriptionModel, ListingModel, DealModel, UnderwritingModel, InvestorProfileModel
from app.repositories.BaseRepository import BaseRepository
from app.schemas.DealSchema import DealSchema
from app.schemas.ListingSchema import ListingSchema

logger = logging.getLogger(__name__)


class DealService:
    def __init__(self, db: Session):
        self.logger = logger
        self.db = db
        self.repository = BaseRepository[DealModel](self.db, DealModel)

    def save_deal(self, deal_data: DealSchema) -> DealSchema:

        try:
            deal_model = BaseRepository.pydantic_to_sqlalchemy(deal_data, DealModel)

            # if we don't check, saving deal, saving underwriting will duplicate the already saved investorprofile
            if deal_model.underwriting is not None:
                if deal_model.underwriting.id is not None:
                    existing_id = deal_model.underwriting.id
                    existing_underwriting = self.db.query(UnderwritingModel).filter_by(id=existing_id).first()
                    deal_model.underwriting = existing_underwriting
                # check to avoid duplicating pre-existing investorprofile
                if deal_model.underwriting.investor_profile and deal_model.underwriting.investor_profile.id is not None:
                    existing_investor_profile_id = deal_model.underwriting.investor_profile.id
                    existing_investor_profile = (self.db.query(InvestorProfileModel)
                                                        .filter_by(id=existing_investor_profile_id).first())
                    deal_model.underwriting.investor_profile = existing_investor_profile

            new_deal_model = self.repository.add(deal_model)

            self.db.flush()   # to make sure the newly created ID is passed back

            new_deal_schema = BaseRepository.sqlalchemy_to_pydantic(new_deal_model, DealSchema)

            self.db.commit()

            return new_deal_schema  # Convert to response schema
        except Exception as e:
            self.logger.error(f'Error saving {deal_data}:: {str(e)}')
            raise

    def get_all(self) -> List[DealSchema]:
        deal_model_list = self.repository.get_all()

        deal_schema_list = \
            [BaseRepository.sqlalchemy_to_pydantic(x, DealSchema) for x in deal_model_list]
        return deal_schema_list

    def get_by_id(self, id: int) -> DealSchema:
        deal_model = self.repository.get_by_id(id)
        deal_schema = BaseRepository.sqlalchemy_to_pydantic(deal_model, DealSchema)
        return deal_schema
