import copy
from datetime import datetime

from app.database.models import InvestorProfileModel
from app.repositories.BaseRepository import BaseRepository
from app.services.FinancingService import FinancingService
from app.services.InvestorProfileService import InvestorProfileService
from app.services.ListingService import ListingService
from app.services.MortgageService import MortgageService
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
    mortgage_service = MortgageService(db)

    mortgages_list = mortgage_service.get_all()

    assert len(mortgages_list) >= 2


