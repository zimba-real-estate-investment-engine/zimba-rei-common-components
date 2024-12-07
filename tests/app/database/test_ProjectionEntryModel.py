from app.database.models import AddressModel, ProjectionEntryModel, UnderwritingModel
from app.repositories.BaseRepository import BaseRepository


def test_crud_project_entry_model_after_underwriting(get_test_projection_entry_model,
                                                     get_test_underwriting_model_min,get_test_db):
    session = get_test_db
    test_projection_entry = get_test_projection_entry_model
    test_underwriting = get_test_underwriting_model_min

    underwriting_repo = BaseRepository[UnderwritingModel](session, UnderwritingModel)
    newly_created_underwriting = underwriting_repo.add(test_underwriting)

    session.flush()
    existing_id = newly_created_underwriting.id

    existing_underwriting = session.query(UnderwritingModel).filter_by(id=existing_id).first()

    # Now create the projectEntry
    test_projection_entry.underwriting = existing_underwriting

    projection_entry_repo = BaseRepository[ProjectionEntryModel](session, ProjectionEntryModel)

    newly_created_projection_entry = projection_entry_repo.add(test_projection_entry)
    session.flush()

    assert newly_created_projection_entry.id and newly_created_projection_entry.id != 0

    # session.commit()  # To save,if we need some test data

