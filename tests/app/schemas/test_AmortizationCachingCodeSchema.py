import json

import pytest


@pytest.skip  # will need a solution to handle serialization without specifying an encoder
def test_is_amortization_caching_code_schema_serializable(test_amortization_caching_code_schema):
    try:
        json_dump = json.dumps(test_amortization_caching_code_schema)
        assert json_dump
    except Exception as e:
        assert False