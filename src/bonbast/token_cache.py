"""Keeps the bonbast.com access token between runs, saving a request per run."""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

from platformdirs import user_cache_path


class TokenCache:
    """Stores the access token in memory and, optionally, in a file.

    The cache is best effort: an unreadable, corrupt or unwritable file just means a fresh token gets fetched.
    """

    def __init__(self, path: Path | None = None, ttl: float = 600.0) -> None:
        self.path = path
        self.ttl = ttl
        self._token: str | None = None
        self._created_at = 0.0

    @classmethod
    def default(cls) -> TokenCache:
        return cls(user_cache_path("bonbast", appauthor=False) / "token.json")

    def load(self) -> str | None:
        """Return the cached token, or ``None`` if there is none or it has expired."""
        if self._token is None:
            self._read()
        if self._token is not None and time.time() - self._created_at < self.ttl:
            return self._token
        return None

    def save(self, token: str) -> None:
        self._token = token
        self._created_at = time.time()
        if self.path is None:
            return
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            temporary = self.path.with_suffix(".tmp")
            temporary.write_text(json.dumps({"token": token, "created_at": self._created_at}), encoding="utf-8")
            os.replace(temporary, self.path)
        except OSError:
            pass

    def clear(self) -> None:
        self._token = None
        if self.path is None:
            return
        try:
            self.path.unlink(missing_ok=True)
        except OSError:
            pass

    def _read(self) -> None:
        if self.path is None:
            return
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            token, created_at = data["token"], float(data["created_at"])
        except (OSError, ValueError, TypeError, KeyError):
            return
        if isinstance(token, str) and token:
            self._token, self._created_at = token, created_at
