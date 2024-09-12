from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

from rei_models.rei_models.Mortgage import Mortgage
from tests.conftest import get_current_time_in_seconds_string


def test_create_mortgage(get_current_time_in_seconds_string):
    current_time_string = get_current_time_in_seconds_string
    issued_date = datetime.now()

    mortgage = Mortgage(
        id=current_time_string, appraisal_value=300000.00, principal=240000.03, issued_date=issued_date,
        pre_qualifid=True, pre_approved=True, loan_to_value=80.0, interest_rate=3.75,
        term=timedelta(days=3*365), amortization_period=timedelta(days=30*365),monthly_payment=3565.25,
        owner_occupied=True, insurance=3500.75,
    )
    #TODO more validation to be added
    assert mortgage.issued_date
    assert mortgage.principal