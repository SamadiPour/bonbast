try:
    from ..utils import *
except ImportError:
    from src.bonbast.utils import *


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
