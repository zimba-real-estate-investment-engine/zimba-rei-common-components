from app.domain.UnderwritingProcess import UnderwritingProcess


def test_extract_listing_from_url():
    listing = UnderwritingProcess.extract_listing_from_url(
        "https://www.compass.com/listing/380-harrison-avenue-unit-1108-boston-ma-02118/1725626025069056057/")
    assert listing