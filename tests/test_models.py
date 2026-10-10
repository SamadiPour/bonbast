from bonbast.catalog import Unit
from bonbast.models import Coin, Currency, Gold, Prices

PRICES = Prices(
    currencies=(Currency("USD", "US Dollar", 100, 99), Currency("EUR", "Euro", None, None)),
    coins=(Coin("emami1", "Emami", 1000, None),),
    golds=(Gold("ounce", "Gold Ounce", 4100.5, Unit.USD),),
)


def test_iteration_and_length() -> None:
    assert [asset.code for asset in PRICES] == ["USD", "EUR", "emami1", "ounce"]
    assert len(PRICES) == 4


def test_get_ignores_case() -> None:
    assert PRICES.get("usd") is PRICES.currencies[0]
    assert PRICES.get("OUNCE") is PRICES.golds[0]
    assert PRICES.get("nope") is None


def test_only() -> None:
    assert [asset.code for asset in PRICES.only({"usd", "Emami1"})] == ["USD", "emami1"]


def test_valid_drops_assets_without_prices() -> None:
    assert [asset.code for asset in PRICES.valid()] == ["USD", "emami1", "ounce"]


def test_to_dict_matches_the_export_format() -> None:
    assert PRICES.to_dict() == {
        "USD": {"name": "US Dollar", "sell": 100, "buy": 99},
        "EUR": {"name": "Euro"},
        "emami1": {"name": "Emami", "sell": 1000},
        "ounce": {"name": "Gold Ounce", "price": 4100.5},
    }
