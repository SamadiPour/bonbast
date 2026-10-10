"""Price models. All prices are in Toman unless a Gold's unit says otherwise."""

from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass, replace
from typing import Any, Union

from .catalog import Unit


@dataclass(frozen=True, slots=True)
class Quote:
    """Something bonbast.com quotes with separate sell and buy prices."""

    code: str
    name: str
    sell: int | None
    buy: int | None

    def is_valid(self) -> bool:
        return self.sell is not None or self.buy is not None

    def to_dict(self) -> dict[str, Any]:
        return _without_none({"name": self.name, "sell": self.sell, "buy": self.buy})


@dataclass(frozen=True, slots=True)
class Currency(Quote):
    # How many units of the currency the prices are for (e.g. 10 for Japanese Yen).
    quantity: int = 1


@dataclass(frozen=True, slots=True)
class Coin(Quote):
    pass


@dataclass(frozen=True, slots=True)
class Gold:
    """Gold (and Bitcoin) with a single price, in Toman or US Dollars."""

    code: str
    name: str
    price: int | float | None
    unit: Unit = Unit.TOMAN

    def is_valid(self) -> bool:
        return self.price is not None

    def to_dict(self) -> dict[str, Any]:
        return _without_none({"name": self.name, "price": self.price})


Asset = Union[Currency, Coin, Gold]


@dataclass(frozen=True, slots=True)
class Prices:
    """A snapshot of prices."""

    currencies: tuple[Currency, ...] = ()
    coins: tuple[Coin, ...] = ()
    golds: tuple[Gold, ...] = ()
    # When bonbast.com last changed the prices, as the website words it (Tehran time).
    updated_at: str | None = None

    def __iter__(self) -> Iterator[Asset]:
        yield from self.currencies
        yield from self.coins
        yield from self.golds

    def __len__(self) -> int:
        return len(self.currencies) + len(self.coins) + len(self.golds)

    def get(self, code: str) -> Asset | None:
        """Find an asset by its code, ignoring case."""
        code = code.lower()
        return next((asset for asset in self if asset.code.lower() == code), None)

    def only(self, codes: Iterable[str]) -> Prices:
        """Keep only the assets with the given codes, ignoring case."""
        wanted = {code.lower() for code in codes}
        return self._filter(lambda asset: asset.code.lower() in wanted)

    def valid(self) -> Prices:
        """Drop the assets bonbast.com has no price for."""
        return self._filter(lambda asset: asset.is_valid())

    def to_dict(self) -> dict[str, dict[str, Any]]:
        """The JSON shape ``bonbast export`` prints: ``{"USD": {"name": ..., "sell": ..., "buy": ...}, ...}``."""
        return {asset.code: asset.to_dict() for asset in self}

    def _filter(self, keep: Callable[[Asset], bool]) -> Prices:
        return replace(
            self,
            currencies=tuple(filter(keep, self.currencies)),
            coins=tuple(filter(keep, self.coins)),
            golds=tuple(filter(keep, self.golds)),
        )


def _without_none(values: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in values.items() if value is not None}
