from datetime import timedelta
from pathlib import Path

import pytest
import requests
import responses
from responses import matchers

from bonbast.client import BASE_URL, FIRST_ARCHIVE_DATE, BonbastClient, tehran_today
from bonbast.errors import InvalidDateError, NetworkError, ParseError
from bonbast.token_cache import TokenCache

from .conftest import TOKEN, fixture_json, fixture_text


def _calls(http: responses.RequestsMock, method: str, path: str) -> int:
    return sum(1 for call in http.calls if call.request.method == method and call.request.url == BASE_URL + path)


def test_prices(site: responses.RequestsMock, client: BonbastClient) -> None:
    prices = client.prices()

    assert len(prices.currencies) == 28
    json_request = next(call.request for call in site.calls if call.request.url == f"{BASE_URL}/json")
    assert json_request.headers["X-Requested-With"] == "XMLHttpRequest"
    assert json_request.body == "param=fef9596724a94ad83fb75df5ad468b96%2CNQvYk%2C2026-10-04-18-15-43"


def test_prices_reuses_the_cached_token(site: responses.RequestsMock, client: BonbastClient) -> None:
    client.prices()
    client.prices()

    assert _calls(site, "GET", "/") == 1
    assert _calls(site, "POST", "/json") == 2


def test_prices_refreshes_a_rejected_token(http: responses.RequestsMock, client: BonbastClient) -> None:
    http.get(f"{BASE_URL}/", body=fixture_text("home.html"))
    http.post(f"{BASE_URL}/json", json={"reset": 1})
    http.post(f"{BASE_URL}/json", json=fixture_json("prices.json"))

    assert len(client.prices().currencies) == 28
    assert _calls(http, "GET", "/") == 2


def test_prices_gives_up_when_the_token_keeps_failing(http: responses.RequestsMock, client: BonbastClient) -> None:
    http.get(f"{BASE_URL}/", body=fixture_text("home.html"))
    http.post(f"{BASE_URL}/json", json={"reset": 1})

    with pytest.raises(NetworkError, match="rejecting"):
        client.prices()


def test_http_errors_become_network_errors(http: responses.RequestsMock, client: BonbastClient) -> None:
    http.get(f"{BASE_URL}/", status=403)

    with pytest.raises(NetworkError, match="HTTP 403"):
        client.prices()


def test_connection_errors_become_network_errors(http: responses.RequestsMock, client: BonbastClient) -> None:
    http.get(f"{BASE_URL}/", body=requests.ConnectionError("boom"))

    with pytest.raises(NetworkError, match="could not connect"):
        client.prices()


def test_non_json_answers_become_parse_errors(http: responses.RequestsMock, client: BonbastClient) -> None:
    http.get(f"{BASE_URL}/", body=fixture_text("home.html"))
    http.post(f"{BASE_URL}/json", body="<html>Checking your browser…</html>")

    with pytest.raises(ParseError):
        client.prices()


def test_history(http: responses.RequestsMock, client: BonbastClient) -> None:
    day = tehran_today() - timedelta(days=3)
    http.post(
        f"{BASE_URL}/archive",
        body=fixture_text("archive.html"),
        match=[matchers.urlencoded_params_matcher({"date": day.isoformat()})],
    )

    assert len(client.history(day).coins) == 5


@pytest.mark.parametrize("days_ago", [0, -1])
def test_history_rejects_today_and_the_future(client: BonbastClient, days_ago: int) -> None:
    with pytest.raises(InvalidDateError):
        client.history(tehran_today() - timedelta(days=days_ago))


def test_history_rejects_dates_before_the_archive(client: BonbastClient) -> None:
    with pytest.raises(InvalidDateError):
        client.history(FIRST_ARCHIVE_DATE - timedelta(days=1))


def test_graph_includes_the_end_date(http: responses.RequestsMock, client: BonbastClient) -> None:
    end = tehran_today() - timedelta(days=5)
    start = end - timedelta(days=10)
    http.post(
        f"{BASE_URL}/graph",
        body=fixture_text("graph.html"),
        match=[
            matchers.urlencoded_params_matcher(
                {"currency": "eur", "stdate": start.isoformat(), "endate": (end + timedelta(days=1)).isoformat()}
            )
        ],
    )

    assert len(client.graph("EUR", start, end)) == 9


def test_graph_never_asks_for_a_future_end_date(http: responses.RequestsMock, client: BonbastClient) -> None:
    today = tehran_today()
    start = today - timedelta(days=30)
    http.post(
        f"{BASE_URL}/graph",
        body=fixture_text("graph.html"),
        match=[
            matchers.urlencoded_params_matcher(
                {"currency": "usd", "stdate": start.isoformat(), "endate": today.isoformat()}
            )
        ],
    )

    client.graph("usd", start, today)


def test_graph_validates_the_range(client: BonbastClient) -> None:
    today = tehran_today()
    with pytest.raises(InvalidDateError):
        client.graph("usd", today - timedelta(days=1), today - timedelta(days=2))
    with pytest.raises(InvalidDateError):
        client.graph("usd", today, today + timedelta(days=1))
    with pytest.raises(InvalidDateError):
        client.graph("usd", FIRST_ARCHIVE_DATE - timedelta(days=1), today)
    with pytest.raises(ValueError):
        client.graph("xyz", today - timedelta(days=2), today)


def test_token_is_shared_through_the_cache_file(site: responses.RequestsMock, tmp_path: Path) -> None:
    path = tmp_path / "shared.json"
    with BonbastClient(token_cache=TokenCache(path)) as first:
        first.prices()
    with BonbastClient(token_cache=TokenCache(path)) as second:
        second.prices()

    assert _calls(site, "GET", "/") == 1
    assert TOKEN in path.read_text()
