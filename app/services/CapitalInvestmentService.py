import logging
from typing import List

from sqlalchemy.orm import Session

from app.database.models import SubscriptionModel, ListingModel, CapitalInvestmentModel
from app.repositories.BaseRepository import BaseRepository
from app.schemas.CapitalInvestmentSchema import CapitalInvestmentSchema

logger = logging.getLogger(__name__)


class CapitalInvestmentService:
    def __init__(self, db: Session):
        self.logger = logger
        self.db = db
        self.repository = BaseRepository[CapitalInvestmentModel](self.db, CapitalInvestmentModel)

    def save_capital_investment(self, capital_investment_data: CapitalInvestmentSchema) -> CapitalInvestmentSchema:

        try:
            capital_investment_model = BaseRepository.pydantic_to_sqlalchemy(capital_investment_data, CapitalInvestmentModel)

            new_capital_investment_model = self.repository.add(capital_investment_model)
            self.db.flush()   # Makes sure the id is auto-incremented

            new_capital_investment_schema = BaseRepository.sqlalchemy_to_pydantic(new_capital_investment_model,
                                                                                  CapitalInvestmentSchema)

            self.db.commit()

            return new_capital_investment_schema  # Convert to response schema
        except Exception as e:
            self.logger.error(f'Error saving {capital_investment_data}:: {str(e)}')
            raise

    def get_all(self) -> List[CapitalInvestmentSchema]:
        capital_investment_model_list = self.repository.get_all()

        capital_investment_schema_list = \
            [BaseRepository.sqlalchemy_to_pydantic(x, CapitalInvestmentSchema) for x in capital_investment_model_list]
        return capital_investment_schema_list
