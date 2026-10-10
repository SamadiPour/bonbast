"""Turn bonbast.com responses into models."""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping
from datetime import date
from typing import Any, TypeVar

from bs4 import BeautifulSoup

from .catalog import COINS, CURRENCIES, GOLDS, Unit
from .errors import ParseError
from .models import Coin, Currency, Gold, Prices

_TOKEN = re.compile(r"""\bparam\s*[:=]\s*["']([^"']+)["']""")
_GRAPH_LABELS = re.compile(r"\blabels\s*:\s*\[(.*?)\]", re.DOTALL)
_GRAPH_DATA = re.compile(r"\bdata\s*:\s*\[(.*?)\]", re.DOTALL)
_ISO_DATE = re.compile(r"\d{4}-\d{2}-\d{2}")
_NUMBER = re.compile(r"-?\d+(?:\.\d+)?")

# The JSON API suffixes currency codes with "1" for the sell and "2" for the buy price.
# Coins use their bare code for the sell price and the "2" suffix for the buy price.
_SELL, _BUY = "1", "2"

_T = TypeVar("_T", Currency, Coin)


def parse_token(html: str) -> str:
    """Extract the access token the home page embeds for its ``/json`` requests."""
    match = _TOKEN.search(html)
    if match is None:
        raise ParseError("could not find the access token on bonbast.com; the website may have changed")
    return match.group(1)


def parse_prices(data: Mapping[str, Any]) -> Prices:
    """Parse the payload of the ``/json`` endpoint."""
    currencies = []
    for code, info in CURRENCIES.items():
        sell_key, buy_key = f"{code.lower()}{_SELL}", f"{code.lower()}{_BUY}"
        if sell_key in data or buy_key in data:
            currencies.append(
                Currency(
                    code=code,
                    name=info.label,
                    sell=_int(data.get(sell_key)),
                    buy=_int(data.get(buy_key)),
                    quantity=info.quantity,
                )
            )

    coins = [
        Coin(code=code, name=name, sell=_int(data.get(code)), buy=_int(data.get(f"{code}{_BUY}")))
        for code, name in COINS.items()
        if code in data or f"{code}{_BUY}" in data
    ]

    golds = []
    for code, gold in GOLDS.items():
        if code in data:
            price = _number(data[code])
            if price is not None and gold.unit is Unit.TOMAN:
                price = round(price)
            golds.append(Gold(code=code, name=gold.name, price=price, unit=gold.unit))

    if not (currencies or coins or golds):
        raise ParseError("bonbast.com returned no prices; the website may have changed")

    updated_at = data.get("last_modified")
    return Prices(tuple(currencies), tuple(coins), tuple(golds), updated_at=str(updated_at) if updated_at else None)


def parse_archive(html: str) -> Prices:
    """Parse the ``/archive`` page, which lists the currency and coin prices of one day."""
    coin_codes = {_squash(name): code for code, name in COINS.items()}
    currencies: list[Currency] = []
    coins: list[Coin] = []

    for table in BeautifulSoup(html, "html.parser").find_all("table"):
        rows = [[cell.get_text(" ", strip=True) for cell in row.find_all(["td", "th"])] for row in table.find_all("tr")]
        if not rows or not rows[0]:
            continue
        kind = _squash(rows[0][0])

        for cells in rows[1:]:
            if kind == "code" and len(cells) >= 4 and cells[0].upper() in CURRENCIES:
                code = cells[0].upper()
                info = CURRENCIES[code]
                currencies.append(
                    Currency(code, info.label, sell=_int(cells[2]), buy=_int(cells[3]), quantity=info.quantity)
                )
            elif kind == "goldcoins" and len(cells) >= 3 and _squash(cells[0]) in coin_codes:
                code = coin_codes[_squash(cells[0])]
                coins.append(Coin(code, COINS[code], sell=_int(cells[1]), buy=_int(cells[2])))

    if not (currencies or coins):
        raise ParseError("bonbast.com returned no prices for this date; the website may have changed")

    return Prices(currencies=_in_catalog_order(currencies, CURRENCIES), coins=_in_catalog_order(coins, COINS))


def parse_graph(html: str) -> dict[date, int]:
    """Parse the chart on the ``/graph`` page into ``{day: sell price}``."""
    chart_start = html.find("new Chart(")
    chart = html[chart_start:] if chart_start != -1 else ""
    labels, values = _GRAPH_LABELS.search(chart), _GRAPH_DATA.search(chart)
    if labels is None or values is None:
        raise ParseError("could not find the chart data on bonbast.com; the website may have changed")

    try:
        days = [date.fromisoformat(day) for day in _ISO_DATE.findall(labels.group(1))]
    except ValueError as error:
        raise ParseError("bonbast.com returned invalid dates in the chart data") from error
    prices = [round(float(price)) for price in _NUMBER.findall(values.group(1))]

    if len(days) != len(prices):
        raise ParseError("bonbast.com returned inconsistent chart data")
    return dict(zip(days, prices))


def _number(value: Any) -> float | None:
    """Parse a price. bonbast.com uses 0 or blanks for prices it doesn't have."""
    try:
        number = float(str(value).replace(",", ""))
    except ValueError:
        return None
    return number if number > 0 else None


def _int(value: Any) -> int | None:
    number = _number(value)
    return None if number is None else round(number)


def _squash(text: str) -> str:
    """Lowercase and drop all whitespace, since the archive page spaces names inconsistently ("10Armenian Dram")."""
    return "".join(text.split()).lower()


def _in_catalog_order(items: Iterable[_T], catalog: Mapping[str, Any]) -> tuple[_T, ...]:
    order = {code: index for index, code in enumerate(catalog)}
    return tuple(sorted(items, key=lambda item: order[item.code]))
