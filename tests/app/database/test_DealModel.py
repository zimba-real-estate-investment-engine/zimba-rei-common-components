from app.database.models import AddressModel, DealModel, UnderwritingModel
from app.repositories.BaseRepository import BaseRepository
from app.database.models import SubscriptionModel


def test_crud_deal_model_after_underwriting(get_test_deal_model, get_test_underwriting_model_min, get_test_db):
    session = get_test_db
    test_deal = get_test_deal_model
    test_underwriting = get_test_underwriting_model_min

    underwriting_repo = BaseRepository[UnderwritingModel](session, UnderwritingModel)
    newly_created_underwriting = underwriting_repo.add(test_underwriting)

    session.flush()
    existing_id = newly_created_underwriting.id

    existing_underwriting = session.query(UnderwritingModel).filter_by(id=existing_id).first()

    # Now create the deal
    test_deal.underwriting = existing_underwriting

    deal_repo = BaseRepository[DealModel](session, DealModel)

    newly_created_deal = deal_repo.add(test_deal)
    session.flush()

    assert newly_created_deal.id and newly_created_deal.id != 0

    # session.commit()  # To save,if we need some test data

