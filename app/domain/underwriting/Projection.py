from typing import Any, List

from pandas import DataFrame

from app.domain.Deal import Deal
from app.domain.underwriting.AmortizationSchedule import AmortizationSchedule
from app.domain.underwriting.ProjectionRow import ProjectionRow
from app.schemas.ProjectionSchema import ProjectionSchema


class Projection(ProjectionSchema):

    def get_projection_rows(self) -> List[ProjectionRow]:
        projection_rows: List[ProjectionRow] = []
        if self.amortization_schedule is None or self.deal is None:
            raise ValueError("Missing values, amortization_schedule and deal values need to be set")

        if self.deal.real_estate_property is None:
            raise ValueError("Missing Deal has to have RealEstateProperty set.")

        amortization_schedule = AmortizationSchedule(**self.amortization_schedule.dict())
        deal = Deal(**self.deal.dict())

        dataframe = self._create_final_projection_dataframe(amortization_schedule=amortization_schedule,
                                                            deal=deal)
        # projection_rows_json = dataframe.to_json(orient='records')
        projection_records = dataframe.to_dict('records')
        projection_rows = [ProjectionRow(**record) for record in projection_records]

        return projection_rows

    def _create_final_projection_dataframe(self, amortization_schedule: AmortizationSchedule, deal: Deal) -> DataFrame:
        amortization_period = amortization_schedule.amortization_period
        property_value = deal.real_estate_property_value
        # real_estate_property = deal.real_estate_property
        real_estate_property = deal.real_estate_property

        monthly_cashflow = 0
        if real_estate_property:
            monthly_cashflow = real_estate_property.get_total_monthly_cashflow()

        dataframe = amortization_schedule.get_basic_dataframe()
        monthly_values = self._create_monthly_appreciation_percentage_values(
            property_start_value=deal.real_estate_property_value,
            annual_percentage=3.0, amortization_period=amortization_period)
        dataframe['monthly_value'] = monthly_values

        dataframe['passive_appreciation'] = dataframe['monthly_value'].apply(lambda x: (x - property_value))

        dataframe['monthly_cashflow'] = monthly_cashflow

        return dataframe

    @staticmethod
    def _create_monthly_appreciation_percentage_values(property_start_value: float,
                                                       annual_percentage: float,
                                                       amortization_period: int) -> List[float]:
        # Convert annual rate to monthly rate
        monthly_rate = annual_percentage / 12

        # Initialize list to store appreciated values
        appreciated_values = []

        # Calculate appreciation for each month
        current_value = property_start_value
        for _ in range(amortization_period * 12):
            current_value *= (1 + monthly_rate)
            appreciated_values.append(round(current_value, 2))

        return appreciated_values
