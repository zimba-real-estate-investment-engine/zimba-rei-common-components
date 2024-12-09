import copy

from app.services.InvestorProfileService import InvestorProfileService
from app.services.ProjectionEntryService import ProjectionEntryService
from app.services.RealEstatePropertyService import RealEstatePropertyService
from app.services.DealService import DealService
from app.services.UnderwritingService import UnderwritingService


def test_save_projection_entry_min(get_test_db, get_test_projection_entry_schema, get_test_underwriting_schema):
    db = get_test_db
    test_projection_entry = get_test_projection_entry_schema

    test_underwriting = get_test_underwriting_schema

    underwriting_service = UnderwritingService(db)

    newly_saved_underwriting = underwriting_service.save_underwriting(test_underwriting)

    db.flush()
    # db.commit() Only commit if you want to actually save in db.
    assert newly_saved_underwriting.id and newly_saved_underwriting.id != 0

    projection_entry_service = ProjectionEntryService(db)

    test_projection_entry.underwriting = newly_saved_underwriting

    newly_saved_projection_entry = projection_entry_service.save_projection_entry(test_projection_entry)

    db.flush()
    assert newly_saved_projection_entry.id and newly_saved_projection_entry.id != 0

    # db.commit()  # Only commit if you want to actually save in db.


# def test_get_all(get_test_db, get_test_investor_profile_schema, get_test_real_state_property_schema_unpopulated,
#                  get_test_address_schema, get_test_listing_schema, get_test_projection_entry_schema):
#     db = get_test_db
#
#     test_projection_entry_1 = get_test_projection_entry_schema
#     test_projection_entry_2 = copy.deepcopy(test_projection_entry_1)
#
#     test_investor_profile_1_1 = get_test_investor_profile_schema
#     test_investor_profile_2_2 = copy.deepcopy(test_investor_profile_1_1)
#
#     test_address_1_1 = get_test_address_schema
#     test_address_2_2 = copy.deepcopy(test_address_1_1)
#
#     test_listing_1_1 = get_test_listing_schema
#     test_listing_2_2 = copy.deepcopy(test_listing_1_1)
#
#     test_real_estate_property_1_1 = get_test_real_state_property_schema_unpopulated
#     test_real_estate_property_1_1.address = test_address_1_1
#     test_real_estate_property_1_1.listing = test_listing_1_1
#
#     test_real_estate_property_2_2 = copy.deepcopy(test_real_estate_property_1_1)
#     test_real_estate_property_2_2.address = test_address_2_2
#     test_real_estate_property_2_2.listing = test_listing_2_2
#
#     test_projection_entry_1.real_estate_property = test_real_estate_property_1_1
#     test_projection_entry_1.investor_profile = test_investor_profile_1_1
#
#     test_projection_entry_2.real_estate_property = test_real_estate_property_2_2
#     test_projection_entry_2.investor_profile = test_investor_profile_2_2
#
#     projection_entry_service = Projection_EntryService(db)
#
#     newly_created_projection_entry_1 = projection_entry_service.save_projection_entry(test_projection_entry_1)
#     newly_created_projection_entry_2 = projection_entry_service.save_projection_entry(test_projection_entry_2)
#     db.flush()
#
#     assert newly_created_projection_entry_1.id and newly_created_projection_entry_1.id != 0
#     assert newly_created_projection_entry_2.id and newly_created_projection_entry_2.id != 0
#
#     projection_entry_list = projection_entry_service.get_all()
#
#     assert len(projection_entry_list) >= 2
#
#     # We don't want this to be too large for testing.
#     assert len(projection_entry_list) < 100000
#

def test_get_all_optimistic(get_test_db):   # does not create the data it tests...not good
    db = get_test_db

    projection_entry_service = ProjectionEntryService(db)
    projection_entry_list = projection_entry_service.get_all()
    assert len(projection_entry_list) > 0
