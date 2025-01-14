import json

from app.domain.underwriting.AmortizationSchedule import AmortizationSchedule
from app.domain.underwriting.AmortizationScheduleRow import AmortizationScheduleRow


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


def test_amortization_rows_for_payment_range(test_amortization_json):
    start = 5
    end = 10
    filtered_json_list = AmortizationSchedule.amortization_rows_for_payment_range(test_amortization_json,
                                                                                  start=start, end=end)
    assert len(filtered_json_list) == end - start

    single_result = AmortizationSchedule.amortization_rows_for_payment_range(test_amortization_json, start=10)
    assert len(single_result) == 1
    assert  isinstance(single_result[0], AmortizationScheduleRow)


def test_get_schedule_entry_for_payment_number():

    amortization_schedule = AmortizationSchedule(principal=343434, annual_interest_rate=5.75, amortization_period=30)

    amortization_schedule_row = amortization_schedule.get_schedule_entry_for_payment_number(10)
    assert amortization_schedule_row
    assert isinstance(amortization_schedule_row, AmortizationScheduleRow)
    assert amortization_schedule_row.principal_recapture


def test_get_schedule_entries_for_payment_number_range():

    amortization_schedule = AmortizationSchedule(principal=343434, annual_interest_rate=5.75, amortization_period=30)

    amortization_schedule_rows = amortization_schedule.get_schedule_entries_for_payment_number_range(
        10, 20)

    assert amortization_schedule_rows
    assert len(amortization_schedule_rows) == 10