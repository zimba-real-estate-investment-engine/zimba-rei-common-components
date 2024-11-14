from app.domain.Deal import Deal


def test_create_deal(get_test_deal_schema, get_current_time_in_seconds_string):
    deal_data = get_test_deal_schema

    deal = Deal(deal_data)

    #TODO more validation to be added
    assert deal.deal_date == deal_data.deal_date
    assert deal.closing_date
