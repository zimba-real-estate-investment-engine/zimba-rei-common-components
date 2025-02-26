import json
import logging
from typing import Optional, List, Any

import pandas as pd
import numpy_financial as npf
from pandas import DataFrame

from app.domain.underwriting.AmortizationCachingCode import AmortizationCachingCode
from app.domain.underwriting.AmortizationScheduleRow import AmortizationScheduleRow
from app.schemas.AmortizationScheduleSchema import AmortizationScheduleSchema

logger = logging.getLogger(__name__)


class AmortizationSchedule(AmortizationScheduleSchema):

    def get_schedule_entry_for_payment_number(self, payment_number: int = 0) -> AmortizationScheduleRow:

        self.amortization_schedule_json = AmortizationSchedule.generate_amortization_json(self.principal,
                                                                                          self.annual_interest_rate,
                                                                                          self.amortization_period)
        amortization_schedule_rows = AmortizationSchedule.amortization_rows_for_payment_range(
            self.amortization_schedule_json, start=payment_number)

        if amortization_schedule_rows[0]:
            return amortization_schedule_rows[0]

    def get_schedule_entries_for_payment_number_range(self, range_start: int = 0, range_end: int = 0) \
            -> List[AmortizationScheduleRow]:

        self.amortization_schedule_json = AmortizationSchedule.generate_amortization_json(self.principal,
                                                                                          self.annual_interest_rate,
                                                                                          self.amortization_period)
        amortization_schedule_rows = AmortizationSchedule.amortization_rows_for_payment_range(
            self.amortization_schedule_json, start=range_start, end=range_end)

        return amortization_schedule_rows

    def get_basic_dataframe(self) -> DataFrame:
        self.amortization_schedule_json = AmortizationSchedule.generate_amortization_json(self.principal,
                                                                                          self.annual_interest_rate,
                                                                                          self.amortization_period)
        parsed_json = json.loads(self.amortization_schedule_json)
        dataframe: DataFrame = pd.DataFrame(parsed_json)

        return dataframe

    @staticmethod
    def get_monthly_payment(principal: float, annual_interest_rate: float, amortization_period: int) -> float:
        n_periods = amortization_period * 12
        monthly_rate = annual_interest_rate / 100 / 12
        npf_payment = npf.pmt(monthly_rate, n_periods, -principal)
        monthly_payment = round(float(npf_payment), 2)
        return monthly_payment

    @staticmethod
    def generate_amortization_json(principal: float, annual_interest_rate: float,
                                   amortization_period: int) -> str:
        # Loan details
        principal = principal
        annual_interest_rate = annual_interest_rate
        amortization_period = amortization_period

        # Get payment periods and compounding payments
        n_periods = amortization_period * 12
        monthly_rate = annual_interest_rate / 100 / 12
        npf_payment = npf.pmt(monthly_rate, n_periods, -principal)
        monthly_payment = round(float(npf_payment), 2)

        # Create a caching code that will be used track amortizations that have already been calculated
        amortization_caching_code: AmortizationCachingCode = (
            AmortizationCachingCode(principal=principal, annual_interest_rate=annual_interest_rate,
                                    amortization_period=amortization_period))
        caching_code = amortization_caching_code.model_dump()

        # Create an amortization schedule
        schedule = []
        remaining_balance = principal

        for i in range(1, n_periods + 1):
            interest_payment = round(remaining_balance * monthly_rate, 2)
            principal_payment = round(monthly_payment - interest_payment, 2)
            remaining_balance -= principal_payment
            remaining_balance = round(remaining_balance, 2)
            schedule.append([i, monthly_payment, interest_payment, principal_payment, remaining_balance, caching_code])

        # Convert to DataFrame
        columns = ["payment_number", "monthly_payment", "interest_payment",
                   "principal_recapture", "remaining_balance", "caching_code"]
        df = pd.DataFrame(schedule, columns=columns)

        json_string = df.to_json(orient='records')

        return json_string

    @staticmethod
    def amortization_rows_for_payment_range(amortization_json_string: str, start: int, end: Optional[int] = None) \
            -> List[AmortizationScheduleRow]:
        df = pd.DataFrame(json.loads(amortization_json_string))

        try:
            json_string = json.loads(amortization_json_string)

            if start and end:
                filtered_json = json_string[start: end]
            elif start == end or end is None:
                filtered_json = [json_string[start]]

            filtered_amortization_schedule_rows: List[AmortizationScheduleRow] = \
                [AmortizationScheduleRow(**entry) for entry in filtered_json]

            return filtered_amortization_schedule_rows

        except Exception as e:
            logging.error(f' Error selecting rows start={start}, end={end} from: {amortization_json_string}')
