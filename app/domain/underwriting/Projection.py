from app.domain.underwriting.AmortizationSchedule import AmortizationSchedule
from app.schemas.ProjectionSchema import ProjectionSchema


class Projection(ProjectionSchema):
    pass


    @staticmethod
    def create_projection(property_value: float, amortization_schedule: AmortizationSchedule,
                          passive_appreciation_percentage: float, active_appreciation: float):