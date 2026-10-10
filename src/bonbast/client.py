"""HTTP client for bonbast.com."""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from types import TracebackType
from typing import Any

import requests
from requests.adapters import HTTPAdapter, Retry

from .catalog import CURRENCIES
from .errors import InvalidDateError, NetworkError, ParseError
from .models import Prices
from .parsers import parse_archive, parse_graph, parse_prices, parse_token
from .token_cache import TokenCache

BASE_URL = "https://bonbast.com"
USER_AGENT = (
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/140.0.0.0 Mobile Safari/537.36"
)
FIRST_ARCHIVE_DATE = date(2012, 10, 9)
# Iran stopped observing daylight saving time in 2022, so a fixed offset is exact.
TEHRAN = timezone(timedelta(hours=3, minutes=30), "Asia/Tehran")

_XHR_HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Origin": BASE_URL,
    "Referer": f"{BASE_URL}/",
    "X-Requested-With": "XMLHttpRequest",
}


def tehran_today() -> date:
    """bonbast.com follows Tehran's calendar, so "today" means today in Tehran."""
    return datetime.now(TEHRAN).date()


class BonbastClient:
    """Fetches prices from bonbast.com.

    >>> with BonbastClient() as client:  # doctest: +SKIP
    ...     usd = client.prices().get("usd")
    ...     print(usd.sell, usd.buy)
    """

    def __init__(
        self,
        *,
        session: requests.Session | None = None,
        token_cache: TokenCache | None = None,
        timeout: float = 10.0,
    ) -> None:
        self._session = session or _new_session()
        self._tokens = token_cache or TokenCache.default()
        self._timeout = timeout

    def close(self) -> None:
        self._session.close()

    def __enter__(self) -> BonbastClient:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.close()

    def prices(self) -> Prices:
        """Current prices of currencies, coins and gold."""
        for attempt in range(2):
            token = self._token(refresh=attempt > 0)
            data = self._post_json("/json", {"param": token})
            if "reset" not in data:
                return parse_prices(data)
            # The token expired before our cache noticed; drop it and try once more with a fresh one.
            self._tokens.clear()
        raise NetworkError("bonbast.com keeps rejecting the access token; please try again later")

    def history(self, day: date) -> Prices:
        """Prices of currencies and coins on a past day."""
        yesterday = tehran_today() - timedelta(days=1)
        if not FIRST_ARCHIVE_DATE <= day <= yesterday:
            raise InvalidDateError(f"date must be between {FIRST_ARCHIVE_DATE} and {yesterday}")
        return parse_archive(self._request("POST", "/archive", data={"date": day.isoformat()}).text)

    def graph(self, currency: str, start: date, end: date) -> dict[date, int]:
        """Daily sell price of a currency, from ``start`` to ``end`` inclusive."""
        if currency.upper() not in CURRENCIES:
            raise ValueError(f"unknown currency: {currency}")
        today = tehran_today()
        if start > end:
            raise InvalidDateError("the start date must not be after the end date")
        if start < FIRST_ARCHIVE_DATE:
            raise InvalidDateError(f"the start date must not be before {FIRST_ARCHIVE_DATE}")
        if end > today:
            raise InvalidDateError(f"the end date must not be after today ({today})")

        # bonbast.com excludes the end date, and silently swaps in a default range if it is in the future.
        stop = min(end + timedelta(days=1), today)
        form = {"currency": currency.lower(), "stdate": start.isoformat(), "endate": stop.isoformat()}
        return parse_graph(self._request("POST", "/graph", data=form).text)

    def _token(self, *, refresh: bool) -> str:
        token = None if refresh else self._tokens.load()
        if token is None:
            token = parse_token(self._request("GET", "/").text)
            self._tokens.save(token)
        return token

    def _post_json(self, path: str, data: dict[str, str]) -> dict[str, Any]:
        response = self._request("POST", path, data=data, headers=_XHR_HEADERS)
        try:
            payload = response.json()
        except ValueError as error:
            raise ParseError("bonbast.com returned an unexpected response") from error
        if not isinstance(payload, dict):
            raise ParseError("bonbast.com returned an unexpected response")
        return payload

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        try:
            response = self._session.request(method, BASE_URL + path, timeout=self._timeout, **kwargs)
            response.raise_for_status()
        except requests.HTTPError as error:
            raise NetworkError(f"bonbast.com responded with HTTP {error.response.status_code}") from error
        except requests.Timeout as error:
            raise NetworkError("bonbast.com did not respond in time") from error
        except requests.ConnectionError as error:
            raise NetworkError("could not connect to bonbast.com; check your internet connection") from error
        except requests.RequestException as error:
            raise NetworkError(f"request to bonbast.com failed: {error}") from error
        return response


def _new_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"})
    session.cookies.update({"cookieconsent_status": "true", "st_bb": "0"})
    # Every request bonbast makes only reads data, so retrying POSTs is safe too.
    retry = Retry(
        total=2,
        backoff_factor=0.5,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=None,
        raise_on_status=False,
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session
