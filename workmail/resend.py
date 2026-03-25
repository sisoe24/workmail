from __future__ import annotations

import json
from typing import Any, Callable
from urllib import error, request

from .core import ClockEmail

RESEND_API_URL = "https://api.resend.com/emails"


def send_email_via_resend(
    email: ClockEmail,
    api_key: str,
    from_email: str,
    opener: Callable[..., Any] = request.urlopen,
) -> None:
    payload = json.dumps(
        {
            "from": from_email,
            "to": [email.receiver],
            "subject": email.subject,
            "text": email.body,
        }
    ).encode("utf-8")

    req = request.Request(
        RESEND_API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with opener(req, timeout=10) as response:
            if response.status >= 400:
                raise RuntimeError(f"Resend returned HTTP {response.status}")
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Resend returned HTTP {exc.code}: {detail}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Could not reach Resend: {exc.reason}") from exc
