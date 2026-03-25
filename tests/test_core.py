from __future__ import annotations

from datetime import datetime

from workmail.core import Action, build_clock_email


def test_build_clock_in_email() -> None:
    email = build_clock_email(
        action=Action.CLOCK_IN,
        receiver="boss@example.com",
        now=datetime(2026, 3, 25, 9, 30),
    )
    assert email.subject == "Lavoro da remoto - Inizio 25/03/2026"
    assert email.body == "Inizio orario lavorativo da remoto in data 25/03/2026 alle ore 10:00"


def test_build_clock_out_email() -> None:
    email = build_clock_email(
        action=Action.CLOCK_OUT,
        receiver="boss@example.com",
        now=datetime(2026, 3, 25, 18, 0),
    )
    assert email.subject == "Lavoro da remoto - Fine 25/03/2026"
    assert email.body == "Fine orario lavorativo da remoto in data 25/03/2026 alle ore 19:00"
