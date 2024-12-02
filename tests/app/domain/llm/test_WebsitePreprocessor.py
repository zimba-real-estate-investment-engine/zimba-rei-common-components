from app.domain.llm.WebsitePreprocessor import WebsitePreprocessor


def test_get_raw_text_from_html(test_sample_html):
    data_preprocessor = WebsitePreprocessor(html=test_sample_html)

    raw_text = data_preprocessor.get_raw_text()
    assert raw_text


def test_get_raw_text_from_url():
    data_processor = WebsitePreprocessor(url='http://cnn.com')

    raw_text = data_processor.get_raw_text()
    assert raw_text
