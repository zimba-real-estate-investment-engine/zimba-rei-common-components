import logging
from typing import ClassVar

from app.schemas.ListingSchema import ListingSchema
import pyap

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)  # Set the logging level


class Listing(ListingSchema):

    logger: ClassVar[logging.Logger] = logging.getLogger("app.domain.Listing")

    @staticmethod
    def parse_address(address: str, country: str | None = None):
        if country in ['US', 'CA']:
            addresses = pyap.parse(address, country=country)
        elif country is None:
            canadian_addresses = pyap.parse(address, country="CA")
            us_addresses = pyap.parse(address, country="US")
            addresses = canadian_addresses + us_addresses
        else:
            logging.error(f'Incorrect country specified {country}')
            raise ValueError(f'Incorrect country specified {country}')

        if len(addresses) == 0:
            logging.error(f'Address could not be parsed: {address}')

        return addresses
