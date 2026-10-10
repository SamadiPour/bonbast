"""Checks against the real bonbast.com, to notice when the website changes.

Skipped unless BONBAST_LIVE_TESTS=1.
"""

import os
from datetime import timedelta

import pytest

from bonbast.client import BonbastClient, tehran_today

pytestmark = pytest.mark.skipif(not os.environ.get("BONBAST_LIVE_TESTS"), reason="set BONBAST_LIVE_TESTS=1 to run")


def test_prices(client: BonbastClient) -> None:
    prices = client.prices()
    assert prices.currencies and prices.coins and prices.golds
    assert all(currency.is_valid() for currency in prices.currencies)


def test_history(client: BonbastClient) -> None:
    prices = client.history(tehran_today() - timedelta(days=7))
    assert prices.currencies and prices.coins


def test_graph(client: BonbastClient) -> None:
    end = tehran_today() - timedelta(days=1)
    assert client.graph("usd", end - timedelta(days=7), end)
