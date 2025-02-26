from app.services.SubscriptionService import SubscriptionService


def test_save_subscription(get_test_db, get_test_subscription_schema):
    db = get_test_db
    test_subscription = get_test_subscription_schema

    subscription_service = SubscriptionService(db)

    newly_saved_subscription = subscription_service.save_subscription(test_subscription)

    # Make sure ID was successfully auto-incremented
    assert newly_saved_subscription.id and newly_saved_subscription.id != 0
    assert newly_saved_subscription.unsubscribe_token != test_subscription.unsubscribe_token  # Generated at saving

    # Clean up TBD

    db.commit() # Only commit if you want to actually save in db.
