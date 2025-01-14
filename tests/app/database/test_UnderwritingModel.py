from app.database.models import AddressModel, ListingModel, UnderwritingModel, InvestorProfileModel
from app.database.models import RealEstatePropertyModel
from app.repositories.BaseRepository import BaseRepository


def test_crud_underwriting_min_model(get_test_underwriting_model_min, get_test_db):
    session = get_test_db
    test_underwriting = get_test_underwriting_model_min

    underwriting_repo = BaseRepository[UnderwritingModel](session, UnderwritingModel)
    newly_created_underwriting = underwriting_repo.add(test_underwriting)
    session.flush()

    assert newly_created_underwriting.id and newly_created_underwriting.id != 0

    session.commit()


def test_crud_underwriting_with_investor_profile(get_test_underwriting_model_min, get_test_investor_profile_model,
                                                 get_test_db):
    session = get_test_db

    # Underwriting is done from a pre-existing investor profile or real estate property
    test_investor_profile = get_test_investor_profile_model

    investor_profile_repository = BaseRepository[InvestorProfileModel](session, InvestorProfileModel)
    newly_created_investor_profile = investor_profile_repository.add(test_investor_profile)
    session.flush()

    assert newly_created_investor_profile.id and newly_created_investor_profile.id != 0

    # Now create the underwriting
    test_underwriting = get_test_underwriting_model_min
    test_underwriting.investor_profile = newly_created_investor_profile

    underwriting_repository = BaseRepository[UnderwritingModel](session, UnderwritingModel)
    newly_created_underwriting = underwriting_repository.add(test_underwriting)
    session.flush()

    assert newly_created_underwriting.id and newly_created_underwriting.id != 0

    # session.commit() # Only if we want to save this


def test_crud_underwriting_with_real_estate_property(get_test_underwriting_model_min,
                                                     get_test_real_estate_property_model,
                                                     get_test_address_model,
                                                     get_test_listing_model,
                                                     get_test_db):
    session = get_test_db

    # Underwriting is done from a pre-existing investor profile or real estate property
    test_real_estate_property = get_test_real_estate_property_model
    test_address = get_test_address_model
    test_listing = get_test_listing_model

    test_real_estate_property.address = test_address
    test_real_estate_property.listing = test_listing

    re_repository = BaseRepository[RealEstatePropertyModel](session, RealEstatePropertyModel)
    newly_created_real_estate_property = re_repository.add(test_real_estate_property)
    session.flush()

    assert newly_created_real_estate_property.id and newly_created_real_estate_property.id != 0

    # # Now create the underwriting
    test_underwriting = get_test_underwriting_model_min
    test_underwriting.real_estate_property = newly_created_real_estate_property

    underwriting_repository = BaseRepository[UnderwritingModel](session, UnderwritingModel)
    newly_created_underwriting = underwriting_repository.add(test_underwriting)
    session.flush()

    assert newly_created_underwriting.id and newly_created_underwriting.id != 0
    assert newly_created_underwriting.real_estate_property.id and \
           newly_created_underwriting.real_estate_property.id != 0

    session.commit()  # Only if we want to save this


def test_crud_underwriting_with_real_estate_property_and_investor_profile(
        get_test_underwriting_model_min,
        get_test_real_estate_property_model,
        get_test_investor_profile_model,
        get_test_address_model,
        get_test_listing_model,
        get_test_db):
    session = get_test_db

    # Underwriting is done from a pre-existing investor profile or real estate property
    test_real_estate_property = get_test_real_estate_property_model
    test_address = get_test_address_model
    test_listing = get_test_listing_model

    test_real_estate_property.address = test_address
    test_real_estate_property.listing = test_listing

    re_repository = BaseRepository[RealEstatePropertyModel](session, RealEstatePropertyModel)
    newly_created_real_estate_property = re_repository.add(test_real_estate_property)
    session.flush()

    assert newly_created_real_estate_property.id and newly_created_real_estate_property.id != 0

    test_investor_profile = get_test_investor_profile_model

    investor_profile_repository = BaseRepository[InvestorProfileModel](session, InvestorProfileModel)
    newly_created_investor_profile = investor_profile_repository.add(test_investor_profile)
    session.flush()

    assert newly_created_investor_profile.id and newly_created_investor_profile.id != 0

    # # Now create the underwriting
    test_underwriting = get_test_underwriting_model_min
    test_underwriting.real_estate_property = newly_created_real_estate_property
    test_underwriting.investor_profile = newly_created_investor_profile

    underwriting_repository = BaseRepository[UnderwritingModel](session, UnderwritingModel)
    newly_created_underwriting = underwriting_repository.add(test_underwriting)
    session.flush()

    assert newly_created_underwriting.id and newly_created_underwriting.id != 0
    assert newly_created_underwriting.real_estate_property.id and \
           newly_created_underwriting.real_estate_property.id != 0
    assert newly_created_underwriting.investor_profile.id and \
           newly_created_underwriting.investor_profile.id != 0

    session.commit()  # Only if we want to save this

    # test_listing_model = get_test_listing_model
    #
    # listing_repo = BaseRepository[ListingModel](session, ListingModel)
    # newly_created_listing = listing_repo.add(test_listing_model)
    # session.flush()
    #
    # assert newly_created_listing.id and newly_created_listing.id != 0
    #
    # re_repo = BaseRepository[RealEstatePropertyModel](session, RealEstatePropertyModel)
    # test_real_estate_property_model.address = test_address
    # test_real_estate_property_model.listing = newly_created_listing
    # newly_created_real_estate_property = re_repo.add(test_real_estate_property_model)
    # session.flush()
    #
    # # Make sure the id was autoincremented
    # assert newly_created_real_estate_property.id and newly_created_real_estate_property.id != 0
    # newly_created_address = newly_created_real_estate_property.address
    #
    # assert newly_created_address.id and newly_created_address.id != 0
    #
    # # Cleanup, you can comment these out to create test data
    # re_repo.delete(newly_created_real_estate_property.id)
    # listing_repo.delete(newly_created_listing.id)
    #
    # address_repo = BaseRepository[AddressModel](session, AddressModel)
    # address_repo.delete(newly_created_address.id)
    #
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
