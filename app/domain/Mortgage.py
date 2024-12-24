from app.domain.underwriting.AmortizationCachingCode import AmortizationCachingCode
from app.domain.underwriting.AmortizationSchedule import AmortizationSchedule
from app.schemas.MortgageSchema import MortgageSchema


class Mortgage(MortgageSchema):

    def __init__(self, principal: float, annual_interest_rate: float, amortization_period: int, **kwargs):
        super().__init__(principal=principal, annual_interest_rate=annual_interest_rate,
                         amortization_period=amortization_period, **kwargs)

        self.principal = principal
        self.annual_interest_rate = annual_interest_rate
        self.amortization_period = amortization_period
        self.monthly_payment = AmortizationSchedule.get_monthly_payment(principal, annual_interest_rate,
                                                                        amortization_period)

        amortization_schema_json = AmortizationSchedule.generate_amortization_json(principal, annual_interest_rate,
                                                                                   amortization_period)
        amortization_caching_code = AmortizationCachingCode(principal=principal,
                                                            annual_interest_rate=annual_interest_rate,
                                                            amortization_period=amortization_period)
        caching_code_string = amortization_caching_code.model_dump_json()

        amortization_schedule = AmortizationSchedule(principal=principal, annual_interest_rate=annual_interest_rate,
                                                     amortization_period=amortization_period,
                                                     amortization_schedule_json=amortization_schema_json,
                                                     caching_code=caching_code_string)

        self.amortization_schedule = amortization_schedule
    # amortization_schedule_json: Optional[str] = ''
    # created_date: Optional[datetime] = None
    # caching_code: Optional[str] = None
    # principal: float
    # annual_interest_rate: float
    # amortization_period: int

    # MortgageSchema
    #
    # appraisal_value: Optional[float] = 0
    # down_payment: Optional[float] = 0
    # principal: Optional[float] = 800000
    # issued_date: datetime
    # pre_qualified: Optional[bool]
    # pre_approved: Optional[bool]
    # loan_to_value: float
    # annual_interest_rate: float = 5
    # term: Optional[int] = 5
    # amortization_period:  int = 30
    # monthly_payment: Optional[float]
    # owner_occupied: bool = False
    # insurance: float = 0
    # amortization_schedule: Optional[AmortizationScheduleSchema] = None
