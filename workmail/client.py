from __future__ import annotations

import json
from typing import Any, Callable
from urllib import error, request

from .core import Action


def trigger_remote_clock(
    action: Action,
    api_url: str,
    secret: str,
    opener: Callable[..., Any] = request.urlopen,
) -> dict[str, Any]:
    payload = json.dumps({"action": action.value}).encode("utf-8")
    req = request.Request(
        api_url,
        data=payload,
        headers={
            "Authorization": f"Bearer {secret}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with opener(req, timeout=10) as response:
            body = response.read().decode("utf-8") or "{}"
            return json.loads(body)
    except error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Clock request failed with HTTP {exc.code}: {detail}") from exc
    except error.URLError as exc:
        raise RuntimeError(f"Could not reach Workmail endpoint: {exc.reason}") from exc
