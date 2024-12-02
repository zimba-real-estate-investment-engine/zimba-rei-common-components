import copy
from datetime import datetime

from app.database.models import InvestorProfileModel
from app.repositories.BaseRepository import BaseRepository
from app.services.InvestorProfileService import InvestorProfileService
from app.services.ListingService import ListingService
from app.services.RealEstatePropertyService import RealEstatePropertyService
from app.services.SubscriptionService import SubscriptionService
from app.services.UnderwritingService import UnderwritingService


def test_save_underwriting_min(get_test_db, get_test_underwriting_schema):
    db = get_test_db
    test_underwriting = get_test_underwriting_schema

    underwriting_service = UnderwritingService(db)

    newly_saved_underwriting = underwriting_service.save_underwriting(test_underwriting)

    db.flush()
    # db.commit() Only commit if you want to actually save in db.
    assert newly_saved_underwriting.id and newly_saved_underwriting.id != 0


def test_save_underwriting_with_investor_profile(get_test_db, get_test_underwriting_schema,
                                                 get_test_investor_profile_schema):
    db = get_test_db
    test_investor_profile = get_test_investor_profile_schema

    investor_profile_service = InvestorProfileService(db)

    newly_saved_investor_profile = investor_profile_service.save_investor_profile(test_investor_profile)

    db.flush()
    # db.commit() Only commit if you want to actually save in db.
    assert newly_saved_investor_profile.id and newly_saved_investor_profile.id != 0

    # Now create the underwriting
    test_underwriting = get_test_underwriting_schema
    # test_underwriting.investor_profile = existing_investor_profile
    test_underwriting.investor_profile = newly_saved_investor_profile

    underwriting_service = UnderwritingService(db)

    newly_saved_underwriting = underwriting_service.save_underwriting(test_underwriting)

    assert newly_saved_underwriting.id and newly_saved_underwriting.id != 0
    assert newly_saved_underwriting.investor_profile.id and newly_saved_underwriting.investor_profile.id != 0


def test_save_underwriting_with_real_estate_property(get_test_db, get_test_underwriting_schema,
                                                     get_test_real_state_property_schema_unpopulated,
                                                     get_test_address_schema,
                                                     get_test_listing_schema):
    db = get_test_db
    test_real_estate_property = get_test_real_state_property_schema_unpopulated
    test_real_estate_property.address = get_test_address_schema
    test_real_estate_property.listing = get_test_listing_schema

    real_estate_service = RealEstatePropertyService(db)

    newly_saved_real_estate_property = real_estate_service.save_real_estate_property(test_real_estate_property)

    db.flush()
    # db.commit() Only commit if you want to actually save in db.
    assert newly_saved_real_estate_property.id and newly_saved_real_estate_property.id != 0

    # Now create the underwriting
    test_underwriting = get_test_underwriting_schema
    test_underwriting.real_estate_property = newly_saved_real_estate_property

    underwriting_service = UnderwritingService(db)

    newly_saved_underwriting = underwriting_service.save_underwriting(test_underwriting)

    db.flush()
    assert newly_saved_underwriting.id and newly_saved_underwriting.id != 0
    assert newly_saved_underwriting.real_estate_property.id and newly_saved_underwriting.real_estate_property.id != 0


def test_get_all(get_test_db, get_test_investor_profile_schema, get_test_real_state_property_schema_unpopulated,
                 get_test_address_schema, get_test_listing_schema, get_test_underwriting_schema):
    db = get_test_db

    test_underwriting_1 = get_test_underwriting_schema
    test_underwriting_2 = copy.deepcopy(test_underwriting_1)

    test_investor_profile_1_1 = get_test_investor_profile_schema
    test_investor_profile_2_2 = copy.deepcopy(test_investor_profile_1_1)

    test_address_1_1 = get_test_address_schema
    test_address_2_2 = copy.deepcopy(test_address_1_1)

    test_listing_1_1 = get_test_listing_schema
    test_listing_2_2 = copy.deepcopy(test_listing_1_1)

    test_real_estate_property_1_1 = get_test_real_state_property_schema_unpopulated
    test_real_estate_property_1_1.address = test_address_1_1
    test_real_estate_property_1_1.listing = test_listing_1_1

    test_real_estate_property_2_2 = copy.deepcopy(test_real_estate_property_1_1)
    test_real_estate_property_2_2.address = test_address_2_2
    test_real_estate_property_2_2.listing = test_listing_2_2

    test_underwriting_1.real_estate_property = test_real_estate_property_1_1
    test_underwriting_1.investor_profile = test_investor_profile_1_1

    test_underwriting_2.real_estate_property = test_real_estate_property_2_2
    test_underwriting_2.investor_profile = test_investor_profile_2_2

    underwriting_service = UnderwritingService(db)

    newly_created_underwriting_1 = underwriting_service.save_underwriting(test_underwriting_1)
    newly_created_underwriting_2 = underwriting_service.save_underwriting(test_underwriting_2)
    db.flush()

    assert newly_created_underwriting_1.id and newly_created_underwriting_1.id != 0
    assert newly_created_underwriting_2.id and newly_created_underwriting_2.id != 0

    underwriting_list = underwriting_service.get_all()

    assert len(underwriting_list) >= 2

    # We don't want this to be too large for testing.
    assert len(underwriting_list) < 100000
