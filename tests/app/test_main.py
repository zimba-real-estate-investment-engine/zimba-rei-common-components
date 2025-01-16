import time

from app.database.models import SubscriptionModel
from app.domain.UnderwritingProcess import UnderwritingProcess
from app.repositories.BaseRepository import BaseRepository
from app.schemas.DropdownOptionSchema import DropdownOptionSearchSchema
from app.schemas.InvestorProfileSchema import InvestorProfileSchema, InvestorProfileSearchSchema
from app.schemas.SubscriptionSchema import SubscriptionSchema
from app.schemas.UnderwritingSchema import UnderwritingCreateDealSchema, UnderwritingCreateDealFromURLSchema
from app.services.InvestorProfileService import InvestorProfileService
from app.services.RealEstatePropertyService import RealEstatePropertyService


def test_create_subscription(get_test_subscription_schema, test_fastapi_client, get_test_db):
    test_subscription = get_test_subscription_schema
    client = test_fastapi_client
    test_db = get_test_db

    response = client.post("/subscriptions/", data=test_subscription.json())
    assert response.status_code == 200

    # Confirms that the returned value can be instantiated from the pydantic schema
    newly_created_subscription = SubscriptionSchema(**response.json())

    # Clean up to avoid bloated migrations. Using BaseRepository which uses SqlAlchemy migrations ¯\_(ツ)_/¯
    subscription_model = SubscriptionModel(**newly_created_subscription.model_dump())
    base_repo = BaseRepository(test_db, SubscriptionModel)
    base_repo.delete(subscription_model.id)
    test_db.commit()


def test_get_subscriptions(test_fastapi_client):
    client = test_fastapi_client
    response = client.get("/subscriptions/")
    assert response.status_code == 200


def test_get_dropdown_options_by_dropdown_name(test_fastapi_client):
    request_payload = DropdownOptionSearchSchema(dropdown_name="real_estate_property_capital_investments")
    json_payload = request_payload.json()
    client = test_fastapi_client
    response = client.post("/dropdown_options/get_by_dropdown_name/", data=json_payload)
    assert response.status_code == 200


def test_get_investor_profiles(test_fastapi_client, request):
    client = test_fastapi_client
    response = client.get("/investor-profiles/")
    assert response.status_code == 200


def test_get_real_estate_properties(test_fastapi_client, request):
    client = test_fastapi_client
    response = client.get("/real-estate-properties/")
    assert response.status_code == 200


def test_get_investor_profile(test_fastapi_client, request):
    client = test_fastapi_client

    request_payload = InvestorProfileSearchSchema(id=70)
    request_json = request_payload.json()

    response = client.post("/investor-profiles/find-by-id", data=request_json)
    assert response.status_code == 200

    result_json = response.json()
    investor_profile_schema = InvestorProfileSchema(**result_json)  # Ensure we can instantiate the pydantic object
    assert investor_profile_schema.id and investor_profile_schema.id != 0


def test_create_investor_profile(test_fastapi_client, request, get_test_investor_profile_schema):
    test_investor_profile = get_test_investor_profile_schema
    request_json = test_investor_profile.json()

    client = test_fastapi_client
    response = client.post("/investor-profiles/", data=request_json)
    assert response.status_code == 200

    result_json = response.json()
    investor_profile_schema = InvestorProfileSchema(**result_json)  # Ensure we can instantiate the pydantic object
    assert investor_profile_schema.id and investor_profile_schema.id != 0


def test_get_underwritings(test_fastapi_client, request):
    client = test_fastapi_client
    response = client.get("/underwritings/")
    assert response.status_code == 200


def test_create_deal_from_url(test_fastapi_client, get_test_investor_profile_schema, get_test_db,
                              get_test_listing_schema):
    # url = 'https://www.realtor.com/realestateandhomes-detail/67-New-York-Ave-NW_Washington_DC_20001_M52254-63513'
    url = 'https://www.realtor.ca/real-estate/27608941/20-kanata-rockeries-ottawa-9007-kanata-kanata-lakesheritage-hills'
    db = get_test_db

    investor_profile_schema = get_test_investor_profile_schema

    # Create the investor profile that will be needed to be in the database
    investor_profile_service = InvestorProfileService(db)
    newly_created_investor_profile = investor_profile_service.save_investor_profile(investor_profile_schema)

    assert newly_created_investor_profile.id

    request_schema = UnderwritingCreateDealFromURLSchema(investor_profile_id=newly_created_investor_profile.id,
                                                         listing_url=url)

    request_json = request_schema.json()

    client = test_fastapi_client
    response = client.post("/underwriting/create-deal-from-url/", data=request_json)
    assert response.status_code == 200


def test_get_deal_from_url_pre_existing(test_fastapi_client):
    investor_profile_id = 75
    # listing_url = 'https://www.realtor.ca/real-estate/27608941/20-kanata-rockeries-ottawa-9007-kanata-kanata-lakesheritage-hills'
    # listing_url = 'https://www.realtor.com/realestateandhomes-detail/26-Glen-Echo_Trabuco-Canyon_CA_92679_M23444-70469'
    # listing_url = 'https://www.realtor.ca/real-estate/27628974/18-birch-avenue-ottawa-3202-rockcliffe'
    listing_url = 'https://www.realtor.ca/real-estate/27553080/14-3466-keswick-bv-sw-edmonton-keswick-area'
    request_schema = UnderwritingCreateDealFromURLSchema(investor_profile_id=investor_profile_id,
                                                         listing_url=listing_url)

    request_json = request_schema.json()

    client = test_fastapi_client
    response = client.post("/underwriting/create-deal-from-url/", data=request_json)
    assert response.status_code == 200
