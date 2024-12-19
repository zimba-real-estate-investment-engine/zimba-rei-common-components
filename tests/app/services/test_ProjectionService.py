import copy

from app.schemas.ProjectionSchema import ProjectionSchema
from app.services.InvestorProfileService import InvestorProfileService
from app.services.ProjectionService import ProjectionService
from app.services.RealEstatePropertyService import RealEstatePropertyService
from app.services.DealService import DealService
from app.services.UnderwritingService import UnderwritingService


def test_save_projection_min(get_test_db, get_test_deal_schema, get_test_underwriting_schema, test_projection_schema):
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

    # finally test saving projection
    test_projection = test_projection_schema
    test_projection.deal = newly_saved_deal

    projection_service = ProjectionService(db)
    newly_saved_projection = projection_service.save_projection(test_projection)
    db.flush()

    assert newly_saved_projection.id and newly_saved_projection.id != 0

    # db.commit()  # Only commit if you want to actually save in db.


def test_find_projection_by_deal_id (get_test_db, get_test_deal_schema,
                                     get_test_underwriting_schema, test_projection_schema):
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

    # Create at least two projections
    test_projection_1 = test_projection_schema
    test_projection_2 = copy.deepcopy(test_projection_1)
    test_projection_1.deal = newly_saved_deal
    test_projection_2.deal = newly_saved_deal

    projection_service = ProjectionService(db)
    newly_saved_projection_1 = projection_service.save_projection(test_projection_1)
    newly_saved_projection_2 = projection_service.save_projection(test_projection_2)
    db.flush()

    assert newly_saved_projection_1.id and newly_saved_projection_1.id != 0
    assert newly_saved_projection_2.id and newly_saved_projection_2.id != 0

    # Search for projections by deal Id
    search_results = projection_service.get_projection_by_deal_id(deal_id=newly_saved_deal.id)
    assert len(search_results) == 2

    first_result = search_results[0]
    assert isinstance(first_result, ProjectionSchema)
    assert first_result.id == newly_saved_projection_1.id or first_result.id == newly_saved_projection_2.id


def test_get_all_optimistic(get_test_db):
    db = get_test_db

    projection_service = ProjectionService(db)
    projection_list = projection_service.get_all()
    assert len(projection_list) > 0
