"""Gold prices and Iranian Rial exchange rates from bonbast.com."""

from importlib.metadata import PackageNotFoundError, version

from .client import BonbastClient
from .errors import BonbastError, InvalidDateError, NetworkError, ParseError
from .models import Coin, Currency, Gold, Prices

try:
    __version__ = version("bonbast")
except PackageNotFoundError:  # running from a source tree that was never installed
    __version__ = "0.0.0"

__all__ = [
    "BonbastClient",
    "BonbastError",
    "Coin",
    "Currency",
    "Gold",
    "InvalidDateError",
    "NetworkError",
    "ParseError",
    "Prices",
    "__version__",
]
