from app.database.models import AddressModel
from app.database.models import RealEstatePropertyModel
from app.repositories.BaseRepository import BaseRepository


def test_crud_real_estate_property_min_model(get_test_real_estate_property_model, get_test_db):
    session = get_test_db
    new_real_estate_property_model = get_test_real_estate_property_model

    repo = BaseRepository[RealEstatePropertyModel](session, RealEstatePropertyModel)

    # CREATE
    results = repo.add(new_real_estate_property_model)
    assert results
    session.commit()

    # READ
    newly_created = repo.get_by_id(results.id)
    # assert newly_created.id == results.id
    # assert newly_created.state == results.state

    # DELETE and commit, we'll need to clean up test data
    # repo.delete(results.id)
    # session.commit()

    #
    #
    # repository.
    #
    # repository.add(test_subscription)
    #
    # id = test_subscription.id
    #
    # returned_instance = repository.get(id)
    # assert returned_instance


def test_crud_real_estate_property_with_address(get_test_real_estate_property_model, get_test_address_model, get_test_db):
    session = get_test_db
    new_real_estate_property_model = get_test_real_estate_property_model
    new_real_estate_property_model.address = get_test_address_model

    repo = BaseRepository[RealEstatePropertyModel](session, RealEstatePropertyModel)

    # CREATE
    results = repo.add(new_real_estate_property_model)
    assert results
    session.commit()

    # READ
    newly_created = repo.get_by_id(results.id)
    # assert newly_created.id == results.id
    # assert newly_created.state == results.state

    # DELETE and commit, we'll need to clean up test data
    # repo.delete(results.id)
    # session.commit()


def test_crud_real_estate_property_with_listing(get_test_real_estate_property_model,
                                                get_test_listing_model, get_test_db):
    session = get_test_db
    new_real_estate_property_model = get_test_real_estate_property_model
    new_real_estate_property_model.listing = get_test_listing_model

    repo = BaseRepository[RealEstatePropertyModel](session, RealEstatePropertyModel)

    # CREATE
    results = repo.add(new_real_estate_property_model)
    assert results
    session.commit()

    # READ
    newly_created = repo.get_by_id(results.id)
    # assert newly_created.id == results.id
    # assert newly_created.state == results.state

    # DELETE and commit, we'll need to clean up test data
    # repo.delete(results.id)
    # session.commit()
