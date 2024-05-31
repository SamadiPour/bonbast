from __future__ import annotations

from rich.text import Text

try:
    from ..helpers.utils import *
    from ..helpers.currency_flags import *
except ImportError:
    from src.bonbast.helpers.utils import *
    from src.bonbast.helpers.currency_flags import *


class Currency:
    """
    Represents a currency with its code, name, sell, and buy prices.
    
    Attributes:
        code (str): The currency code.
        name (str): The currency name.
        sell (int): The sell price.
        buy (int): The buy price.
    """
    VALUES = {
        'usd': 'US Dollar',
        'eur': 'Euro',
        'gbp': 'British Pound',
        'chf': 'Swiss Franc',
        'cad': 'Canadian Dollar',
        'aud': 'Australian Dollar',
        'sek': 'Swedish Krona',
        'nok': 'Norwegian Krone',
        'rub': 'Russian Ruble',
        'thb': 'Thai Baht',
        'sgd': 'Singapore Dollar',
        'hkd': 'Hong Kong Dollar',
        'azn': 'Azerbaijani Manat',
        'amd': '10 Armenian Dram',
        'dkk': 'Danish Krone',
        'aed': 'UAE Dirham',
        'jpy': '10 Japanese Yen',
        'try': 'Turkish Lira',
        'cny': 'Chinese Yuan',
        'sar': 'Saudi Riyal',
        'inr': 'Indian Rupee',
        'myr': 'Malaysian Ringgit',
        'afn': 'Afghan Afghani',
        'kwd': 'Kuwaiti Dinar',
        'iqd': '100 Iraqi Dinar',
        'bhd': 'Bahraini Dinar',
        'omr': 'Omani Rial',
        'qar': 'Qatari Rial',
    }

    def __init__(self, code: str, name: str, sell: int, buy: int):
        """
        Initializes a new instance of the Currency class.

        :param code: The code of the currency.
        :param name: The name of the currency.
        :param sell: The sell price of the currency.
        :param buy: The buy price of the currency.
        """
        self.code = code
        self.name = name
        self.sell = sell
        self.buy = buy

    @property
    def formatted_buy(self) -> str:
        """Returns the buy price formatted as a string."""
        return format_toman(self.buy)

    @property
    def formatted_sell(self) -> str:
        """Returns the sell price formatted as a string."""
        return format_toman(self.sell)

    @property
    def flag(self) -> str:
        """Returns the flag emoji associated with the currency code."""
        return currency_flags[self.code.lower()]

    def to_json(self) -> dict:
        """Converts the currency instance to a JSON serializable dictionary."""
        return {
            self.code: {
                'name': self.name,
                'sell': self.sell,
                'buy': self.buy,
            }
        }

    def is_valid(self) -> bool:
        """Determines if the currency has valid sell or buy prices."""
        return (self.sell is not None and self.sell > 0) or (self.buy is not None and self.buy > 0)

    def assemble_simple_text(self, old_currency: Currency, with_flag: bool = False) -> Text:
        """
        Assembles a simple text representation of the currency.

        :param old_currency: An instance of Currency to compare with for changes.
        :param with_flag: Whether to include the flag emoji in the text.
        :return: A Text instance with the currency's information.
        """
        return Text.assemble(
            (f'{self.flag} ' if with_flag else '') + f'{self.code}: ',
            (f'{self.formatted_sell}', get_color(self.sell, old_currency.sell) if old_currency is not None else ''),
            ' / ',
            (f'{self.formatted_buy}', get_color(self.buy, old_currency.buy) if old_currency is not None else ''),
            '\n'
        )
