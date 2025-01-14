import json


def test_is_amortization_caching_code_model_serializable(test_amortization_schedule_row_model):
    try:
        json_dump = json.dumps(test_amortization_schedule_row_model)
        assert json_dump
    except Exception as e:
        assert False
