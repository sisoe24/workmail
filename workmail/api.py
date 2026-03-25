from __future__ import annotations

import json
import os
from typing import Any, Mapping

from .core import Action, build_clock_email
from .resend import send_email_via_resend


def json_response(status: int, payload: dict[str, Any]) -> tuple[int, bytes]:
    return status, json.dumps(payload).encode("utf-8")


def handle_clock_request(
    method: str,
    headers: Mapping[str, str],
    body: bytes,
    env: Mapping[str, str] | None = None,
    sender=send_email_via_resend,
) -> tuple[int, bytes]:
    config = env or os.environ

    if method != "POST":
        return json_response(405, {"ok": False, "error": "method_not_allowed"})

    auth_header = headers.get("Authorization", "")
    expected_secret = config.get("WORKMAIL_SECRET", "")
    expected_header = f"Bearer {expected_secret}" if expected_secret else ""
    if not expected_secret or auth_header != expected_header:
        return json_response(401, {"ok": False, "error": "unauthorized"})

    try:
        payload = json.loads(body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return json_response(400, {"ok": False, "error": "invalid_json"})

    action_value = payload.get("action")
    if not isinstance(action_value, str):
        return json_response(400, {"ok": False, "error": "invalid_action"})

    try:
        action = Action.parse(action_value)
    except ValueError:
        return json_response(400, {"ok": False, "error": "invalid_action"})

    receiver = config.get("WORKMAIL_RECEIVER", "")
    api_key = config.get("RESEND_API_KEY", "")
    from_email = config.get("WORKMAIL_FROM_EMAIL", "")
    if not receiver or not api_key or not from_email:
        return json_response(500, {"ok": False, "error": "missing_server_config"})

    email = build_clock_email(action=action, receiver=receiver)

    try:
        sender(email=email, api_key=api_key, from_email=from_email)
    except Exception as exc:
        return json_response(
            500,
            {"ok": False, "error": "send_failed", "detail": str(exc)},
        )

    return json_response(200, {"ok": True})
