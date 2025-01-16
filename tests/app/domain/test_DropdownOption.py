
from app.domain.DropdownOption import DropdownOption


def test_dropdown_option_init(test_dropdown_option_schema):
    test_dropdown_option = test_dropdown_option_schema

    dropdown_option = DropdownOption(**test_dropdown_option.dict())

    assert dropdown_option.value == test_dropdown_option.value
