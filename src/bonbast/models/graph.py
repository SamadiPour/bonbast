try:
    from ..helpers.utils import *
except ImportError:
    from src.bonbast.helpers.utils import *


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
