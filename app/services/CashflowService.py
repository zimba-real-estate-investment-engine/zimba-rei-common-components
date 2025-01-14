import logging
from typing import List

from sqlalchemy.orm import Session

from app.database.models import SubscriptionModel, ListingModel, CashflowModel
from app.repositories.BaseRepository import BaseRepository
from app.schemas.CashflowSchema import CashflowSchema
from app.schemas.ListingSchema import ListingSchema

logger = logging.getLogger(__name__)


class CashflowService:
    def __init__(self, db: Session):
        self.logger = logger
        self.db = db
        self.repository = BaseRepository[CashflowModel](self.db, CashflowModel)

    def save_cashflow(self, cashflow_data: CashflowSchema) -> CashflowSchema:

        try:
            cashflow_model = BaseRepository.pydantic_to_sqlalchemy(cashflow_data, CashflowModel)

            new_cashflow_model = self.repository.add(cashflow_model)
            self.db.flush()   # Makes sure the id is auto-incremented

            new_cashflow_schema = BaseRepository.sqlalchemy_to_pydantic(new_cashflow_model, CashflowSchema)

            self.db.commit()

            return new_cashflow_schema  # Convert to response schema
        except Exception as e:
            self.logger.error(f'Error saving {cashflow_data}:: {str(e)}')
            raise

    def get_all(self) -> List[CashflowSchema]:
        cashflow_model_list = self.repository.get_all()

        cashflow_schema_list = \
            [BaseRepository.sqlalchemy_to_pydantic(x, CashflowSchema) for x in cashflow_model_list]
        return cashflow_schema_list
