import json
import time
from pathlib import Path

import pytest

from bonbast.token_cache import TokenCache


def test_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "nested" / "token.json"
    TokenCache(path).save("abc")

    assert TokenCache(path).load() == "abc"


def test_expired_tokens_are_ignored(tmp_path: Path) -> None:
    path = tmp_path / "token.json"
    path.write_text(json.dumps({"token": "abc", "created_at": time.time() - 601}))

    assert TokenCache(path, ttl=600).load() is None


@pytest.mark.parametrize("content", ["", "not json", "[]", '{"token": 1, "created_at": 0}', '{"token": "abc"}'])
def test_corrupt_files_are_ignored(tmp_path: Path, content: str) -> None:
    path = tmp_path / "token.json"
    path.write_text(content)

    assert TokenCache(path).load() is None


def test_clear(tmp_path: Path) -> None:
    path = tmp_path / "token.json"
    cache = TokenCache(path)
    cache.save("abc")
    cache.clear()

    assert cache.load() is None
    assert not path.exists()


def test_memory_only() -> None:
    cache = TokenCache(None)
    cache.save("abc")

    assert cache.load() == "abc"


def test_unwritable_location_is_not_fatal(tmp_path: Path) -> None:
    blocker = tmp_path / "file"
    blocker.write_text("")
    cache = TokenCache(blocker / "token.json")
    cache.save("abc")

    assert cache.load() == "abc"
