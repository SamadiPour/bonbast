from __future__ import annotations

from rich.text import Text

try:
    from ..helpers.utils import *
except ImportError:
    from src.bonbast.helpers.utils import *


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

    def assemble_simple_text(self, old_coin: Coin, **kwargs) -> Text:
        return Text.assemble(
            f'{self.name}: ',
            (f'{self.formatted_sell}', get_color(self.sell, old_coin.sell) if old_coin is not None else ''),
            ' / ',
            (f'{self.formatted_buy}', get_color(self.buy, old_coin.buy) if old_coin is not None else ''),
            '\n'
        )
