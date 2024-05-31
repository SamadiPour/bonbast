try:
    from ..helpers.utils import *
except ImportError:
    from src.bonbast.helpers.utils import *


class Graph:
    """Represents a graph model for currency value over time.

    Attributes:
        date (str): The date of the data point.
        value (int): The value of the currency at the given date.
        currency (str): The currency code.
    """

    def __init__(self, date: str, value: int, currency: str):
        """Initializes a new instance of the Graph class.

        Args:
            date (str): The date of the data point.
            value (int): The value of the currency at the given date.
            currency (str): The currency code.
        """
        self.date = date
        self.value = value
        self.currency = currency

    def to_json(self) -> dict:
        """Converts the Graph instance to a JSON serializable dictionary.

        Returns:
            dict: A dictionary representation of the Graph instance.
        """
        return {
            self.currency: {
                'date': self.date,
                'value': self.value,
            }
        }
