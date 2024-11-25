from app.services.EmailService import EmailService


def test_get_ses_client():
    ses_client = EmailService.get_ses_client()
    quota_response = ses_client.get_send_quota()
    assert 'Max24HourSend' in quota_response  # confirms user is authenticated and has permission
    assert 'SentLast24Hours' in quota_response

    identities_response = ses_client.list_identities()
    assert 'rei@zimbasolutions.io' in identities_response['Identities']   # ensure email is validated
    assert 'rei.zimbasolutions.io' in identities_response['Identities']   # ensure domain is validated


def test_send_email(get_test_email_schema):
    response = EmailService.send_email(get_test_email_schema)
    assert response['MessageId']
