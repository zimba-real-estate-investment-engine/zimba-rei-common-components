from typing import TypeVar, Generic, Type, List, Optional
from sqlalchemy.orm import Session, Query
from sqlalchemy import select, delete
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()
# Generic type for SQLAlchemy migrations
T = TypeVar('T')

PydanticSchemaType = TypeVar('PydanticSchemaType', bound=BaseModel)
SQLAlchemyModelType = TypeVar('SQLAlchemyModelType', bound=Base)


class BaseRepository(Generic[T]):
    """
    A generic repository interface for SQLAlchemy migrations.
    Transaction management is handled outside the repository.
    """

    def __init__(self, session: Session, model_class: Type[T]):
        self.session = session
        self.model_class = model_class

    def add(self, entity: T) -> T:
        """Add a new entity to the migrations."""
        self.session.add(entity)
        return entity

    def add_many(self, entities: List[T]) -> List[T]:
        """Add multiple entities to the migrations."""
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

    def dynamic_query_builder(self, columns=None, filters=None, order_by=None) :
        """
        Usage example
            results = dynamic_query_builder(User,
                                          columns = [User.id, User.username],
                                          filters = [User.active == True],
                                          order_byUser.username.asc())
                                          ).all()
        :param columns:
        :param filters:
        :param order_by:
        :return:
        """
        query = self.session.query(self.model_class)

        if columns:
            query = query.with_entities(*columns)

        if filters:
            query = query.filter(*filters)

        if order_by:
            query = query.order_by(*order_by)

        return query

    @staticmethod
    def sqlalchemy_to_pydantic(sqlalchemy_obj: SQLAlchemyModelType, pydantic_schema: Type[PydanticSchemaType]) \
            -> PydanticSchemaType:
        # PydanticSchema = sqlalchemy_to_pydantic(PydanticSchemaType)
        pydantic_instance = pydantic_schema.from_orm(sqlalchemy_obj)
        return pydantic_instance

    #     """
    #         Converts a SQLAlchemy object to a Pydantic object.
    #         #TODO consider using vars()
    #             sqlalchemy_obj = User(id=1, name='John Doe', email='john.doe@example.com')
    #
    #             # Convert the SQLAlchemy object to a dictionary
    #             obj_dict = vars(sqlalchemy_obj)
    #             # obj_dict = {k: v for k, v in vars(sqlalchemy_obj).items() if not k.startswith('_sa_')} avoid SqlAlchemy internal
    #
    #             # Instantiate the Pydantic model using the dictionary
    #             pydantic_obj = UserModel(**obj_dict)
    #
    #     Args:
    #         sqlalchemy_obj (SQLAlchemy object): The SQLAlchemy object to be converted.
    #         pydantic_model (type[BaseModel]): The Pydantic model class to use.
    #
    #     Returns:
    #         pydantic_model: The Pydantic object representing the SQLAlchemy object.
    #     """
    #     # Get the column names and values from the SQLAlchemy object
    #     inspector = inspect(sqlalchemy_obj)
    #     data = {c.key: getattr(sqlalchemy_obj, c.key) for c in inspector.mapper.column_attrs}
    #
    #     # Create an instance of the Pydantic model class and return it
    #     return pydantic_model(**data)

    @staticmethod
    def pydantic_to_sqlalchemy(pydantic_obj, sqlalchemy_model):
        """
        Converts a Pydantic object to an SQLAlchemy instance.
        Supports nested models by recursively handling relationships.
        """
        # Ensure the object is a Pydantic model
        if hasattr(pydantic_obj, "dict"):
            obj_data = pydantic_obj.dict()
        elif isinstance(pydantic_obj, dict):
            obj_data = pydantic_obj
        else:
            raise ValueError("Input must be a Pydantic model or a dictionary.")

        relationships = {}

        # Handle nested relationships
        for field, value in obj_data.items():
            if isinstance(value, list) and hasattr(sqlalchemy_model, field):
                # Convert list of nested models
                relationships[field] = [
                    BaseRepository.pydantic_to_sqlalchemy(item, getattr(sqlalchemy_model, field).property.mapper.class_)
                    for item in value
                ]
            elif isinstance(value, dict) and hasattr(sqlalchemy_model, field):
                # Convert single nested model
                relationships[field] = BaseRepository.pydantic_to_sqlalchemy(value,
                                                                             getattr(sqlalchemy_model,
                                                                                     field).property.mapper.class_)

        # Unpack relationships and simple fields
        return sqlalchemy_model(**{**obj_data, **relationships})

# @contextmanager
# def unit_of_work(session_factory):
#     """Context manager for handling migrations transactions."""
#     session = session_factory()
#     try:
#         yield session
#         session.commit()
#     except Exception:
#         session.rollback()
#         raise
#     finally:
#         session.close()
