from app.database.models import DropdownOptionModel
from app.repositories.BaseRepository import BaseRepository


def test_crud_dropdown_option_model(test_dropdown_option_model, get_test_db):
    session = get_test_db
    new_dropdown_options_model = test_dropdown_option_model

    repo = BaseRepository[DropdownOptionModel](session, DropdownOptionModel)

    # CREATE
    results = repo.add(new_dropdown_options_model)
    assert results
    session.flush()

    # READ
    newly_created = repo.get_by_id(results.id)

    # DELETE and commit, we'll need to clean up test data
    repo.delete(results.id)
    session.commit()
