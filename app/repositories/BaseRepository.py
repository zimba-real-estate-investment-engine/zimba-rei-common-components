from contextlib import contextmanager
from typing import TypeVar, Generic, Type, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, delete, inspect
from pydantic import BaseModel

# Generic type for SQLAlchemy database
T = TypeVar('T')


class BaseRepository(Generic[T]):
    """
    A generic repository interface for SQLAlchemy database.
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


    def sqlalchemy_to_pydantic(self, sqlalchemy_obj, pydantic_model: type[BaseModel]):
        """
            Converts a SQLAlchemy object to a Pydantic object.
            #TODO consider using vars()
                sqlalchemy_obj = User(id=1, name='John Doe', email='john.doe@example.com')

                # Convert the SQLAlchemy object to a dictionary
                obj_dict = vars(sqlalchemy_obj)
                # obj_dict = {k: v for k, v in vars(sqlalchemy_obj).items() if not k.startswith('_sa_')} avoid SqlAlchemy internal

                # Instantiate the Pydantic model using the dictionary
                pydantic_obj = UserModel(**obj_dict)

        Args:
            sqlalchemy_obj (SQLAlchemy object): The SQLAlchemy object to be converted.
            pydantic_model (type[BaseModel]): The Pydantic model class to use.

        Returns:
            pydantic_model: The Pydantic object representing the SQLAlchemy object.
        """
        # Get the column names and values from the SQLAlchemy object
        inspector = inspect(sqlalchemy_obj)
        data = {c.key: getattr(sqlalchemy_obj, c.key) for c in inspector.mapper.column_attrs}

        # Create an instance of the Pydantic model class and return it
        return pydantic_model(**data)


# @contextmanager
# def unit_of_work(session_factory):
#     """Context manager for handling database transactions."""
#     session = session_factory()
#     try:
#         yield session
#         session.commit()
#     except Exception:
#         session.rollback()
#         raise
#     finally:
#         session.close()

