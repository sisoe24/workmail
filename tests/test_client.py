from __future__ import annotations

import json

from workmail.client import trigger_remote_clock
from workmail.core import Action


class FakeResponse:
    def __init__(self, payload: dict[str, object], status: int = 200) -> None:
        self._payload = json.dumps(payload).encode("utf-8")
        self.status = status

    def read(self) -> bytes:
        return self._payload

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None


def test_trigger_remote_clock_sends_in_payload() -> None:
    captured = {}

    def opener(req, timeout=10):
        captured["url"] = req.full_url
        captured["auth"] = req.headers["Authorization"]
        captured["body"] = req.data
        return FakeResponse({"ok": True})

    result = trigger_remote_clock(
        action=Action.CLOCK_IN,
        api_url="https://example.com/api/clock",
        secret="secret-token",
        opener=opener,
    )

    assert result == {"ok": True}
    assert captured["url"] == "https://example.com/api/clock"
    assert captured["auth"] == "Bearer secret-token"
    assert json.loads(captured["body"]) == {"action": "in"}
