from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Action(str, Enum):
    CLOCK_IN = "in"
    CLOCK_OUT = "out"

    @classmethod
    def parse(cls, value: str) -> "Action":
        try:
            return cls(value)
        except ValueError as exc:
            raise ValueError(f"Unsupported action: {value}") from exc


@dataclass(frozen=True)
class ClockEmail:
    receiver: str
    subject: str
    body: str


def build_clock_email(
    action: Action,
    receiver: str,
    now: datetime | None = None,
) -> ClockEmail:
    current_time = now or datetime.now()
    date_value = current_time.strftime("%d/%m/%Y")

    if action == Action.CLOCK_IN:
        subject_action = "Inizio"
        time_value = "10:00"
    else:
        subject_action = "Fine"
        time_value = "19:00"

    return ClockEmail(
        receiver=receiver,
        subject=f"Lavoro da remoto - {subject_action} {date_value}",
        body=(
            f"{subject_action} orario lavorativo da remoto in data "
            f"{date_value} alle ore {time_value}"
        ),
    )
