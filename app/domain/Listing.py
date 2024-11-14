from app.schemas import ListingSchema


class Listing:
    """
        Domain entity contains business logic and inherits from pydantic schema
    """

    def __init__(self, data: ListingSchema):
        self._data = data

    # Delegate Pydantic model attributes
    def __getattr__(self, name: str):
        return getattr(self._data, name)