import logging
from typing import ClassVar, List

from app.domain.Address import Address
from app.schemas.ListingSchema import ListingSchema
import pyap

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)  # Set the logging level


class Listing(ListingSchema):

    logger: ClassVar[logging.Logger] = logging.getLogger("app.domain.Listing")

    @staticmethod
    def parse_address(address: str, country: str | None = None) -> List[Address]:
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
        else:
            attribute_mapping = {
                "city": "city",
                "full_street": "street_address",
                "region1": "state",
                "country_id": "country",
                "postal_code": "postal_code",
            }
            final_addresses: List[Address] = []
            for new_address in addresses:
                temp_address = {}
                for source_attr, target_attr in attribute_mapping.items():
                    if hasattr(new_address, source_attr):
                        # setattr(temp_address, target_attr, getattr(new_address, source_attr))
                        temp_address[target_attr] = getattr(new_address, source_attr)

                final_addresses.append(Address(**temp_address))

            return final_addresses
