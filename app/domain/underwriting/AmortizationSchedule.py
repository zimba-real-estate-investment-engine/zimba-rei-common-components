import pandas as pd
import numpy_financial as npf

from app.schemas.AmortizationScheduleSchema import AmortizationScheduleSchema


class AmortizationSchedule(AmortizationScheduleSchema):
    pass

    def __init__(self, principal: float, annual_interest_rate: float, amortization_period: int):
        self.principal = principal
        self.annual_interest_rate = annual_interest_rate
        self.amortization_period = amortization_period
        self.amortization_schedule_json = AmortizationSchedule.generate_amortization_json(
            principal=principal, annual_interest_rate=annual_interest_rate, amortization_period=amortization_period)


    @staticmethod
    def generate_amortization_json(principal: float, annual_interest_rate: float,
                                   amortization_period: int) -> str:
        # Loan details
        principal = principal
        annual_interest_rate = annual_interest_rate
        amortization_period = amortization_period

        n_periods = amortization_period * 12
        monthly_rate = annual_interest_rate /100/ 12
        npf_payment = npf.pmt(monthly_rate, n_periods, -principal)
        monthly_payment = round(float(npf_payment), 2)

        # Create an amortization schedule
        schedule = []
        remaining_balance = principal

        for i in range(1, n_periods + 1):
            interest_payment = round(remaining_balance * monthly_rate, 2)
            principal_payment = round(monthly_payment - interest_payment, 2)
            remaining_balance -= principal_payment
            remaining_balance = round(remaining_balance, 2)
            schedule.append([i, monthly_payment, interest_payment, principal_payment, remaining_balance])

        # schedule2 = [
        #     {
        #         'Payment': round(monthly_payment, 2),
        #         'Interest': round(principal * annual_interest_rate / 100 / 12, 2),
        #         'Principal': round(monthly_payment - principal * annual_interest_rate / 100 / 12, 2),
        #         'Balance': round(principal - monthly_payment, 2)
        #     }
        #     for _ in range(n_periods)
        # ]

        # Convert to DataFrame
        columns = ["payment_number", "monthly_payment", "interest_payment", "principal_recapture", "remaining_balance"]
        df = pd.DataFrame(schedule, columns=columns)

        json_string = df.to_json(orient='records')

        return json_string

