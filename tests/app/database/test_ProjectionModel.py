from app.database.models import AddressModel, DealModel, UnderwritingModel, ProjectionModel, AmortizationScheduleModel
from app.repositories.BaseRepository import BaseRepository
from app.database.models import SubscriptionModel


def test_crud_projection_model_after_underwriting_and_deal(get_test_deal_model, get_test_underwriting_model_min,
                                                           test_projection_model, get_test_db):
    session = get_test_db
    test_deal = get_test_deal_model
    test_underwriting = get_test_underwriting_model_min
    test_projection = test_projection_model

    underwriting_repo = BaseRepository[UnderwritingModel](session, UnderwritingModel)
    newly_created_underwriting = underwriting_repo.add(test_underwriting)

    session.flush()
    existing_id = newly_created_underwriting.id

    existing_underwriting = session.query(UnderwritingModel).filter_by(id=existing_id).first()

    # Then create the deal
    test_deal.underwriting = existing_underwriting

    deal_repo = BaseRepository[DealModel](session, DealModel)

    newly_created_deal = deal_repo.add(test_deal)
    session.flush()

    assert newly_created_deal.id and newly_created_deal.id != 0

    # Finally create the projection
    test_projection.deal = newly_created_deal
    projection_repo = BaseRepository[ProjectionModel](session, ProjectionModel)
    newly_created_projection = projection_repo.add(test_projection)
    session.flush()

    assert newly_created_projection.id and newly_created_projection.id != 0

    # session.commit() # Only if you want to actually save.


def test_crud_projection_model_after_underwriting_and_amortization_schedule(
        test_projection_model, test_amortization_schedule_model_without_json, get_test_db):
    session = get_test_db
    test_amortization_schedule = test_amortization_schedule_model_without_json
    test_projection = test_projection_model

    amortization_schedule_repo = BaseRepository[AmortizationScheduleModel](session, AmortizationScheduleModel)
    newly_created_amortization_schedule = amortization_schedule_repo.add(test_amortization_schedule)

    session.flush()
    existing_id = newly_created_amortization_schedule.id

    existing_amortization_schedule = session.query(AmortizationScheduleModel).filter_by(id=existing_id).first()

    # Then create the projection
    test_projection_model.amortization_schedule = existing_amortization_schedule

    projection_repo = BaseRepository[ProjectionModel](session, ProjectionModel)

    newly_created_projection = projection_repo.add(test_projection_model)
    session.flush()

    assert newly_created_projection.id and newly_created_projection.id != 0

    session.commit()  # Only if you want to actually save.
