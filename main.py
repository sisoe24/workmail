from __future__ import annotations

import argparse
import os
from textwrap import dedent

from workmail.client import trigger_remote_clock
from workmail.core import Action, build_clock_email


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser("workmail")
    parser.add_argument("action", choices=[Action.CLOCK_IN.value, Action.CLOCK_OUT.value])
    parser.add_argument("--dry-run", action="store_true", default=False)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    action = Action.parse(args.action)

    receiver = os.environ.get("WORKMAIL_RECEIVER", "")
    if args.dry_run:
        if not receiver:
            raise SystemExit("WORKMAIL_RECEIVER is required for --dry-run")
        email = build_clock_email(action=action, receiver=receiver)
        print(
            dedent(
                f"""\
                [Receiver]
                {email.receiver}

                [Subject]
                {email.subject}

                [Body]
                {email.body}
                """
            ).rstrip()
        )
        return 0

    api_url = os.environ.get("WORKMAIL_API_URL", "").strip()
    secret = os.environ.get("WORKMAIL_SECRET", "").strip()
    if not api_url or not secret:
        raise SystemExit("WORKMAIL_API_URL and WORKMAIL_SECRET are required")

    result = trigger_remote_clock(action=action, api_url=api_url, secret=secret)
    if not result.get("ok"):
        raise SystemExit(f"Clock request failed: {result}")

    print(f"Sent clock {action.value}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
