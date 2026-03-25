from __future__ import annotations

import json

from workmail.api import handle_clock_request


ENV = {
    "WORKMAIL_SECRET": "secret-token",
    "WORKMAIL_RECEIVER": "boss@example.com",
    "RESEND_API_KEY": "resend-key",
    "WORKMAIL_FROM_EMAIL": "clock@example.com",
}


def test_valid_clock_in_request() -> None:
    calls = []

    def sender(**kwargs):
        calls.append(kwargs)

    status, body = handle_clock_request(
        method="POST",
        headers={"Authorization": "Bearer secret-token"},
        body=b'{"action":"in"}',
        env=ENV,
        sender=sender,
    )

    assert status == 200
    assert json.loads(body) == {"ok": True}
    assert calls[0]["email"].receiver == "boss@example.com"


def test_valid_clock_out_request() -> None:
    calls = []

    def sender(**kwargs):
        calls.append(kwargs)

    status, body = handle_clock_request(
        method="POST",
        headers={"Authorization": "Bearer secret-token"},
        body=b'{"action":"out"}',
        env=ENV,
        sender=sender,
    )

    assert status == 200
    assert json.loads(body) == {"ok": True}
    assert calls[0]["email"].subject.startswith("Lavoro da remoto - Fine ")


def test_missing_auth_returns_401() -> None:
    status, body = handle_clock_request(
        method="POST",
        headers={},
        body=b'{"action":"in"}',
        env=ENV,
    )

    assert status == 401
    assert json.loads(body)["error"] == "unauthorized"


def test_wrong_auth_returns_401() -> None:
    status, body = handle_clock_request(
        method="POST",
        headers={"Authorization": "Bearer nope"},
        body=b'{"action":"in"}',
        env=ENV,
    )

    assert status == 401
    assert json.loads(body)["error"] == "unauthorized"


def test_invalid_action_returns_400() -> None:
    status, body = handle_clock_request(
        method="POST",
        headers={"Authorization": "Bearer secret-token"},
        body=b'{"action":"start"}',
        env=ENV,
    )

    assert status == 400
    assert json.loads(body)["error"] == "invalid_action"


def test_resend_failure_returns_500() -> None:
    def sender(**kwargs):
        raise RuntimeError("provider unavailable")

    status, body = handle_clock_request(
        method="POST",
        headers={"Authorization": "Bearer secret-token"},
        body=b'{"action":"in"}',
        env=ENV,
        sender=sender,
    )

    payload = json.loads(body)
    assert status == 500
    assert payload["error"] == "send_failed"
