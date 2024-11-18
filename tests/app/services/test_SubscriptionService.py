from app.services.SubscriptionService import SubscriptionService


def test_save_subscription(get_test_db, get_test_subscription_schema):
    db = get_test_db
    tests_subscription = get_test_subscription_schema

    subscription_service = SubscriptionService(db)

    newly_saved_subscription = subscription_service.save_subscription(tests_subscription)

    # db.commit() Only commit if you want to actually save in db.
    assert newly_saved_subscription.unsubscribe_token == tests_subscription.unsubscribe_token
