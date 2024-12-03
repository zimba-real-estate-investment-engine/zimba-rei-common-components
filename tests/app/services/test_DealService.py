import copy

from app.services.InvestorProfileService import InvestorProfileService
from app.services.RealEstatePropertyService import RealEstatePropertyService
from app.services.DealService import DealService
from app.services.UnderwritingService import UnderwritingService


def test_save_deal_min(get_test_db, get_test_deal_schema, get_test_underwriting_schema):
    db = get_test_db
    test_deal = get_test_deal_schema

    test_underwriting = get_test_underwriting_schema

    underwriting_service = UnderwritingService(db)

    newly_saved_underwriting = underwriting_service.save_underwriting(test_underwriting)

    db.flush()
    # db.commit() Only commit if you want to actually save in db.
    assert newly_saved_underwriting.id and newly_saved_underwriting.id != 0

    deal_service = DealService(db)

    test_deal.underwriting = newly_saved_underwriting

    newly_saved_deal = deal_service.save_deal(test_deal)

    db.flush()
    assert newly_saved_deal.id and newly_saved_deal.id != 0

    db.commit() # Only commit if you want to actually save in db.

#
# def test_save_deal_with_investor_profile(get_test_db, get_test_deal_schema,
#                                                  get_test_investor_profile_schema):
#     db = get_test_db
#     test_investor_profile = get_test_investor_profile_schema
#
#     investor_profile_service = InvestorProfileService(db)
#
#     newly_saved_investor_profile = investor_profile_service.save_investor_profile(test_investor_profile)
#
#     db.flush()
#     # db.commit() Only commit if you want to actually save in db.
#     assert newly_saved_investor_profile.id and newly_saved_investor_profile.id != 0
#
#     # Now create the deal
#     test_deal = get_test_deal_schema
#     # test_deal.investor_profile = existing_investor_profile
#     test_deal.investor_profile = newly_saved_investor_profile
#
#     deal_service = DealService(db)
#
#     newly_saved_deal = deal_service.save_deal(test_deal)
#
#     assert newly_saved_deal.id and newly_saved_deal.id != 0
#     assert newly_saved_deal.investor_profile.id and newly_saved_deal.investor_profile.id != 0
#
#
# def test_save_deal_with_real_estate_property(get_test_db, get_test_deal_schema,
#                                                      get_test_real_state_property_schema_unpopulated,
#                                                      get_test_address_schema,
#                                                      get_test_listing_schema):
#     db = get_test_db
#     test_real_estate_property = get_test_real_state_property_schema_unpopulated
#     test_real_estate_property.address = get_test_address_schema
#     test_real_estate_property.listing = get_test_listing_schema
#
#     real_estate_service = RealEstatePropertyService(db)
#
#     newly_saved_real_estate_property = real_estate_service.save_real_estate_property(test_real_estate_property)
#
#     db.flush()
#     # db.commit() Only commit if you want to actually save in db.
#     assert newly_saved_real_estate_property.id and newly_saved_real_estate_property.id != 0
#
#     # Now create the deal
#     test_deal = get_test_deal_schema
#     test_deal.real_estate_property = newly_saved_real_estate_property
#
#     deal_service = DealService(db)
#
#     newly_saved_deal = deal_service.save_deal(test_deal)
#
#     db.flush()
#     assert newly_saved_deal.id and newly_saved_deal.id != 0
#     assert newly_saved_deal.real_estate_property.id and newly_saved_deal.real_estate_property.id != 0
#
#
# def test_get_all(get_test_db, get_test_investor_profile_schema, get_test_real_state_property_schema_unpopulated,
#                  get_test_address_schema, get_test_listing_schema, get_test_deal_schema):
#     db = get_test_db
#
#     test_deal_1 = get_test_deal_schema
#     test_deal_2 = copy.deepcopy(test_deal_1)
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
#     test_deal_1.real_estate_property = test_real_estate_property_1_1
#     test_deal_1.investor_profile = test_investor_profile_1_1
#
#     test_deal_2.real_estate_property = test_real_estate_property_2_2
#     test_deal_2.investor_profile = test_investor_profile_2_2
#
#     deal_service = DealService(db)
#
#     newly_created_deal_1 = deal_service.save_deal(test_deal_1)
#     newly_created_deal_2 = deal_service.save_deal(test_deal_2)
#     db.flush()
#
#     assert newly_created_deal_1.id and newly_created_deal_1.id != 0
#     assert newly_created_deal_2.id and newly_created_deal_2.id != 0
#
#     deal_list = deal_service.get_all()
#
#     assert len(deal_list) >= 2
#
#     # We don't want this to be too large for testing.
#     assert len(deal_list) < 100000
#

def test_get_all_optimistic(get_test_db):
    db = get_test_db

    deal_service = DealService(db)
    deal_list = deal_service.get_all()
    assert len(deal_list) > 0