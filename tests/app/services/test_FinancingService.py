import copy
from datetime import datetime

from app.database.models import InvestorProfileModel
from app.repositories.BaseRepository import BaseRepository
from app.services.FinancingService import FinancingService
from app.services.InvestorProfileService import InvestorProfileService
from app.services.ListingService import ListingService
from app.services.SubscriptionService import SubscriptionService


def test_get_all(get_test_db, get_test_investor_profile_schema, get_test_financing_schema_minimum,
                 get_test_mortgage_schema):

    db = get_test_db
    test_investor_profile = get_test_investor_profile_schema
    test_financing_1 = get_test_financing_schema_minimum
    test_financing_2 = copy.deepcopy(test_financing_1)

    test_mortgage_1 = get_test_mortgage_schema
    test_mortgage_2 = copy.deepcopy(test_mortgage_1)

    test_financing_1.mortgages = [test_mortgage_1]
    test_financing_2.mortgages = [test_mortgage_2]

    test_investor_profile.financing_sources = [test_financing_1, test_financing_2]

    investor_profile_service = InvestorProfileService(db)

    # We need to save the investor profile first
    newly_saved_investor_profile = investor_profile_service.save_investor_profile(test_investor_profile)

    db.flush()
    # db.commit() Only commit if you want to actually save in db.

    assert newly_saved_investor_profile.id and newly_saved_investor_profile.id != 0
    assert len(newly_saved_investor_profile.financing_sources) >= 2

    # Now test the get_all
    financing_service = FinancingService(db)

    financing_sources_list = financing_service.get_all()

    assert len(financing_sources_list) >= 2
#
# def test_save_investor_profile_cascade_to_financing(get_test_db, get_test_investor_profile_schema,
#                                                     get_test_financing_schema_minimum):
#     db = get_test_db
#     test_investor_profile = get_test_investor_profile_schema
#     test_financing_source_1 = get_test_financing_schema_minimum
#
#     test_investor_profile.financing_sources = [test_financing_source_1]
#
#     investor_profile_service = InvestorProfileService(db)
#
#     newly_saved_investor_profile = investor_profile_service.save_investor_profile(test_investor_profile)
#
#     assert newly_saved_investor_profile.id and newly_saved_investor_profile.id != 0
#     assert newly_saved_investor_profile.financing_sources[0].id and newly_saved_investor_profile.financing_sources[
#         0].id != 0
#
#
# def test_save_investor_profile_cascade_to_mortgage(get_test_db, get_test_investor_profile_schema,
#                                                    get_test_financing_schema_minimum, get_test_mortgage_schema):
#     db = get_test_db
#     test_investor_profile = get_test_investor_profile_schema
#     test_financing_source_1 = get_test_financing_schema_minimum
#     test_mortgage = get_test_mortgage_schema
#
#     test_financing_source_1.mortgages = [test_mortgage]
#     test_investor_profile.financing_sources = [test_financing_source_1]
#
#     investor_profile_service = InvestorProfileService(db)
#
#     newly_saved_investor_profile = investor_profile_service.save_investor_profile(test_investor_profile)
#
#     assert newly_saved_investor_profile.id and newly_saved_investor_profile.id != 0
#     assert newly_saved_investor_profile.financing_sources[0].id and \
#            newly_saved_investor_profile.financing_sources[0].id != 0
#     assert newly_saved_investor_profile.financing_sources[0].mortgages[0].id and \
#            newly_saved_investor_profile.financing_sources[0].mortgages[0].id != 0
#
#
# def test_get_all(get_test_db, get_test_investor_profile_schema, get_test_financing_schema_minimum, get_test_mortgage_schema):
#     db = get_test_db
#     test_investor_profile_1 = get_test_investor_profile_schema
#     test_investor_profile_2 = copy.deepcopy(test_investor_profile_1)
#
#     test_financing_source_1_1 = get_test_financing_schema_minimum
#     test_financing_source_1_2 = copy.deepcopy(test_financing_source_1_1)
#
#     test_mortgage_1_1_1 = get_test_mortgage_schema
#     test_mortgage_1_2_1 = copy.deepcopy(test_mortgage_1_1_1)
#
#     test_financing_source_1_1.mortgages = [test_mortgage_1_1_1]
#     test_investor_profile_1.financing_sources = [test_financing_source_1_1]
#
#     test_financing_source_1_2.mortgages = [test_mortgage_1_2_1]
#     test_investor_profile_2.financing_sources = [test_financing_source_1_2]
#
#     investor_profile_service = InvestorProfileService(db)
#
#     newly_saved_investor_profile_1 = investor_profile_service.save_investor_profile(test_investor_profile_1)
#     newly_saved_investor_profile_2 = investor_profile_service.save_investor_profile(test_investor_profile_2)
#
#     db.flush()
#
#     investor_profiles_list = investor_profile_service.get_all()
#     assert len(investor_profiles_list) >= 2
#
#     # We don't want this to be too large for testing.
#     assert len(investor_profiles_list) < 100000

