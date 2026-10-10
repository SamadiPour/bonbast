"""Rich renderables for the terminal output."""

from __future__ import annotations

import math
from collections.abc import Iterable, Mapping, Sequence
from datetime import date, datetime
from enum import IntEnum

from rich import box
from rich.console import Group, RenderableType
from rich.table import Table
from rich.text import Text

from .catalog import CURRENCIES, Unit
from .models import Asset, Coin, Currency, Gold, Prices

LABEL_STYLE = "cyan"
BAR_WIDTH = 30


class Trend(IntEnum):
    DOWN = -1
    FLAT = 0
    UP = 1

    @classmethod
    def between(cls, old: float | None, new: float | None) -> Trend | None:
        if old is None or new is None:
            return None
        return cls((new > old) - (new < old))

    @property
    def style(self) -> str:
        return {Trend.UP: "green", Trend.DOWN: "red"}.get(self, "")

    @property
    def arrow(self) -> str:
        return {Trend.UP: "↑", Trend.DOWN: "↓", Trend.FLAT: "-"}[self]


class TrendTracker:
    """Remembers which way each price last moved, so live views stay coloured until the next change."""

    def __init__(self) -> None:
        self._last: dict[tuple[str, str], float] = {}
        self._trends: dict[tuple[str, str], Trend] = {}

    def update(self, prices: Prices) -> None:
        for asset in prices:
            for field, value in price_fields(asset):
                if value is None:
                    continue
                key = (asset.code, field)
                trend = Trend.between(self._last.get(key), value)
                if trend:  # a flat tick keeps the previous direction
                    self._trends[key] = trend
                self._last[key] = value

    def get(self, code: str, field: str) -> Trend | None:
        return self._trends.get((code, field))


def price_fields(asset: Asset) -> tuple[tuple[str, float | None], ...]:
    if isinstance(asset, Gold):
        return (("price", asset.price),)
    return (("sell", asset.sell), ("buy", asset.buy))


def format_value(asset: Asset, value: float | None) -> str:
    if value is None:
        return "-"
    if isinstance(asset, Gold) and asset.unit is Unit.USD:
        return f"${value:,.2f}"
    return f"{value:,}"


def format_amount(value: float) -> str:
    return f"{value:,.2f}"


def prices_view(prices: Prices, trends: TrendTracker | None = None, *, title: str | None = None) -> RenderableType:
    """The currencies, coins and gold tables, as the main command shows them."""
    tables = [
        table
        for table in (
            currencies_table(prices.currencies, trends),
            coins_table(prices.coins, trends),
            golds_table(prices.golds, trends),
        )
        if table is not None
    ]
    if not tables:
        return Text("No prices to show.", style="yellow")

    footer = "Prices are in Toman (1 Toman = 10 Rials) unless marked with $."
    if prices.updated_at:
        footer += f" Updated {prices.updated_at} (Tehran)."
    parts: list[RenderableType] = [Text(title, style="bold")] if title else []
    return Group(*parts, *tables, Text(footer, style="dim"))


def currencies_table(
    currencies: Sequence[Currency], trends: TrendTracker | None = None, *, columns: int = 2
) -> RenderableType | None:
    if not currencies:
        return None
    if len(currencies) < 6:
        columns = 1

    size = math.ceil(len(currencies) / columns)
    parts = [currencies[index : index + size] for index in range(0, len(currencies), size)]

    grid = Table.grid(padding=(0, 4))
    grid.title = "Currencies"
    for _ in parts:
        grid.add_column()
    grid.add_row(*(_currency_part(part, trends) for part in parts))
    return grid


def _currency_part(currencies: Sequence[Currency], trends: TrendTracker | None) -> Table:
    table = Table()
    table.add_column("Code", style=LABEL_STYLE, no_wrap=True)
    table.add_column("Currency", style=LABEL_STYLE)
    table.add_column("Sell", justify="right", no_wrap=True)
    table.add_column("Buy", justify="right", no_wrap=True)
    for currency in currencies:
        table.add_row(currency.code, currency.name, *_price_cells(currency, trends))
    return table


def coins_table(coins: Sequence[Coin], trends: TrendTracker | None = None) -> Table | None:
    if not coins:
        return None
    table = Table(title="Coins")
    table.add_column("Coin", style=LABEL_STYLE)
    table.add_column("Sell", justify="right", no_wrap=True)
    table.add_column("Buy", justify="right", no_wrap=True)
    for coin in coins:
        table.add_row(coin.name, *_price_cells(coin, trends))
    return table


def golds_table(golds: Sequence[Gold], trends: TrendTracker | None = None) -> Table | None:
    if not golds:
        return None
    table = Table(title="Gold")
    table.add_column("Gold", style=LABEL_STYLE)
    table.add_column("Price", justify="right", no_wrap=True)
    for gold in golds:
        table.add_row(gold.name, *_price_cells(gold, trends))
    return table


def simple_text(prices: Prices, trends: TrendTracker | None = None, *, timestamp: datetime | None = None) -> Text:
    """One line per asset, for ``bonbast live simple``."""
    text = Text()
    if timestamp is not None:
        text.append(f"{timestamp:%Y-%m-%d %H:%M:%S}\n\n", style="bold")
    for asset in prices:
        text.append(f"{asset.code if isinstance(asset, Currency) else asset.name}: ")
        text.append_text(Text(" / ").join(_price_cells(asset, trends)))
        text.append("\n")
    text.rstrip()
    return text


def ticker_table(rows: Iterable[tuple[datetime, Asset, Asset | None]]) -> Table:
    """One row per refresh of a single asset, for ``bonbast live currency``.

    Each row is ``(time, asset, the asset at the previous refresh)``.
    """
    rows = list(rows)
    table = Table()
    table.add_column("Date", style=LABEL_STYLE, no_wrap=True)
    table.add_column("Name", style=LABEL_STYLE, no_wrap=True)
    if rows and isinstance(rows[0][1], Gold):
        table.add_column("Price", justify="right", no_wrap=True)
    else:
        table.add_column("Sell", justify="right", no_wrap=True)
        table.add_column("Buy", justify="right", no_wrap=True)

    for when, asset, previous in rows:
        old = dict(price_fields(previous)) if previous is not None else {}
        cells = []
        for field, value in price_fields(asset):
            trend = Trend.between(old.get(field), value)
            text = format_value(asset, value)
            cells.append(Text(f"{text} {trend.arrow}", style=trend.style) if trend is not None else Text(text))
        table.add_row(f"{when:%Y-%m-%d %H:%M:%S}", asset.name, *cells)
    return table


def graph_view(currency: str, points: Mapping[date, int]) -> RenderableType:
    """A table of daily prices with a bar for each day, for ``bonbast graph``."""
    code = currency.upper()
    if not points:
        return Text(f"bonbast.com has no {code} prices for this range.", style="yellow")

    values = list(points.values())
    low, high = min(values), max(values)
    table = Table(title=f"{CURRENCIES[code].label} ({code}) sell price in Toman", box=box.SIMPLE_HEAD)
    table.add_column("Date", style=LABEL_STYLE, no_wrap=True)
    table.add_column("Price", justify="right", no_wrap=True)
    table.add_column("Change", justify="right", no_wrap=True)
    table.add_column("", no_wrap=True)

    previous: int | None = None
    for day, value in points.items():
        trend = Trend.between(previous, value)
        style = trend.style if trend is not None else ""
        change = f"{value - previous:+,}" if previous is not None else ""
        table.add_row(
            day.isoformat(),
            f"{value:,}",
            Text(change, style=style),
            Text("█" * _bar(value, low, high), style=style or LABEL_STYLE),
        )
        previous = value

    first, last = values[0], values[-1]
    summary = f"Low {low:,}  ·  High {high:,}  ·  Average {round(sum(values) / len(values)):,}  ·  Change {last - first:+,}"
    if first:
        summary += f" ({(last - first) / first:+.2%})"
    return Group(table, Text(summary, style="dim"))


def _bar(value: float, low: float, high: float) -> int:
    if high == low:
        return BAR_WIDTH
    return 1 + round((value - low) / (high - low) * (BAR_WIDTH - 1))


def _price_cells(asset: Asset, trends: TrendTracker | None) -> list[Text]:
    cells = []
    for field, value in price_fields(asset):
        text = format_value(asset, value)
        trend = trends.get(asset.code, field) if trends is not None else None
        cells.append(Text(f"{text} {trend.arrow}", style=trend.style) if trend else Text(text))
    return cells
