"""SQS-THC Temporal / Five Clocks / PIT / Trading Calendar — package skeleton (TS-REF-03 / CH06).

PRE-SEEDED skeleton for the Codex bounded worker. Windows Codex sandbox cannot
CREATE new files, so the contract surface is pre-seeded; Codex FILLS the
implementations + tests.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from enum import Enum


class TemporalState(str, Enum):
    INGESTED = "INGESTED"
    CLOCK_BOUND = "CLOCK_BOUND"
    CALENDAR_VALID = "CALENDAR_VALID"
    QUALITY_PASS = "QUALITY_PASS"


class TemporalError(Exception):
    code = "ERR_TEMPORAL"


class LookaheadError(TemporalError):
    code = "ERR_LOOKAHEAD"


class CalendarGapError(TemporalError):
    code = "ERR_CALENDAR_GAP"


class ClockOrderingError(TemporalError):
    code = "ERR_CLOCK_ORDERING"


class StaleVersionError(TemporalError):
    code = "ERR_STALE_VERSION"


@dataclass(frozen=True)
class FiveClockStamp:
    id: str
    schema_version: str
    event_time: str
    availability_time: str
    decision_time: str
    execution_time: str
    recorded_time: str
    calendar_id: str
    dataset_version: str = "v1.0.0"
    owner_id: str = "Temporal and Data Quality Owner"


@dataclass(frozen=True)
class TradingCalendar:
    id: str
    schema_version: str
    calendar_id: str
    dataset_version: str
    active: bool = True
    owner_id: str = "Temporal and Data Quality Owner"


@dataclass(frozen=True)
class PITRecord:
    id: str
    schema_version: str
    record_id: str
    event_time: str
    availability_time: str
    decision_time: str
    execution_time: str
    recorded_time: str
    calendar_id: str
    dataset_version: str = "v1.0.0"
    state: TemporalState = TemporalState.INGESTED
    owner_id: str = "Temporal and Data Quality Owner"


def parse_iso(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


_EXPECTED_OWNER = "Temporal and Data Quality Owner"

# Non-frozen version markers (a frozen dataset_version is a released, immutable
# version such as "v1.0.0"; any draft/snapshot marker means the data may still
# change and the kernel must abstain rather than silently pass).
_NON_FROZEN_MARKERS = ("-draft", "-alpha", "-beta", "-rc", "-dev", "-snapshot")


def _is_frozen(dataset_version: str) -> bool:
    lowered = dataset_version.lower()
    return not any(marker in lowered for marker in _NON_FROZEN_MARKERS)


def bind_clocks(record: PITRecord, calendar: TradingCalendar) -> PITRecord:
    """INGESTED -> CLOCK_BOUND. Verifies owner + calendar active + clock ordering.

    Core predicate: event_time <= availability_time <= decision_time <=
    execution_time. Violation -> ERR_LOOKAHEAD (availability > decision) or
    ERR_CLOCK_ORDERING (any other ordering break).
    """
    if record.owner_id != _EXPECTED_OWNER:
        raise TemporalError(
            f"forged owner_id rejected: {record.owner_id!r}; "
            f"expected {_EXPECTED_OWNER!r}"
        )
    if not calendar.active:
        raise CalendarGapError(
            f"calendar {calendar.id!r} (calendar_id={calendar.calendar_id!r}) "
            "is inactive; clocks cannot be bound"
        )

    event = parse_iso(record.event_time)
    availability = parse_iso(record.availability_time)
    decision = parse_iso(record.decision_time)
    execution = parse_iso(record.execution_time)

    if availability > decision:
        raise LookaheadError(
            f"lookahead: availability_time {record.availability_time} is after "
            f"decision_time {record.decision_time}"
        )
    if not (event <= availability <= decision <= execution):
        raise ClockOrderingError(
            "clock ordering violated: expected event_time <= availability_time "
            "<= decision_time <= execution_time "
            f"(got {record.event_time}, {record.availability_time}, "
            f"{record.decision_time}, {record.execution_time})"
        )

    return replace(record, state=TemporalState.CLOCK_BOUND)


def validate_calendar(record: PITRecord, calendar: TradingCalendar) -> PITRecord:
    """CLOCK_BOUND -> CALENDAR_VALID. calendar active + dataset_version frozen.

    Inactive calendar -> ERR_CALENDAR_GAP.
    """
    if not calendar.active:
        raise CalendarGapError(
            f"calendar gap: calendar {calendar.id!r} "
            f"(calendar_id={calendar.calendar_id!r}) is inactive"
        )
    for source, version in (
        ("record", record.dataset_version),
        ("calendar", calendar.dataset_version),
    ):
        if not _is_frozen(version):
            raise StaleVersionError(
                f"abstain: {source} dataset_version {version!r} is not frozen "
                "(contains a draft marker); cannot validate against a moving "
                "version"
            )
    return replace(record, state=TemporalState.CALENDAR_VALID)


def quality_pass(record: PITRecord) -> PITRecord:
    """CALENDAR_VALID -> QUALITY_PASS."""
    return replace(record, state=TemporalState.QUALITY_PASS)
