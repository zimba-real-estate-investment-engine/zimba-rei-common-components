from app.database.models import AddressModel, AmortizationScheduleModel
from app.domain.underwriting.AmortizationCachingCode import AmortizationCachingCode
from app.repositories.BaseRepository import BaseRepository
from app.database.models import SubscriptionModel


def test_crud_amortization_schedule(test_amortization_schedule_model_without_json,
                                    test_amortization_json,
                                    get_test_db):
    session = get_test_db
    test_amortization_json = test_amortization_json
    test_amortization_model = test_amortization_schedule_model_without_json

    test_amortization_model.amortization_schedule_json = test_amortization_json

    repo = BaseRepository[AmortizationScheduleModel](session, AmortizationScheduleModel)

    # CREATE
    results = repo.add(test_amortization_model)
    assert results
    session.flush()

    # # READ
    newly_created = repo.get_by_id(results.id)
    assert newly_created.id == results.id and newly_created.id != 0
    # assert newly_created.state == results.state

    # DELETE and commit, we'll need to clean up test data
    # repo.delete(results.id)
    session.commit()

