from app.database.models import AddressModel, ListingModel
from app.database.models import RealEstatePropertyModel
from app.repositories.BaseRepository import BaseRepository


def test_crud_real_estate_property_min_model(get_test_real_estate_property_model, get_test_db, get_test_listing_model):
    session = get_test_db
    test_real_estate_property_model = get_test_real_estate_property_model
    test_listing_model = get_test_listing_model

    listing_repo = BaseRepository[ListingModel](session, ListingModel)
    newly_created_listing = listing_repo.add(test_listing_model)
    session.flush()

    assert newly_created_listing.id and newly_created_listing.id != 0

    # Now create real estate property. We don't want to create a real estate property without a listing
    test_real_estate_property_model.listing = newly_created_listing  # Cannot be null
    re_repo = BaseRepository[RealEstatePropertyModel](session, RealEstatePropertyModel)
    newly_saved_real_estate_property = re_repo.add(test_real_estate_property_model)
    session.flush()
    #
    assert newly_saved_real_estate_property.id and newly_saved_real_estate_property.id != 0

    # Clean up
    re_repo.delete(newly_saved_real_estate_property.id)
    listing_repo.delete(newly_created_listing.id)
    session.commit()


def test_crud_real_estate_property_with_address(get_test_real_estate_property_model, get_test_listing_model,
                                                get_test_db, get_test_address_model):
    session = get_test_db
    test_real_estate_property_model = get_test_real_estate_property_model
    test_address = get_test_address_model
    # new_real_estate_property_model.address = get_test_address_model

    test_listing_model = get_test_listing_model

    listing_repo = BaseRepository[ListingModel](session, ListingModel)
    newly_created_listing = listing_repo.add(test_listing_model)
    session.flush()

    assert newly_created_listing.id and newly_created_listing.id != 0

    re_repo = BaseRepository[RealEstatePropertyModel](session, RealEstatePropertyModel)
    test_real_estate_property_model.address = test_address
    test_real_estate_property_model.listing = newly_created_listing
    newly_created_real_estate_property = re_repo.add(test_real_estate_property_model)
    session.flush()

    # Make sure the id was autoincremented
    assert newly_created_real_estate_property.id and newly_created_real_estate_property.id != 0
    newly_created_address = newly_created_real_estate_property.address

    assert newly_created_address.id and newly_created_address.id != 0

    # Cleanup, you can comment these out to create test data
    re_repo.delete(newly_created_real_estate_property.id)
    listing_repo.delete(newly_created_listing.id)

    address_repo = BaseRepository[AddressModel](session, AddressModel)
    address_repo.delete(newly_created_address.id)

    session.commit()



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
