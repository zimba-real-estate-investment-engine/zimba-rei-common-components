from app.domain.Deal import Deal


def test_deal(get_test_deal_schema, get_current_time_in_seconds_string):
    deal_data = get_test_deal_schema

    deal = Deal(**deal_data.dict())

    assert deal.deal_date == deal_data.deal_date