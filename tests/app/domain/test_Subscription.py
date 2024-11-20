from app.domain.Subscription import Subscription


def test_init_from_schema(get_test_subscription_schema):
    test_subscription = get_test_subscription_schema
    subscription = Subscription(**test_subscription.dict())
    assert subscription.service_subscribed_to == test_subscription.service_subscribed_to


def test_generate_unsubscribe_token(get_test_subscription_schema):
    test_subscription = Subscription(**get_test_subscription_schema.dict())

    unsubscribe_token = test_subscription.unsubscribe_token
    generated_unsubscribe_token = test_subscription.generate_unsubscribe_token()

    assert unsubscribe_token != generated_unsubscribe_token
