from __future__ import annotations

from rich.text import Text

try:
    from ..helpers.utils import *
except ImportError:
    from src.bonbast.helpers.utils import *


class Gold:
    """
    Represents a gold item with its code, name, and price.

    Attributes:
        code (str): The code of the gold item.
        name (str): The name of the gold item.
        price (float): The price of the gold item.
    """
    VALUES = {
        'mithqal': 'Gold Mithqal',
        'gol18': 'Gold Gram',
        'ounce': 'Ounce',
        'bitcoin': 'Bitcoin',
    }

    def __init__(self, code: str, name: str, price: float):
        """
        Initializes a new instance of the Gold class.

        :param code: The code of the gold item.
        :param name: The name of the gold item.
        :param price: The price of the gold item.
        """
        self.code = code
        self.name = name
        self.price = price

    @property
    def price(self):
        """
        Gets the price of the gold item, formatted based on its code.

        :return: The price of the gold item.
        """
        if self.code in ['mithqal', 'gol18']:
            return int(self._price)
        else:
            return self._price

    @price.setter
    def price(self, value):
        """
        Sets the price of the gold item.

        :param value: The new price of the gold item.
        """
        self._price = value

    @property
    def formatted_price(self) -> str:
        """
        Gets the formatted price of the gold item.

        :return: The formatted price of the gold item.
        """
        return format_toman(self.price)

    def to_json(self) -> dict:
        """
        Converts the gold item instance to a JSON serializable dictionary.

        :return: A dictionary representation of the gold item.
        """
        return {
            self.code: {
                'name': self.name,
                'price': self.price,
            }
        }

    def is_valid(self) -> bool:
        """
        Determines if the gold item has a valid price.

        :return: True if the gold item has a valid price, False otherwise.
        """
        return self.price is not None and self.price > 0

    def assemble_simple_text(self, old_gold: Gold, **kwargs) -> Text:
        """
        Assembles a simple text representation of the gold item.

        :param old_gold: An instance of Gold to compare with for changes.
        :return: A Text instance with the gold item's information.
        """
        return Text.assemble(
            f'{self.code}: ',
            (f'{self.price}', get_color(self.price, old_gold.price) if old_gold is not None else ''),
            '\n'
        )
