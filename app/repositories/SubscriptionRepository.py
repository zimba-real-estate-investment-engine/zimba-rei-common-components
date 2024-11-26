from typing import TypeVar, List, Optional
from .BaseRepository import BaseRepository
from app.database.SubscriptionModel import SubscriptionModel

from sqlalchemy.orm import Session


#
#
class SubscriptionRepository(BaseRepository[SubscriptionModel]):

    def __init__(self, db: Session):
        super().__init__(db, SubscriptionModel)
    #
    # def find_by_email(self, email: str) -> List[SubscriptionModel]:
    #     return self.db.query(self.model) \
    #         .filter(self.model.email == email) \
    #         .all()
    #
    # def find_recent(self, limit: int = 10) -> List[SubscriptionModel]:
    #     return self.db.query(self.model)\
    #         .order_by(self.model.created_date.desc())\
    #         .limit(limit)\
    #         .all()
    #
    # def find_by_unsubscribe_token(self, unsubscribe_token: str) -> List[SubscriptionModel]:
    #     return self.db.query(self.model) \
    #         .filter(self.model.unsubscribe_token == unsubscribe_token) \
    #         .all()