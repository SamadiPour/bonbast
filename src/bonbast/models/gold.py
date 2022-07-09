from __future__ import annotations

from rich.text import Text

try:
    from ..helpers.utils import *
except ImportError:
    from src.bonbast.helpers.utils import *


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

    def assemble_simple_text(self, old_gold: Gold, **kwargs) -> Text:
        return Text.assemble(
            f'{self.code}: ',
            (f'{self.price}', get_color(self.price, old_gold.price) if old_gold is not None else ''),
            '\n'
        )
