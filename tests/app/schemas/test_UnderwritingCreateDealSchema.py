import pytest
from pydantic import ValidationError

from app.schemas.UnderwritingSchema import UnderwritingCreateDealSchema


def test_at_least_url_json_is_passed():
    try:
        obj = UnderwritingCreateDealSchema(investor_profile_id=1, real_estate_property_id=2,
                                           listing_url="https://example.com")
    except ValidationError as e:
        pass


def test_neither_passed():
    with pytest.raises(ValidationError):
        obj = UnderwritingCreateDealSchema(investor_profile_id=1, real_estate_property_id=2)


