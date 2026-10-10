"""Everything bonbast.com publishes, in the order the website lists it."""

from __future__ import annotations

from enum import Enum
from typing import NamedTuple


class Unit(str, Enum):
    """The currency a price is quoted in."""

    TOMAN = "toman"
    USD = "usd"


class CurrencyInfo(NamedTuple):
    name: str
    # bonbast.com quotes a few low-value currencies per 10 or 100 units.
    quantity: int = 1

    @property
    def label(self) -> str:
        return f"{self.quantity} {self.name}" if self.quantity > 1 else self.name


class GoldInfo(NamedTuple):
    name: str
    unit: Unit


CURRENCIES: dict[str, CurrencyInfo] = {
    "USD": CurrencyInfo("US Dollar"),
    "EUR": CurrencyInfo("Euro"),
    "GBP": CurrencyInfo("British Pound"),
    "CHF": CurrencyInfo("Swiss Franc"),
    "CAD": CurrencyInfo("Canadian Dollar"),
    "AUD": CurrencyInfo("Australian Dollar"),
    "SEK": CurrencyInfo("Swedish Krona"),
    "NOK": CurrencyInfo("Norwegian Krone"),
    "RUB": CurrencyInfo("Russian Ruble"),
    "THB": CurrencyInfo("Thai Baht"),
    "SGD": CurrencyInfo("Singapore Dollar"),
    "HKD": CurrencyInfo("Hong Kong Dollar"),
    "AZN": CurrencyInfo("Azerbaijani Manat"),
    "AMD": CurrencyInfo("Armenian Dram", quantity=10),
    "DKK": CurrencyInfo("Danish Krone"),
    "AED": CurrencyInfo("UAE Dirham"),
    "JPY": CurrencyInfo("Japanese Yen", quantity=10),
    "TRY": CurrencyInfo("Turkish Lira"),
    "CNY": CurrencyInfo("Chinese Yuan"),
    "SAR": CurrencyInfo("Saudi Riyal"),
    "INR": CurrencyInfo("Indian Rupee"),
    "MYR": CurrencyInfo("Malaysian Ringgit"),
    "AFN": CurrencyInfo("Afghan Afghani"),
    "KWD": CurrencyInfo("Kuwaiti Dinar"),
    "IQD": CurrencyInfo("Iraqi Dinar", quantity=100),
    "BHD": CurrencyInfo("Bahraini Dinar"),
    "OMR": CurrencyInfo("Omani Rial"),
    "QAR": CurrencyInfo("Qatari Riyal"),
}

COINS: dict[str, str] = {
    "emami1": "Emami",
    "azadi1g": "Gerami",
    "azadi1": "Azadi",
    "azadi1_2": "½ Azadi",
    "azadi1_4": "¼ Azadi",
}

GOLDS: dict[str, GoldInfo] = {
    "mithqal": GoldInfo("Gold Mithqal", Unit.TOMAN),
    "gol18": GoldInfo("Gold Gram", Unit.TOMAN),
    "ounce": GoldInfo("Gold Ounce", Unit.USD),
    "bitcoin": GoldInfo("Bitcoin", Unit.USD),
}

ALL_CODES: frozenset[str] = frozenset(code.lower() for code in (*CURRENCIES, *COINS, *GOLDS))
