import io
from datetime import date, datetime

from rich.console import Console, RenderableType

from bonbast.catalog import Unit
from bonbast.models import Currency, Gold, Prices
from bonbast.render import Trend, TrendTracker, graph_view, simple_text, ticker_table


def _render(renderable: RenderableType) -> str:
    buffer = io.StringIO()
    Console(width=200, file=buffer).print(renderable)
    return buffer.getvalue()


def _usd(sell: int, buy: int = 1) -> Prices:
    return Prices(currencies=(Currency("USD", "US Dollar", sell, buy),))


def test_trend_between() -> None:
    assert Trend.between(1, 2) is Trend.UP
    assert Trend.between(2, 1) is Trend.DOWN
    assert Trend.between(1, 1) is Trend.FLAT
    assert Trend.between(None, 1) is None


def test_tracker_keeps_the_last_direction_through_flat_ticks() -> None:
    tracker = TrendTracker()
    tracker.update(_usd(100))
    assert tracker.get("USD", "sell") is None

    tracker.update(_usd(110))
    assert tracker.get("USD", "sell") is Trend.UP

    tracker.update(_usd(110))
    assert tracker.get("USD", "sell") is Trend.UP

    tracker.update(_usd(90))
    assert tracker.get("USD", "sell") is Trend.DOWN
    assert tracker.get("USD", "buy") is None


def test_simple_text_shows_arrows_for_changes() -> None:
    tracker = TrendTracker()
    tracker.update(_usd(100))
    tracker.update(_usd(110))
    prices = Prices(currencies=_usd(110).currencies, golds=(Gold("ounce", "Gold Ounce", 4100.5, Unit.USD),))

    text = simple_text(prices, tracker, timestamp=datetime(2026, 1, 2, 3, 4, 5)).plain

    assert text == "2026-01-02 03:04:05\n\nUSD: 110 ↑ / 1\nGold Ounce: $4,100.50"


def test_ticker_table_compares_with_the_previous_row() -> None:
    first, second = _usd(100).currencies[0], _usd(90).currencies[0]
    output = _render(ticker_table([(datetime(2026, 1, 1), first, None), (datetime(2026, 1, 1, 0, 0, 30), second, first)]))

    assert "90 ↓" in output and "1 -" in output


def test_graph_view() -> None:
    output = _render(graph_view("eur", {date(2026, 1, 1): 100, date(2026, 1, 2): 150, date(2026, 1, 3): 120}))

    assert "Euro (EUR)" in output
    assert "+50" in output and "-30" in output
    assert "Low 100  ·  High 150  ·  Average 123  ·  Change +20 (+20.00%)" in output


def test_graph_view_without_data() -> None:
    assert "no EUR prices" in _render(graph_view("eur", {}))
