import json

from app.domain.underwriting.AmortizationSchedule import AmortizationSchedule


def test_generate_amortization_json():
    principal = 500000.00
    annual_interest_rate = 5.75
    amortization_period = 30
    amortization_schedule = AmortizationSchedule.generate_amortization_json(principal, annual_interest_rate,
                                                                            amortization_period)

    assert amortization_schedule

    json_string = json.loads(amortization_schedule)
    first_row = json_string[0]
    principal_recapture = round(first_row['principal_recapture'], 2)
    monthly_payment = round(first_row['monthly_payment'], 2)
    interest_payment = round(first_row['interest_payment'], 2)

    assert principal_recapture == round((monthly_payment - interest_payment), 2)