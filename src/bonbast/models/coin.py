try:
    from ..utils import *
except ImportError:
    from src.bonbast.utils import *


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
