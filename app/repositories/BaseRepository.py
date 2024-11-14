from typing import TypeVar, Generic, Type, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, delete

# Generic type for SQLAlchemy models
T = TypeVar('T')


class BaseRepository(Generic[T]):
    """
    A generic repository interface for SQLAlchemy models.
    Transaction management is handled outside the repository.
    """

    def __init__(self, session: Session, model_class: Type[T]):
        self.session = session
        self.model_class = model_class

    def add(self, entity: T) -> T:
        """Add a new entity to the database."""
        self.session.add(entity)
        return entity

    def add_many(self, entities: List[T]) -> List[T]:
        """Add multiple entities to the database."""
        self.session.add_all(entities)
        return entities

    def get_by_id(self, id: any) -> Optional[T]:
        """Get an entity by its ID."""
        return self.session.get(self.model_class, id)

    def get_all(self) -> List[T]:
        """Get all entities of this type."""
        return list(self.session.execute(select(self.model_class)).scalars())

    def update(self, entity: T) -> T:
        """Update an existing entity."""
        return self.session.merge(entity)

    def delete(self, id: any) -> bool:
        """Delete an entity by its ID."""
        result = self.session.execute(
            delete(self.model_class).where(self.model_class.id == id)
        )
        return result.rowcount > 0

    def delete_many(self, ids: List[any]) -> bool:
        """Delete multiple entities by their IDs."""
        result = self.session.execute(
            delete(self.model_class).where(self.model_class.id.in_(ids))
        )
        return result.rowcount > 0
