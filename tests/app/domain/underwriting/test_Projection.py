import json

import pandas as pd

from app.domain.Deal import Deal
from app.domain.RealEstateProperty import RealEstateProperty
from app.domain.underwriting.AmortizationSchedule import AmortizationSchedule
from app.domain.underwriting.Projection import Projection


def test_init(get_test_deal_schema, test_amortization_json):
    deal_schema = get_test_deal_schema
    deal = Deal(**deal_schema.dict())
    projection = Projection(deal=deal)
    assert projection


def test_dataframe_initial_structure(test_amortization_schedule_without_json):
    principal = test_amortization_schedule_without_json.principal
    annual_interest_rate = test_amortization_schedule_without_json.annual_interest_rate
    amortization_period = test_amortization_schedule_without_json.amortization_period

    amortization_schedule_json = AmortizationSchedule.generate_amortization_json(
        principal=principal,
        annual_interest_rate=annual_interest_rate,
        amortization_period=amortization_period)

    parsed_json = json.loads(amortization_schedule_json)
    dataframe = pd.DataFrame(parsed_json)
    assert dataframe.shape[0] == test_amortization_schedule_without_json.amortization_period * 12

    columns_expected = ['payment_number', 'monthly_payment', 'interest_payment',
                        'principal_recapture', 'remaining_balance', 'caching_code']

    for column in columns_expected:
        assert column in dataframe.columns


def test__create_final_projection_dataframe(test_amortization_schedule_without_json, get_test_deal_schema,
                                            get_test_real_state_property_schema_unpopulated):
    deal = Deal(**get_test_deal_schema.dict())
    real_estate_property = RealEstateProperty(**get_test_real_state_property_schema_unpopulated.dict())
    deal.real_estate_property = real_estate_property
    projection = Projection(deal=deal, amortization_schedule=test_amortization_schedule_without_json)
    dataframe = projection._create_final_projection_dataframe(
        amortization_schedule=test_amortization_schedule_without_json,
        deal=deal)
    amortization_period = test_amortization_schedule_without_json.amortization_period
    assert dataframe.shape[0] == amortization_period * 12

    records_json = dataframe.to_json(orient='records')
    assert records_json


def test_get_projection_rows(test_amortization_schedule_without_json, get_test_deal_schema,
                             get_test_real_state_property_schema_unpopulated):
    amortization_schedule = test_amortization_schedule_without_json
    deal = Deal(**get_test_deal_schema.dict())
    real_estate_property = RealEstateProperty(**get_test_real_state_property_schema_unpopulated.dict())
    deal.real_estate_property = real_estate_property
    projection = Projection(deal=deal, amortization_schedule=amortization_schedule)

    projection_rows = projection.get_projection_rows()
    assert len(projection_rows) == amortization_schedule.amortization_period * 12

