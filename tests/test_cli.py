import json
from collections.abc import Callable
from datetime import timedelta

import pytest
import responses
from click.testing import CliRunner, Result
from rich.console import Console

import bonbast
from bonbast import cli as cli_module
from bonbast.cli import cli
from bonbast.client import BASE_URL, BonbastClient, tehran_today

Invoke = Callable[..., Result]


@pytest.fixture(autouse=True)
def _wide_console(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(cli_module, "console", Console(width=200))


@pytest.fixture
def invoke(client: BonbastClient) -> Invoke:
    def run(*args: str) -> Result:
        return CliRunner().invoke(cli, list(args), obj=client)

    return run


def test_version(invoke: Invoke) -> None:
    result = invoke("--version")
    assert result.exit_code == 0
    assert result.output.strip() == bonbast.__version__


def test_main_view(site: responses.RequestsMock, invoke: Invoke) -> None:
    result = invoke()

    assert result.exit_code == 0, result.output
    for text in ("Currencies", "US Dollar", "269,300", "½ Azadi", "Gold Ounce", "$4,140.61", "October 04, 2026 18:15"):
        assert text in result.output


def test_main_view_show_only(site: responses.RequestsMock, invoke: Invoke) -> None:
    result = invoke("--show-only", "usd,mithqal")

    assert result.exit_code == 0, result.output
    assert "US Dollar" in result.output and "Gold Mithqal" in result.output
    assert "Euro" not in result.output and "Coins" not in result.output


def test_export(site: responses.RequestsMock, invoke: Invoke) -> None:
    result = invoke("export")

    assert result.exit_code == 0, result.output
    data = json.loads(result.output)
    assert len(data) == 37
    assert data["USD"] == {"name": "US Dollar", "sell": 269300, "buy": 269200}
    assert data["azadi1_2"] == {"name": "½ Azadi", "sell": 142000000, "buy": 138000000}
    assert data["mithqal"] == {"name": "Gold Mithqal", "price": 114370000}


def test_export_show_only_strips_quotes_and_spaces(site: responses.RequestsMock, invoke: Invoke) -> None:
    result = invoke("export", "--show-only", "'USD, emami1'")

    assert result.exit_code == 0, result.output
    assert set(json.loads(result.output)) == {"USD", "emami1"}


def test_export_pretty_is_valid_json(site: responses.RequestsMock, invoke: Invoke) -> None:
    result = invoke("export", "--pretty", "--expanded", "--show-only", "usd")

    assert result.exit_code == 0, result.output
    assert json.loads(result.output) == {"USD": {"name": "US Dollar", "sell": 269300, "buy": 269200}}


def test_unknown_codes_are_rejected(invoke: Invoke) -> None:
    result = invoke("export", "--show-only", "usd,usdd")

    assert result.exit_code == 2
    assert "unknown code(s) usdd" in result.output


@pytest.mark.parametrize(
    ("args", "expected"),
    [
        (["-s", "usd", "10"], "2,692,000 / 2,693,000"),
        (["-s", "EUR", "12.5", "--only-sell"], "3,790,000"),
        (["-s", "jpy", "1000"], "1,695,000 / 1,705,000"),
        (["-d", "usd", "1837850"], "6.82 / 6.83"),
        (["-d", "iqd", "20600", "--only-buy"], "100.00"),
    ],
)
def test_convert(site: responses.RequestsMock, invoke: Invoke, args: list[str], expected: str) -> None:
    result = invoke("convert", *args)

    assert result.exit_code == 0, result.output
    assert result.output.strip() == expected


@pytest.mark.parametrize(
    "args",
    [["10"], ["-s", "usd", "-d", "eur", "10"], ["-s", "usd", "--only-buy", "--only-sell", "10"]],
)
def test_convert_usage_errors(invoke: Invoke, args: list[str]) -> None:
    assert invoke("convert", *args).exit_code == 2


def test_history_table(site: responses.RequestsMock, invoke: Invoke) -> None:
    day = tehran_today() - timedelta(days=3)
    result = invoke("history", "--date", day.strftime("%Y/%m/%d"))

    assert result.exit_code == 0, result.output
    assert f"Prices on {day.isoformat()}" in result.output
    assert "215,900" in result.output and "¼ Azadi" in result.output


def test_history_json_uses_the_export_format(site: responses.RequestsMock, invoke: Invoke) -> None:
    day = tehran_today() - timedelta(days=3)
    result = invoke("history", "-d", day.isoformat(), "--json", "--show-only", "usd,azadi1_2")

    assert result.exit_code == 0, result.output
    assert json.loads(result.output) == {
        "USD": {"name": "US Dollar", "sell": 215900, "buy": 215800},
        "azadi1_2": {"name": "½ Azadi", "sell": 113500000, "buy": 111500000},
    }


def test_history_rejects_today(invoke: Invoke) -> None:
    result = invoke("history", "--date", tehran_today().isoformat())

    assert result.exit_code == 1
    assert result.output.startswith("Error: date must be between")


def test_graph_table(site: responses.RequestsMock, invoke: Invoke) -> None:
    result = invoke("graph", "usd")

    assert result.exit_code == 0, result.output
    assert "US Dollar (USD)" in result.output
    assert "2026-09-09" in result.output and "+6,400" in result.output
    assert "Low 215,900" in result.output and "High 235,500" in result.output


def test_graph_json(site: responses.RequestsMock, invoke: Invoke) -> None:
    result = invoke("graph", "usd", "--json")

    assert result.exit_code == 0, result.output
    data = json.loads(result.output)
    assert data["2026-09-01"] == 215900 and len(data) == 9


def test_graph_rejects_inverted_ranges(invoke: Invoke) -> None:
    result = invoke("graph", "usd", "--start-date", "2024-02-01", "--end-date", "2024-01-01")

    assert result.exit_code == 1
    assert "start date must not be after the end date" in result.output


def test_network_errors_are_one_line_messages(http: responses.RequestsMock, invoke: Invoke) -> None:
    http.get(f"{BASE_URL}/", status=503)

    result = invoke("export")

    assert result.exit_code == 1
    assert result.output == "Error: bonbast.com responded with HTTP 503\n"
