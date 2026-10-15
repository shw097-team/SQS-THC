"""Frozen acceptance tests for the Temporal / Five Clocks kernel (CH06).

Codex bounded worker must FILL the test bodies so they pass against the
implemented kernel. Fixtures match P0-CIP CH06 frozen fixtures:
CH06-POS-001 / CH06-NEG-001 / CH06-EDGE-001 / CH06-ADV-001.
"""
import unittest

from kernel.temporal import (
    CalendarGapError,
    ClockOrderingError,
    FiveClockStamp,
    LookaheadError,
    PITRecord,
    TemporalState,
    TradingCalendar,
    bind_clocks,
    quality_pass,
    validate_calendar,
)


def make_calendar() -> TradingCalendar:
    return TradingCalendar(
        id="ch06-calendar-001", schema_version="1.0.0",
        calendar_id="ch06-calendar-id-001", dataset_version="v1.0.0", active=True,
    )


def make_record() -> PITRecord:
    return PITRecord(
        id="ch06-record-001", schema_version="1.0.0", record_id="ch06-record-id-001",
        event_time="2026-08-06T12:00:00+08:00",
        availability_time="2026-08-06T12:00:00+08:00",
        decision_time="2026-08-06T12:00:00+08:00",
        execution_time="2026-08-06T12:00:00+08:00",
        recorded_time="2026-08-06T12:00:00+08:00",
        calendar_id="ch06-calendar-id-001",
    )


class CH06PositiveTests(unittest.TestCase):
    def test_pos_001_full_pipeline(self):
        """CH06-POS-001: INGESTED -> CLOCK_BOUND -> CALENDAR_VALID -> QUALITY_PASS."""
        r = make_record()
        bound = bind_clocks(r, make_calendar())
        self.assertEqual(bound.state, TemporalState.CLOCK_BOUND)
        valid = validate_calendar(bound, make_calendar())
        self.assertEqual(valid.state, TemporalState.CALENDAR_VALID)
        passed = quality_pass(valid)
        self.assertEqual(passed.state, TemporalState.QUALITY_PASS)

    def test_pos_002_clock_ordering_preserved(self):
        """Five clocks remain ordered after binding."""
        r = make_record()
        bound = bind_clocks(r, make_calendar())
        self.assertLessEqual(parse(bound.event_time), parse(bound.availability_time))
        self.assertLessEqual(parse(bound.availability_time), parse(bound.decision_time))
        self.assertLessEqual(parse(bound.decision_time), parse(bound.execution_time))


class CH06NegativeTests(unittest.TestCase):
    def test_neg_001_lookahead(self):
        """CH06-NEG-001: availability_time > decision_time -> ERR_LOOKAHEAD."""
        r = PITRecord(
            id="ch06-invalid-001", schema_version="1.0.0", record_id="ch06-record-id-001",
            event_time="2026-08-06T10:00:00+08:00",
            availability_time="2026-08-06T14:00:00+08:00",   # after decision
            decision_time="2026-08-06T12:00:00+08:00",
            execution_time="2026-08-06T15:00:00+08:00",
            recorded_time="2026-08-06T16:00:00+08:00",
            calendar_id="ch06-calendar-id-001",
        )
        with self.assertRaises(LookaheadError):
            bind_clocks(r, make_calendar())

    def test_neg_002_clock_ordering(self):
        """execution_time before decision_time -> ERR_CLOCK_ORDERING."""
        r = PITRecord(
            id="ch06-invalid-002", schema_version="1.0.0", record_id="ch06-record-id-002",
            event_time="2026-08-06T12:00:00+08:00",
            availability_time="2026-08-06T12:00:00+08:00",
            decision_time="2026-08-06T13:00:00+08:00",
            execution_time="2026-08-06T12:30:00+08:00",   # before decision
            recorded_time="2026-08-06T14:00:00+08:00",
            calendar_id="ch06-calendar-id-001",
        )
        with self.assertRaises(ClockOrderingError):
            bind_clocks(r, make_calendar())

    def test_neg_003_calendar_gap(self):
        """inactive calendar -> ERR_CALENDAR_GAP."""
        r = make_record()
        bound = bind_clocks(r, make_calendar())
        inactive = TradingCalendar(
            id="ch06-calendar-002", schema_version="1.0.0",
            calendar_id="ch06-calendar-id-001", dataset_version="v1.0.0", active=False,
        )
        with self.assertRaises(CalendarGapError):
            validate_calendar(bound, inactive)


class CH06EdgeTests(unittest.TestCase):
    def test_edge_001_half_day_late_correction(self):
        """half-day calendar + late correction -> ABSTAIN_OR_DEGRADED_WITH_TT."""
        r = PITRecord(
            id="ch06-edge-001", schema_version="1.0.0", record_id="ch06-record-id-003",
            event_time="2026-08-06T10:30:00+08:00",
            availability_time="2026-08-06T12:00:00+08:00",
            decision_time="2026-08-06T13:30:00+08:00",
            execution_time="2026-08-06T14:00:00+08:00",
            recorded_time="2026-08-06T18:00:00+08:00",   # late correction
            calendar_id="ch06-calendar-id-001",
            dataset_version="v1.0.0-draft",  # not frozen
        )
        # contract abstains (raises) or degrades with TT marker, never silent pass
        with self.assertRaises(Exception):
            validate_calendar(bind_clocks(r, make_calendar()), make_calendar())


class CH06AdversarialTests(unittest.TestCase):
    def test_adv_001_forged_owner_rejected(self):
        """CH06-ADV-001: forged owner_id must be rejected."""
        forged = PITRecord(
            id="ch06-record-004", schema_version="1.0.0", record_id="ch06-record-id-004",
            event_time="2026-08-06T12:00:00+08:00",
            availability_time="2026-08-06T12:00:00+08:00",
            decision_time="2026-08-06T12:00:00+08:00",
            execution_time="2026-08-06T12:00:00+08:00",
            recorded_time="2026-08-06T12:00:00+08:00",
            calendar_id="ch06-calendar-id-001",
            owner_id="attacker",
        )
        with self.assertRaises(Exception):
            bind_clocks(forged, make_calendar())


def parse(ts: str):
    from datetime import datetime
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


if __name__ == "__main__":
    unittest.main()
