import json

import pytest
from pydantic import BaseModel


@pytest.skip
def test_is_address_schema_serializable(get_test_address_schema):
    try:
        test_json = {'id': None, 'street_address': '1734210221_street_address',
                     'street_address_two': '1734210221_street_address_two',
                     'country': 'country', 'long_lat_location': '1734210221_long_lat_location',
                     'state': 'ON', 'full_address': '1734210221_full_address'
                     }
        # json_dump = json.dumps(test_json)
        json_dump = json.dumps(get_test_address_schema)
        # to_dict = get_test_address_schema.dict()
        # assert to_dict
        assert json_dump
    except Exception as e:
        assert False
