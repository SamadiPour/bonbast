from __future__ import annotations

from rich.text import Text

try:
    from ..helpers.utils import *
except ImportError:
    from src.bonbast.helpers.utils import *


class Coin:
    """Represents a coin with its code, name, sell, and buy prices."""
    
    VALUES = {
        'emami1': 'Emami',
        'azadi1g': 'Gerami',
        'azadi1': 'Azadi',
        'azadi1_2': '½ Azadi',
        'azadi1_4': '¼ Azadi',
    }

    def __init__(self, code: str, name: str, sell: int, buy: int):
        """
        Initializes a new instance of the Coin class.

        :param code: The code of the coin.
        :param name: The name of the coin.
        :param sell: The sell price of the coin.
        :param buy: The buy price of the coin.
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

    def to_json(self) -> dict:
        """Converts the coin instance to a JSON serializable dictionary."""
        return {
            self.code: {
                'name': self.name,
                'sell': self.sell,
                'buy': self.buy,
            }
        }

    def is_valid(self) -> bool:
        """Determines if the coin has valid sell or buy prices."""
        return (self.sell is not None and self.sell > 0) or (self.buy is not None and self.buy > 0)

    def assemble_simple_text(self, old_coin: Coin, **kwargs) -> Text:
        """
        Assembles a simple text representation of the coin.

        :param old_coin: An instance of Coin to compare with for changes.
        :return: A Text instance with the coin's information.
        """
        return Text.assemble(
            f'{self.name}: ',
            (f'{self.formatted_sell}', get_color(self.sell, old_coin.sell) if old_coin is not None else ''),
            ' / ',
            (f'{self.formatted_buy}', get_color(self.buy, old_coin.buy) if old_coin is not None else ''),
            '\n'
        )
