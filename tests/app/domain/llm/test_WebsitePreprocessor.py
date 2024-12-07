from app.domain.llm.WebsitePreprocessor import WebsitePreprocessor


def test_get_raw_text_from_html(test_sample_html):
    data_preprocessor = WebsitePreprocessor(html=test_sample_html)

    raw_text = data_preprocessor.get_raw_text()
    assert raw_text


def test_get_raw_text_from_url():
    data_processor = WebsitePreprocessor(url='http://cnn.com')

    raw_text = data_processor.get_raw_text()
    assert raw_text


def test_get_html():
    website_processor = WebsitePreprocessor(url='http://cnn.com')
    html = website_processor.get_html()
    assert 'cnn.com' in html


def test__load_user_agents():
    website_processor = WebsitePreprocessor()
    assert website_processor._load_user_agents()
    assert website_processor.user_agents


def test__get_random_headers():
    website_processor = WebsitePreprocessor()
    first_random_headers = website_processor._get_random_headers()
    assert first_random_headers
    assert website_processor.headers

    # Also test that the values returned are random
    second_random_headers = website_processor._get_random_headers()
    assert first_random_headers != second_random_headers


# Created some static methods for comparison
def test_get_random_headers():
    first_random_headers = WebsitePreprocessor.get_random_headers()
    assert first_random_headers

    # Also test that the values returned are random
    second_random_headers = WebsitePreprocessor.get_random_headers()
    assert first_random_headers != second_random_headers


def test_load_user_agents():
    loaded_agents_list = WebsitePreprocessor.load_user_agents()
    assert loaded_agents_list


def test_get_text_from_url():
    website_processor = WebsitePreprocessor(url='http://cnn.com')
    html = WebsitePreprocessor.get_text_from_url(url='http://cnn.com')
    assert 'cnn.com' in html
