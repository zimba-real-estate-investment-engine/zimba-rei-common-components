from datetime import datetime

from dateutil.relativedelta import relativedelta

from rei_models.rei_models.Deal import Deal
from tests.conftest import get_current_time_in_seconds_string


def test_create_deal(get_current_time_in_seconds_string):
    current_time_string = get_current_time_in_seconds_string
    deal_date = datetime.now()
    closing_date = datetime.now() + relativedelta(months=3)

    deal = Deal(
        id=current_time_string, listing_id=current_time_string, investor_id=current_time_string,
        deal_date=deal_date , deal_status="open", offer_price=300000, sale_price=350000,
        closing_date=closing_date, thumbnail="www.example.com/replace_with_real_link.png"
    )

    #TODO more validation to be added
    assert deal.deal_date