from app.domain.Subscription import Subscription


def test_init_from_schema(get_test_subscription_schema):
    test_subscription = get_test_subscription_schema
    subscription = Subscription(**test_subscription.dict())
    assert subscription.service_subscribed_to == test_subscription.service_subscribed_to


def test_generate_unsubscribe_token(get_test_subscription_schema):
    test_subscription = Subscription(**get_test_subscription_schema.dict())

    before_setting_unsubscribe_token = test_subscription.unsubscribe_token
    test_subscription.set_unsubscribe_token()

    generated_unsubscribe_token = test_subscription.generate_unsubscribe_token()

    assert before_setting_unsubscribe_token != generated_unsubscribe_token

def test_generate_html_body():
    html_body = Subscription.generate_html_message_body()
    formatted_string = html_body.format(recipient_name='testname',
                              unsubscribe_api_endpoint='http://example.com:8080',
                              unsubscribe_token='unsubscribe_token')
    assert formatted_string