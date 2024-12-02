import logging
from typing import List

from sqlalchemy.orm import Session

from app.database.models import SubscriptionModel, ListingModel, ExpenseModel
from app.repositories.BaseRepository import BaseRepository
from app.schemas.ExpenseSchema import ExpenseSchema
from app.schemas.ListingSchema import ListingSchema

logger = logging.getLogger(__name__)


class ExpenseService:
    def __init__(self, db: Session):
        self.logger = logger
        self.db = db
        self.repository = BaseRepository[ExpenseModel](self.db, ExpenseModel)

    def save_expense(self, expense_data: ExpenseSchema) -> ExpenseSchema:

        try:
            expense_model = BaseRepository.pydantic_to_sqlalchemy(expense_data, ExpenseModel)

            new_expense_model = self.repository.add(expense_model)
            self.db.flush()   # Makes sure the id is auto-incremented

            new_expense_schema = BaseRepository.sqlalchemy_to_pydantic(new_expense_model, ExpenseSchema)

            self.db.commit()

            return new_expense_schema  # Convert to response schema
        except Exception as e:
            self.logger.error(f'Error saving {expense_data}:: {str(e)}')
            raise

    def get_all(self) -> List[ExpenseSchema]:
        expense_model_list = self.repository.get_all()

        expense_schema_list = \
            [BaseRepository.sqlalchemy_to_pydantic(x, ExpenseSchema) for x in expense_model_list]
        return expense_schema_list
