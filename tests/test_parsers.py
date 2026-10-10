from datetime import date

import pytest

from bonbast.catalog import COINS, CURRENCIES, Unit
from bonbast.errors import ParseError
from bonbast.parsers import parse_archive, parse_graph, parse_prices, parse_token

from .conftest import TOKEN, fixture_json, fixture_text


def test_parse_token() -> None:
    assert parse_token(fixture_text("home.html")) == TOKEN


def test_parse_token_missing() -> None:
    with pytest.raises(ParseError):
        parse_token("<html></html>")


def test_parse_prices() -> None:
    prices = parse_prices(fixture_json("prices.json"))

    assert [currency.code for currency in prices.currencies] == list(CURRENCIES)
    assert [coin.code for coin in prices.coins] == list(COINS)
    assert prices.updated_at == "October 04, 2026 18:15"

    usd = prices.get("usd")
    assert usd is not None and (usd.name, usd.sell, usd.buy) == ("US Dollar", 269300, 269200)

    jpy = prices.get("JPY")
    assert jpy is not None and (jpy.name, jpy.quantity) == ("10 Japanese Yen", 10)

    emami = prices.get("emami1")
    assert emami is not None and (emami.sell, emami.buy) == (271000000, 267000000)


def test_parse_prices_golds_keep_their_units() -> None:
    golds = {gold.code: gold for gold in parse_prices(fixture_json("prices.json")).golds}

    assert golds["mithqal"].price == 114370000 and isinstance(golds["mithqal"].price, int)
    assert golds["mithqal"].unit is Unit.TOMAN
    assert golds["ounce"].price == 4140.61 and golds["ounce"].unit is Unit.USD
    assert golds["bitcoin"].price == 85301.36


def test_parse_prices_treats_zero_and_blank_as_missing() -> None:
    prices = parse_prices({"usd1": "0", "usd2": "", "eur1": "1,234", "mithqal": "abc"})

    usd, eur = prices.currencies
    assert (usd.sell, usd.buy) == (None, None) and not usd.is_valid()
    assert (eur.sell, eur.buy) == (1234, None) and eur.is_valid()
    assert prices.golds[0].price is None


def test_parse_prices_without_known_keys() -> None:
    with pytest.raises(ParseError):
        parse_prices({"something": "else"})


def test_parse_archive() -> None:
    prices = parse_archive(fixture_text("archive.html"))

    assert [currency.code for currency in prices.currencies] == list(CURRENCIES)
    assert [coin.code for coin in prices.coins] == list(COINS)
    assert prices.golds == ()

    usd = prices.get("USD")
    assert usd is not None and (usd.sell, usd.buy) == (215900, 215800)
    amd = prices.get("amd")
    assert amd is not None and amd.name == "10 Armenian Dram"
    half = prices.get("azadi1_2")
    assert half is not None and (half.name, half.sell, half.buy) == ("½ Azadi", 113500000, 111500000)


def test_parse_archive_without_tables() -> None:
    with pytest.raises(ParseError):
        parse_archive("<html><body>Nothing here</body></html>")


def test_parse_graph() -> None:
    points = parse_graph(fixture_text("graph.html"))

    assert list(points) == [date(2026, 9, day) for day in range(1, 10)]
    assert points[date(2026, 9, 1)] == 215900
    assert points[date(2026, 9, 9)] == 235500


def test_parse_graph_empty_range() -> None:
    html = "<script>new Chart(ctx, {data: {labels: [], datasets: [{data: []}]}});</script>"
    assert parse_graph(html) == {}


def test_parse_graph_mismatched_lengths() -> None:
    html = "<script>new Chart(ctx, {data: {labels: [new Date('2026-09-01')], datasets: [{data: [1, 2]}]}});</script>"
    with pytest.raises(ParseError):
        parse_graph(html)


def test_parse_graph_without_chart() -> None:
    with pytest.raises(ParseError):
        parse_graph("<html></html>")
