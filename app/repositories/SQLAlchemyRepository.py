# from sqlalchemy.orm import Session
# from sqlalchemy.ext.declarative import declarative_base
# from .BaseRepository import Repository
# from typing import List, Optional, Any
#
# Base = declarative_base()
#
#
# class SQLAlchemyRepository(Repository):
#     def __init__(self, session: Session):
#         self.session = session
#
#     def add(self, entity: Any) -> None:
#         self.session.add(entity)
#
#     def get(self, id: Any) -> Optional[Any]:
#         return self.session.query(Any).filter_by(id=id).first()
#
#     def update(self, entity: Any) -> None:
#         self.session.merge(entity)
#
#     def delete(self, id: Any) -> None:
#         entity = self.get(id)
#         if entity:
#             self.session.delete(entity)
#
#     def get_all(self) -> List[Any]:
#         return self.session.query(Any).all()
