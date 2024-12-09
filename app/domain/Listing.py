import logging
from typing import ClassVar, List, Any

import pycountry
from price_parser import Price

from app.domain.Address import Address
from app.domain.REIPrice import REIPrice
from app.schemas.ListingSchema import ListingSchema
import pyap

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)  # Set the logging level


class Listing(ListingSchema):
    logger: ClassVar[logging.Logger] = logging.getLogger("app.domain.Listing")

    def __init__(self, /, **data: Any):

        super().__init__(**data)

    @staticmethod
    def parse_address(address: str, country: str | None = None) -> List[Address]:
        final_addresses: List[Address] = []

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
            full_address_record = Address(full_address=address)
            final_addresses.append(full_address_record)
            return final_addresses
        else:
            attribute_mapping = {
                "city": "city",
                "full_street": "street_address",
                "region1": "state",
                "country_id": "country",
                "postal_code": "postal_code",
                "full_address": "full_address"
            }
            for new_address in addresses:
                temp_address = {}
                for source_attr, target_attr in attribute_mapping.items():
                    if hasattr(new_address, source_attr):
                        # setattr(temp_address, target_attr, getattr(new_address, source_attr))
                        temp_address[target_attr] = getattr(new_address, source_attr)

                final_addresses.append(Address(**temp_address))

            return final_addresses

    @staticmethod
    def parse_price_and_iso_currency(price_string: str) -> REIPrice:  # in future might move to PriceParser class

        try:
            parsed_price = Price.fromstring(price_string)

            currency_info = {
                'original': price_string,
                'amount': parsed_price.amount,
                'currency_symbol': parsed_price.currency,
                'currency_iso_code': None
            }

            if parsed_price:
                try:
                    symbol_to_currency = {
                        '$': 'USD',  # US Dollar
                        '€': 'EUR',  # Euro
                        '£': 'GBP',  # British Pound
                        '¥': 'JPY',  # Japanese Yen
                        '₹': 'INR',  # Indian Rupee
                        '₽': 'RUB',  # Russian Ruble
                        '₩': 'KRW',  # South Korean Won
                        'A$': 'AUD',  # Australian Dollar
                        'CA$': 'CAD',  # Canadian Dollar
                        'CAD$': 'CAD',  # Canadian Dollar
                        'USD': 'USD',  # US Dollar
                        'US$': 'USD',  # US Dollar
                        'EUR': 'EUR',  # Euro
                        'GBP': 'GBP',  # British Pound
                        'JPY': 'JPY',  # Japanese Yen
                        'INR': 'INR',  # Indian Rupee
                        'RUB': 'RUB',  # Russian Ruble
                        'KRW': 'KRW',  # South Korean Won
                        'AUD': 'AUD',  # Australian Dollar
                        'CAD': 'CAD'  # Canadian Dollar
                    }

                    if parsed_price.currency in symbol_to_currency:
                        currency_info['currency_iso_code'] = symbol_to_currency[parsed_price.currency]
                    else:
                        # If not in our symbol map, try to find currency by name or symbol
                        for currency in pycountry.currencies:
                            if (parsed_price.currency.lower() in currency.name.lower() or
                                    parsed_price.currency == currency.symbol):
                                currency_info['currency_iso_code'] = currency.alpha_3
                                break

                    final_value = REIPrice(**currency_info)
                    return final_value

                except Exception as e:
                    logging.error(f'Could not parse ISO Currency Code from {price_string}: {e}')

        except Exception as e:
            logging.error(f'Error parsing price string {price_string}: {e}')
