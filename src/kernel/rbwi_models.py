"""SQS-THC RBWI Canonical Typed Models (RBWI v3.0.0 r2) - WO-RBWI-FULLRUN-001.

Materializes the missing RBWI contract layer for the TW-ICT runbook: canonical
enums plus frozen dataclasses with strict ``__post_init__`` validation.
Stdlib only (dataclasses + enum + typing); Python 3.11+.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Literal, Optional

RBWI_SCHEMA_VERSION = "3.0.0"

_SCHEMA_VERSION_RE = re.compile(r"\d+\.\d+\.\d+")
_WEEK_ID_RE = re.compile(r"^\d{4}-W\d{2}$")
_TRADING_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

_CLOCK_FIELDS = (
    "event_at",
    "published_at",
    "available_at",
    "ingested_at",
    "known_at",
    "decision_at",
    "effective_at",
    "expires_at",
)


class ContractState(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    INVALID = "INVALID"
    REVOKED = "REVOKED"
    BLOCKED = "BLOCKED"
    CLOSED = "CLOSED"


class AckState(str, Enum):
    PENDING = "PENDING"
    ACK = "ACK"
    REJECT = "REJECT"
    REVOKED = "REVOKED"


class ScenarioName(str, Enum):
    BASE = "BASE"
    BULL = "BULL"
    BEAR = "BEAR"
    UNKNOWN = "UNKNOWN"
    TAIL = "TAIL"


class CandidateTier(str, Enum):
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    OBSERVE = "OBSERVE"
    EXCLUDE = "EXCLUDE"
    QUARANTINE = "QUARANTINE"


def _parse_iso(value: str, field_name: str) -> datetime:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be an ISO-8601 string, got {type(value).__name__}")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field_name} must be ISO-8601: {value!r}") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _validate_iso(value: str, field_name: str) -> None:
    _parse_iso(value, field_name)


def _require_non_empty_str(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field_name} must be a non-empty string")


@dataclass(frozen=True)
class ClockVector:
    event_at: str
    published_at: str
    available_at: str
    ingested_at: str
    known_at: str
    decision_at: str
    effective_at: str
    expires_at: str

    def __post_init__(self) -> None:
        parsed = [_parse_iso(getattr(self, name), f"ClockVector.{name}") for name in _CLOCK_FIELDS]
        for index in range(len(parsed) - 1):
            if parsed[index + 1] < parsed[index]:
                raise ValueError(
                    "ClockVector clocks must be monotonic non-decreasing: "
                    f"{_CLOCK_FIELDS[index + 1]} < {_CLOCK_FIELDS[index]}"
                )
        if not (parsed[-2] < parsed[-1]):
            raise ValueError("ClockVector requires effective_at < expires_at")


@dataclass(frozen=True)
class ContractEnvelope:
    object_id: str
    object_type: str
    schema_version: str
    run_id: str
    correlation_id: str
    idempotency_key: str
    producer_role: str
    bound_agent: str
    consumers: list[str]
    accountable_role: str
    checker_role: str
    veto_role: str
    clocks: ClockVector
    state: ContractState
    reason_codes: list
    source_refs: list
    lineage: list
    policy_refs: list
    tool_version_refs: list
    rights: Literal["AUTHORIZED", "RESTRICTED", "UNKNOWN"]
    security_class: Literal["PUBLIC", "INTERNAL", "CONFIDENTIAL"]
    ack_state: AckState
    route_back: str
    supersedes: Optional[str] = None
    rollback_ref: Optional[str] = None

    def __post_init__(self) -> None:
        _require_non_empty_str(self.object_id, "ContractEnvelope.object_id")
        if len(self.object_id) < 3:
            raise ValueError("ContractEnvelope.object_id must have length >= 3")
        _require_non_empty_str(self.object_type, "ContractEnvelope.object_type")
        if len(self.object_type) < 3:
            raise ValueError("ContractEnvelope.object_type must have length >= 3")
        if not _SCHEMA_VERSION_RE.fullmatch(self.schema_version):
            raise ValueError(
                "ContractEnvelope.schema_version must match r'\\d+\\.\\d+\\.\\d+': "
                f"{self.schema_version!r}"
            )
        for name in (
            "run_id",
            "correlation_id",
            "idempotency_key",
            "producer_role",
            "bound_agent",
            "accountable_role",
            "checker_role",
            "veto_role",
            "route_back",
        ):
            _require_non_empty_str(getattr(self, name), f"ContractEnvelope.{name}")
        if not isinstance(self.consumers, list) or not self.consumers:
            raise ValueError("ContractEnvelope.consumers must be a non-empty list")
        if not isinstance(self.source_refs, list) or not self.source_refs:
            raise ValueError("ContractEnvelope.source_refs must be a non-empty list")
        if not isinstance(self.clocks, ClockVector):
            raise ValueError("ContractEnvelope.clocks must be a ClockVector")
        if not isinstance(self.state, ContractState):
            raise ValueError("ContractEnvelope.state must be a ContractState")
        if not isinstance(self.ack_state, AckState):
            raise ValueError("ContractEnvelope.ack_state must be an AckState")
        if self.rights not in ("AUTHORIZED", "RESTRICTED", "UNKNOWN"):
            raise ValueError(
                f"ContractEnvelope.rights must be one of AUTHORIZED/RESTRICTED/UNKNOWN: {self.rights!r}"
            )
        if self.security_class not in ("PUBLIC", "INTERNAL", "CONFIDENTIAL"):
            raise ValueError(
                "ContractEnvelope.security_class must be one of PUBLIC/INTERNAL/CONFIDENTIAL: "
                f"{self.security_class!r}"
            )


@dataclass(frozen=True)
class WeeklyContextPackage:
    envelope: ContractEnvelope
    week_id: str
    rule_snapshot_ref: str
    data_snapshot_refs: list
    transmission_path_refs: list
    alternative_explanations: list
    counterevidence_refs: list
    taiwan_regime_card_ref: str
    evidence_stack_refs: list
    universe_snapshot_ref: str
    candidate_pool_ref: str
    bias_hypothesis_refs: list
    scenario_tree_ref: str
    revision: int
    revoke_cascade_targets: list

    def __post_init__(self) -> None:
        if not isinstance(self.envelope, ContractEnvelope):
            raise ValueError("WeeklyContextPackage.envelope must be a ContractEnvelope")
        if not _WEEK_ID_RE.fullmatch(self.week_id):
            raise ValueError(
                f"WeeklyContextPackage.week_id must match ^\\d{{4}}-W\\d{{2}}$: {self.week_id!r}"
            )
        _require_non_empty_str(self.rule_snapshot_ref, "WeeklyContextPackage.rule_snapshot_ref")
        _require_non_empty_str(self.taiwan_regime_card_ref, "WeeklyContextPackage.taiwan_regime_card_ref")
        _require_non_empty_str(self.universe_snapshot_ref, "WeeklyContextPackage.universe_snapshot_ref")
        _require_non_empty_str(self.candidate_pool_ref, "WeeklyContextPackage.candidate_pool_ref")
        _require_non_empty_str(self.scenario_tree_ref, "WeeklyContextPackage.scenario_tree_ref")
        if not isinstance(self.data_snapshot_refs, list) or len(self.data_snapshot_refs) < 1:
            raise ValueError("WeeklyContextPackage.data_snapshot_refs must have at least 1 ref")
        if not isinstance(self.transmission_path_refs, list) or len(self.transmission_path_refs) < 2:
            raise ValueError("WeeklyContextPackage.transmission_path_refs must have at least 2 refs")
        if not isinstance(self.alternative_explanations, list) or len(self.alternative_explanations) < 1:
            raise ValueError("WeeklyContextPackage.alternative_explanations must have at least 1 entry")
        if not isinstance(self.counterevidence_refs, list) or len(self.counterevidence_refs) < 1:
            raise ValueError("WeeklyContextPackage.counterevidence_refs must have at least 1 ref")
        if not isinstance(self.evidence_stack_refs, list) or len(self.evidence_stack_refs) < 1:
            raise ValueError("WeeklyContextPackage.evidence_stack_refs must have at least 1 ref")
        if not isinstance(self.bias_hypothesis_refs, list) or len(self.bias_hypothesis_refs) < 1:
            raise ValueError("WeeklyContextPackage.bias_hypothesis_refs must have at least 1 ref")
        if not isinstance(self.revision, int) or self.revision < 1:
            raise ValueError("WeeklyContextPackage.revision must be an int >= 1")


@dataclass(frozen=True)
class DailyRunExecutionPackage:
    envelope: ContractEnvelope
    trading_date: str
    active_method_spec_refs: list
    operation_spec_ref: str
    weekly_context_ref: str
    rule_snapshot_ref: str
    data_snapshot_refs: list
    event_risk_packet_ref: str
    universe_snapshot_ref: str
    candidate_pool_ref: str
    bias_hypothesis_ref: str
    scenario_tree_ref: str
    risk_policy_ref: str
    tool_allowlist_ref: str
    operator_profile_ref: str
    session_timing_policy_ref: str
    state: Literal["DRAFT", "FROZEN", "ACTIVE", "CLOSED", "ABORTED"]
    mutation_writes: dict = field(
        default_factory=lambda: {"method": False, "operation": False, "risk": False, "tool": False}
    )
    broker_write_enabled: bool = False
    autonomous_order_submission: bool = False
    human_in_the_loop: str = "REQUIRED"

    def __post_init__(self) -> None:
        if not isinstance(self.envelope, ContractEnvelope):
            raise ValueError("DailyRunExecutionPackage.envelope must be a ContractEnvelope")
        if not _TRADING_DATE_RE.fullmatch(self.trading_date):
            raise ValueError(
                f"DailyRunExecutionPackage.trading_date must match ^\\d{{4}}-\\d{{2}}-\\d{{2}}$: "
                f"{self.trading_date!r}"
            )
        _require_non_empty_str(self.operation_spec_ref, "DailyRunExecutionPackage.operation_spec_ref")
        _require_non_empty_str(self.weekly_context_ref, "DailyRunExecutionPackage.weekly_context_ref")
        _require_non_empty_str(self.rule_snapshot_ref, "DailyRunExecutionPackage.rule_snapshot_ref")
        _require_non_empty_str(self.event_risk_packet_ref, "DailyRunExecutionPackage.event_risk_packet_ref")
        _require_non_empty_str(self.universe_snapshot_ref, "DailyRunExecutionPackage.universe_snapshot_ref")
        _require_non_empty_str(self.candidate_pool_ref, "DailyRunExecutionPackage.candidate_pool_ref")
        _require_non_empty_str(self.bias_hypothesis_ref, "DailyRunExecutionPackage.bias_hypothesis_ref")
        _require_non_empty_str(self.scenario_tree_ref, "DailyRunExecutionPackage.scenario_tree_ref")
        _require_non_empty_str(self.risk_policy_ref, "DailyRunExecutionPackage.risk_policy_ref")
        _require_non_empty_str(self.tool_allowlist_ref, "DailyRunExecutionPackage.tool_allowlist_ref")
        _require_non_empty_str(self.operator_profile_ref, "DailyRunExecutionPackage.operator_profile_ref")
        _require_non_empty_str(self.session_timing_policy_ref, "DailyRunExecutionPackage.session_timing_policy_ref")
        _require_non_empty_str(self.human_in_the_loop, "DailyRunExecutionPackage.human_in_the_loop")
        if not isinstance(self.active_method_spec_refs, list) or len(self.active_method_spec_refs) < 1:
            raise ValueError("DailyRunExecutionPackage.active_method_spec_refs must have at least 1 ref")
        if not isinstance(self.data_snapshot_refs, list) or len(self.data_snapshot_refs) < 1:
            raise ValueError("DailyRunExecutionPackage.data_snapshot_refs must have at least 1 ref")
        if self.state not in ("DRAFT", "FROZEN", "ACTIVE", "CLOSED", "ABORTED"):
            raise ValueError(
                "DailyRunExecutionPackage.state must be one of DRAFT/FROZEN/ACTIVE/CLOSED/ABORTED: "
                f"{self.state!r}"
            )
        expected_keys = {"method", "operation", "risk", "tool"}
        if not isinstance(self.mutation_writes, dict) or set(self.mutation_writes.keys()) != expected_keys:
            raise ValueError(
                "DailyRunExecutionPackage.mutation_writes keys must be exactly "
                f"{sorted(expected_keys)}"
            )
        for key in expected_keys:
            if not isinstance(self.mutation_writes[key], bool):
                raise ValueError(f"DailyRunExecutionPackage.mutation_writes[{key}] must be a bool")
        if self.state == "FROZEN" and any(self.mutation_writes.values()):
            raise ValueError(
                "DailyRunExecutionPackage.mutation_writes must be all False when state is FROZEN"
            )
        if self.broker_write_enabled is not False:
            raise ValueError(
                "DailyRunExecutionPackage.broker_write_enabled must remain False (NO-LIVE-WRITE)"
            )
        if self.autonomous_order_submission is not False:
            raise ValueError(
                "DailyRunExecutionPackage.autonomous_order_submission must remain False (HITL_ONLY)"
            )


@dataclass(frozen=True)
class BiasHypothesis:
    envelope: ContractEnvelope
    timeframe: Literal["WEEKLY", "DAILY", "INTRADAY"]
    parent_ref: Optional[str]
    supporting: list
    contradicting: list
    falsifier: str
    trigger: str
    invalidation: str
    expiry: str
    source_refs: list
    state: ContractState
    revision: int

    def __post_init__(self) -> None:
        if not isinstance(self.envelope, ContractEnvelope):
            raise ValueError("BiasHypothesis.envelope must be a ContractEnvelope")
        if self.timeframe not in ("WEEKLY", "DAILY", "INTRADAY"):
            raise ValueError(
                f"BiasHypothesis.timeframe must be one of WEEKLY/DAILY/INTRADAY: {self.timeframe!r}"
            )
        _require_non_empty_str(self.falsifier, "BiasHypothesis.falsifier")
        _require_non_empty_str(self.trigger, "BiasHypothesis.trigger")
        _require_non_empty_str(self.invalidation, "BiasHypothesis.invalidation")
        _require_non_empty_str(self.expiry, "BiasHypothesis.expiry")
        if not isinstance(self.supporting, list) or len(self.supporting) < 1:
            raise ValueError("BiasHypothesis.supporting must have at least 1 ref")
        if not isinstance(self.contradicting, list) or len(self.contradicting) < 1:
            raise ValueError("BiasHypothesis.contradicting must have at least 1 ref")
        if not isinstance(self.source_refs, list) or len(self.source_refs) < 1:
            raise ValueError("BiasHypothesis.source_refs must have at least 1 ref")
        if not isinstance(self.state, ContractState):
            raise ValueError("BiasHypothesis.state must be a ContractState")
        if not isinstance(self.revision, int) or self.revision < 1:
            raise ValueError("BiasHypothesis.revision must be an int >= 1")


@dataclass(frozen=True)
class ScenarioTree:
    envelope: ContractEnvelope
    branches: dict
    active_branch: ScenarioName
    transition_policy_ref: str
    unknown_branch_rule: str
    tail_branch_rule: str

    def __post_init__(self) -> None:
        if not isinstance(self.envelope, ContractEnvelope):
            raise ValueError("ScenarioTree.envelope must be a ContractEnvelope")
        required = {"BASE", "BULL", "BEAR", "UNKNOWN", "TAIL"}
        if not isinstance(self.branches, dict) or set(self.branches.keys()) != required:
            raise ValueError(
                "ScenarioTree.branches must have exactly keys BASE/BULL/BEAR/UNKNOWN/TAIL"
            )
        for name in sorted(required):
            if not isinstance(self.branches[name], str) or not self.branches[name]:
                raise ValueError(f"ScenarioTree.branches[{name}] must be a non-empty str")
        if not isinstance(self.active_branch, ScenarioName):
            raise ValueError("ScenarioTree.active_branch must be a ScenarioName")
        _require_non_empty_str(self.transition_policy_ref, "ScenarioTree.transition_policy_ref")
        _require_non_empty_str(self.unknown_branch_rule, "ScenarioTree.unknown_branch_rule")
        _require_non_empty_str(self.tail_branch_rule, "ScenarioTree.tail_branch_rule")


@dataclass(frozen=True)
class SetupObservation:
    envelope: ContractEnvelope
    candidate_ref: str
    method_ref: str
    observation_time_bucket: str
    components: dict
    snapshot_hash: str
    data_quality_state: Literal["CLEAN", "DEGRADED", "STALE"]

    def __post_init__(self) -> None:
        if not isinstance(self.envelope, ContractEnvelope):
            raise ValueError("SetupObservation.envelope must be a ContractEnvelope")
        _require_non_empty_str(self.candidate_ref, "SetupObservation.candidate_ref")
        _require_non_empty_str(self.method_ref, "SetupObservation.method_ref")
        _require_non_empty_str(self.observation_time_bucket, "SetupObservation.observation_time_bucket")
        _require_non_empty_str(self.snapshot_hash, "SetupObservation.snapshot_hash")
        if not isinstance(self.components, dict) or not self.components:
            raise ValueError("SetupObservation.components must be a non-empty dict")
        if self.data_quality_state not in ("CLEAN", "DEGRADED", "STALE"):
            raise ValueError(
                "SetupObservation.data_quality_state must be one of CLEAN/DEGRADED/STALE: "
                f"{self.data_quality_state!r}"
            )


@dataclass(frozen=True)
class SetupQualification:
    envelope: ContractEnvelope
    observation_ref: str
    method_ref: str
    decision: Literal["QUALIFIED", "REJECTED", "WAIT"]
    component_results: dict
    invalidation: str
    expiry_at: str
    reason_codes: list

    def __post_init__(self) -> None:
        if not isinstance(self.envelope, ContractEnvelope):
            raise ValueError("SetupQualification.envelope must be a ContractEnvelope")
        _require_non_empty_str(self.observation_ref, "SetupQualification.observation_ref")
        _require_non_empty_str(self.method_ref, "SetupQualification.method_ref")
        _require_non_empty_str(self.invalidation, "SetupQualification.invalidation")
        if self.decision not in ("QUALIFIED", "REJECTED", "WAIT"):
            raise ValueError(
                f"SetupQualification.decision must be one of QUALIFIED/REJECTED/WAIT: {self.decision!r}"
            )
        if not isinstance(self.component_results, dict) or not self.component_results:
            raise ValueError("SetupQualification.component_results must be a non-empty dict")
        _validate_iso(self.expiry_at, "SetupQualification.expiry_at")


@dataclass(frozen=True)
class RiskAuthorization:
    envelope: ContractEnvelope
    setup_ref: str
    position_ref: str
    risk_policy_ref: str
    decision: Literal["AUTHORIZED", "VETOED"]
    authorized_delta: float
    max_notional: float
    veto_reason: str
    expires_at: str
    reason_codes: list

    def __post_init__(self) -> None:
        if not isinstance(self.envelope, ContractEnvelope):
            raise ValueError("RiskAuthorization.envelope must be a ContractEnvelope")
        _require_non_empty_str(self.setup_ref, "RiskAuthorization.setup_ref")
        _require_non_empty_str(self.position_ref, "RiskAuthorization.position_ref")
        _require_non_empty_str(self.risk_policy_ref, "RiskAuthorization.risk_policy_ref")
        if self.decision not in ("AUTHORIZED", "VETOED"):
            raise ValueError(
                f"RiskAuthorization.decision must be one of AUTHORIZED/VETOED: {self.decision!r}"
            )
        if not isinstance(self.authorized_delta, (int, float)) or self.authorized_delta < 0:
            raise ValueError("RiskAuthorization.authorized_delta must be a number >= 0")
        if not isinstance(self.max_notional, (int, float)) or self.max_notional < 0:
            raise ValueError("RiskAuthorization.max_notional must be a number >= 0")
        if self.decision == "VETOED" and not self.veto_reason:
            raise ValueError("RiskAuthorization.veto_reason must be non-empty when decision is VETOED")
        _validate_iso(self.expires_at, "RiskAuthorization.expires_at")


@dataclass(frozen=True)
class OrderIntent:
    envelope: ContractEnvelope
    authorization_ref: str
    human_approval_ref: str
    instrument_id: str
    side: Literal["BUY", "SELL"]
    quantity: float
    limit_price: Optional[float] = None
    send_enabled: bool = False
    approval_hash: str = ""
    reason_codes: list = field(default_factory=list)

    def __post_init__(self) -> None:
        if not isinstance(self.envelope, ContractEnvelope):
            raise ValueError("OrderIntent.envelope must be a ContractEnvelope")
        _require_non_empty_str(self.authorization_ref, "OrderIntent.authorization_ref")
        _require_non_empty_str(self.human_approval_ref, "OrderIntent.human_approval_ref")
        _require_non_empty_str(self.instrument_id, "OrderIntent.instrument_id")
        if self.side not in ("BUY", "SELL"):
            raise ValueError(f"OrderIntent.side must be one of BUY/SELL: {self.side!r}")
        if not isinstance(self.quantity, (int, float)) or self.quantity <= 0:
            raise ValueError("OrderIntent.quantity must be a number > 0")
        if self.limit_price is not None and self.limit_price <= 0:
            raise ValueError("OrderIntent.limit_price must be > 0 when provided")
        if self.send_enabled is not False:
            raise ValueError(
                "OrderIntent.send_enabled must remain False (HITL_ONLY; ERR_AUTONOMOUS_ORDER_PATH)"
            )


@dataclass(frozen=True)
class ExecutionEvent:
    envelope: ContractEnvelope
    intent_ref: str
    event_type: Literal[
        "INTENT_CREATED",
        "SUBMITTED",
        "ACKNOWLEDGED",
        "REJECTED",
        "PARTIALLY_FILLED",
        "FILLED",
        "CANCEL_REQUESTED",
        "CANCEL_CONFIRMED",
        "LATE_FILL",
        "CORRECTION",
    ]
    quantity: float
    price: float
    broker_event_id: str
    idempotency_key: str

    def __post_init__(self) -> None:
        if not isinstance(self.envelope, ContractEnvelope):
            raise ValueError("ExecutionEvent.envelope must be a ContractEnvelope")
        _require_non_empty_str(self.intent_ref, "ExecutionEvent.intent_ref")
        _require_non_empty_str(self.broker_event_id, "ExecutionEvent.broker_event_id")
        _require_non_empty_str(self.idempotency_key, "ExecutionEvent.idempotency_key")
        if self.event_type not in (
            "INTENT_CREATED",
            "SUBMITTED",
            "ACKNOWLEDGED",
            "REJECTED",
            "PARTIALLY_FILLED",
            "FILLED",
            "CANCEL_REQUESTED",
            "CANCEL_CONFIRMED",
            "LATE_FILL",
            "CORRECTION",
        ):
            raise ValueError(f"ExecutionEvent.event_type is not a canonical execution event: {self.event_type!r}")
        if not isinstance(self.quantity, (int, float)) or self.quantity < 0:
            raise ValueError("ExecutionEvent.quantity must be a number >= 0")
        if not isinstance(self.price, (int, float)) or self.price < 0:
            raise ValueError("ExecutionEvent.price must be a number >= 0")


@dataclass(frozen=True)
class PositionState:
    envelope: ContractEnvelope
    symbol: str
    quantity: float
    avg_price: float
    gross_value: float
    unrealized_pnl: float
    reconciled: bool

    def __post_init__(self) -> None:
        if not isinstance(self.envelope, ContractEnvelope):
            raise ValueError("PositionState.envelope must be a ContractEnvelope")
        _require_non_empty_str(self.symbol, "PositionState.symbol")
        if not isinstance(self.quantity, (int, float)):
            raise ValueError("PositionState.quantity must be a number")
        if not isinstance(self.avg_price, (int, float)) or self.avg_price < 0:
            raise ValueError("PositionState.avg_price must be a number >= 0")
        if not isinstance(self.gross_value, (int, float)):
            raise ValueError("PositionState.gross_value must be a number")
        if not isinstance(self.unrealized_pnl, (int, float)):
            raise ValueError("PositionState.unrealized_pnl must be a number")
        if not isinstance(self.reconciled, bool):
            raise ValueError("PositionState.reconciled must be a bool")


@dataclass(frozen=True)
class HumanApproval:
    envelope: ContractEnvelope
    proposal_ref: str
    decision: Literal["ACK", "REJECT", "EXPIRED"]
    approver_role: str
    reason: str
    expires_at: str

    def __post_init__(self) -> None:
        if not isinstance(self.envelope, ContractEnvelope):
            raise ValueError("HumanApproval.envelope must be a ContractEnvelope")
        _require_non_empty_str(self.proposal_ref, "HumanApproval.proposal_ref")
        _require_non_empty_str(self.approver_role, "HumanApproval.approver_role")
        _require_non_empty_str(self.reason, "HumanApproval.reason")
        if self.decision not in ("ACK", "REJECT", "EXPIRED"):
            raise ValueError(
                f"HumanApproval.decision must be one of ACK/REJECT/EXPIRED: {self.decision!r}"
            )
        _validate_iso(self.expires_at, "HumanApproval.expires_at")