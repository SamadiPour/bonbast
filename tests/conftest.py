from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest
import responses

from bonbast.client import BASE_URL, BonbastClient
from bonbast.token_cache import TokenCache

FIXTURES = Path(__file__).parent / "fixtures"
TOKEN = "fef9596724a94ad83fb75df5ad468b96,NQvYk,2026-10-04-18-15-43"


def fixture_text(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def fixture_json(name: str) -> dict[str, Any]:
    return json.loads(fixture_text(name))


@pytest.fixture(autouse=True)
def _isolated_token_cache(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Never touch the real user cache directory."""
    monkeypatch.setattr(TokenCache, "default", classmethod(lambda cls: cls(tmp_path / "token.json")))


@pytest.fixture
def http() -> Iterator[responses.RequestsMock]:
    with responses.RequestsMock(assert_all_requests_are_fired=False) as mock:
        yield mock


@pytest.fixture
def site(http: responses.RequestsMock) -> responses.RequestsMock:
    """bonbast.com serving the recorded fixtures."""
    http.get(f"{BASE_URL}/", body=fixture_text("home.html"))
    http.post(f"{BASE_URL}/json", json=fixture_json("prices.json"))
    http.post(f"{BASE_URL}/archive", body=fixture_text("archive.html"))
    http.post(f"{BASE_URL}/graph", body=fixture_text("graph.html"))
    return http


@pytest.fixture
def client(tmp_path: Path) -> Iterator[BonbastClient]:
    with BonbastClient(token_cache=TokenCache(tmp_path / "client-token.json")) as client:
        yield client
