try:
    from ..utils import *
except ImportError:
    from src.bonbast.utils import *


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
