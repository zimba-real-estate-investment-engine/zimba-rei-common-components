from datetime import datetime

from dateutil.relativedelta import relativedelta

from rei_models.rei_models.Underwriting import Underwriting
from tests.conftest import get_current_time_in_seconds_string


def test_create_underwriting(get_current_time_in_seconds_string):
    current_time_string = get_current_time_in_seconds_string
    underwriting_date = datetime.now() + relativedelta(months=2)

    underwriting = Underwriting(
        underwriting_id=current_time_string, appraisal_value=320000, loan_amount=240000,
        loan_to_value=0.8, interest_rate=5, underwriting_date=underwriting_date,
        approval_status="approved", risk_assessment="low",
    )

    #TODO more validation to be added
    assert underwriting.loan_amount