try:
    from .utils import *
except:
    from utils import *

PRICE_FORMATTER = "{:,}"


class Currency:
    """ Currency model
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
        self.code = code
        self.name = name
        self.sell = sell
        self.buy = buy

    @property
    def formatted_buy(self) -> str:
        return format_toman(self.buy)

    @property
    def formatted_sell(self) -> str:
        return format_toman(self.sell)

    def to_json(self) -> dict:
        return {
            self.code: {
                'name': self.name,
                'sell': self.sell,
                'buy': self.buy,
            }
        }


class Coin:
    """ Coin model
    """
    VALUES = {
        'emami1': 'Emami',
        'azadi1g': 'Gerami',
        'azadi1': 'Azadi',
        'azadi1_2': '½ Azadi',
        'azadi1_4': '¼ Azadi',
    }

    def __init__(self, code: str, name: str, sell: int, buy: int):
        self.code = code
        self.name = name
        self.sell = sell
        self.buy = buy

    @property
    def formatted_buy(self) -> str:
        return format_toman(self.buy)

    @property
    def formatted_sell(self) -> str:
        return format_toman(self.sell)

    def to_json(self) -> dict:
        return {
            self.code: {
                'name': self.name,
                'sell': self.sell,
                'buy': self.buy,
            }
        }


class Gold:
    """ Gold model
    """
    VALUES = {
        'mithqal': 'Gold Mithqal',
        'gol18': 'Gold Gram',
    }

    def __init__(self, code: str, name: str, price: float):
        self.code = code
        self.name = name
        self.price = price

    @property
    def formatted_price(self) -> str:
        return format_toman(self.price)

    def to_json(self) -> dict:
        return {
            self.code: {
                'name': self.name,
                'price': self.price,
            }
        }


class Graph:
    """ Graph model
    """

    def __init__(self, date: str, value: int, currency: str):
        self.date = date
        self.value = value
        self.currency = currency

    def to_json(self) -> dict:
        return {
            self.currency: {
                'date': self.date,
                'value': self.value,
            }
        }
