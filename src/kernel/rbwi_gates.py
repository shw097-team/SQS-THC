"""SQS-THC RBWI Gates (RBWI v3.0.0 r2) - WO-RBWI-FULLRUN-001.

Implements the 12 non-compensating RBWI gates.  Every gate returns a verdict
dict: {"verdict": ..., "reason_code": str, "detail": str} where verdict is one
of PASS / FAIL / WAIT / NO_TRADE / BLOCK / KILL.  Stdlib only; Python 3.11+.
"""
from __future__ import annotations

from datetime import datetime, timezone

PASS = "PASS"
FAIL = "FAIL"
WAIT = "WAIT"
NO_TRADE = "NO_TRADE"
BLOCK = "BLOCK"
KILL = "KILL"

VERDICTS = frozenset({PASS, FAIL, WAIT, NO_TRADE, BLOCK, KILL})

# Execution state machine: prev_state -> allowed next event types.
EXECUTION_TRANSITIONS = {
    "INTENT_CREATED": frozenset({"SUBMITTED", "REJECTED", "CANCEL_REQUESTED", "CORRECTION"}),
    "SUBMITTED": frozenset({"ACKNOWLEDGED", "REJECTED", "CANCEL_REQUESTED", "LATE_FILL", "CORRECTION"}),
    "ACKNOWLEDGED": frozenset({"PARTIALLY_FILLED", "FILLED", "CANCEL_REQUESTED", "REJECTED", "LATE_FILL", "CORRECTION"}),
    "PARTIALLY_FILLED": frozenset({"PARTIALLY_FILLED", "FILLED", "CANCEL_REQUESTED", "LATE_FILL", "CORRECTION"}),
    "FILLED": frozenset({"LATE_FILL", "CORRECTION"}),
    "REJECTED": frozenset({"CORRECTION"}),
    "CANCEL_REQUESTED": frozenset({"CANCEL_CONFIRMED", "PARTIALLY_FILLED", "FILLED", "LATE_FILL", "CORRECTION"}),
    "CANCEL_CONFIRMED": frozenset({"LATE_FILL", "CORRECTION"}),
    "LATE_FILL": frozenset({"CORRECTION"}),
    "CORRECTION": frozenset(),
}

# Scenario transition map: BASE->{BULL,BEAR,UNKNOWN,TAIL}, BULL/BEAR->{BASE,UNKNOWN,TAIL},
# UNKNOWN->all, TAIL->{UNKNOWN,BASE}.
DEFAULT_ALLOWED_TRANSITIONS = {
    "BASE": frozenset({"BULL", "BEAR", "UNKNOWN", "TAIL"}),
    "BULL": frozenset({"BASE", "UNKNOWN", "TAIL"}),
    "BEAR": frozenset({"BASE", "UNKNOWN", "TAIL"}),
    "UNKNOWN": frozenset({"BASE", "BULL", "BEAR", "UNKNOWN", "TAIL"}),
    "TAIL": frozenset({"UNKNOWN", "BASE"}),
}

_CANDIDATE_CHECKS = (
    "ELIGIBILITY",
    "LIQUIDITY",
    "ALL_IN_COST",
    "CAPACITY",
    "BORROW",
    "RIGHTS",
    "CAPABILITY",
    "EVENT_RISK",
)

_QUALIFICATION_COMPONENTS = (
    "RULE_DATA",
    "CANDIDATE",
    "CONTEXT",
    "SCENARIO",
    "STRUCTURE",
    "LIQUIDITY",
    "DELIVERY",
    "PD_ARRAY",
    "TIME",
    "MODEL",
    "TAIWAN_ADAPTER",
)

_SENTINEL = object()


def _verdict(verdict: str, reason_code: str, detail: str) -> dict:
    if verdict not in VERDICTS:
        raise ValueError(f"Unknown verdict: {verdict!r}")
    return {"verdict": verdict, "reason_code": reason_code, "detail": detail}


def _get(obj, name: str, default=_SENTINEL):
    """Read ``name`` from a dataclass instance or a dict."""
    if isinstance(obj, dict):
        return obj.get(name, default)
    if hasattr(obj, name):
        return getattr(obj, name)
    return default


def _norm(value) -> str:
    """Normalize an enum member or str to its canonical string value."""
    if hasattr(value, "value"):
        return str(value.value)
    if value is None:
        return ""
    return str(value)


def _to_dt(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    try:
        parsed = datetime.fromisoformat(str(value))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _is_expired(expires_at, now) -> bool:
    expiry = _to_dt(expires_at)
    current = _to_dt(now)
    if expiry is None or current is None:
        return False
    return current > expiry


def gate01_rule_data_capability(rule_ok, identity_ok, eligibility_ok, session_ok,
                                rights_ok, data_quality_ok, capability_ok) -> dict:
    """All rule/data capability checks must pass; any failure blocks."""
    checks = (
        ("RULE", rule_ok),
        ("IDENTITY", identity_ok),
        ("ELIGIBILITY", eligibility_ok),
        ("SESSION", session_ok),
        ("RIGHTS", rights_ok),
        ("DATA_QUALITY", data_quality_ok),
        ("CAPABILITY", capability_ok),
    )
    for name, ok in checks:
        if not ok:
            return _verdict(BLOCK, f"RULE_{name}_FAIL", f"Rule/data capability check {name} failed")
    return _verdict(PASS, "RULE_DATA_CAPABILITY_PASS", "All rule/data capability checks passed")


def gate02_context_freshness(transmission_path_count, alternative_explanations,
                             counterevidence_refs, state) -> dict:
    """Weekly context must have >=2 transmission paths, counterevidence, known state."""
    if transmission_path_count < 2:
        return _verdict(WAIT, "TRANSMISSION_PATHS_INSUFFICIENT",
                        f"Transmission path count {transmission_path_count} < 2")
    if not counterevidence_refs:
        return _verdict(WAIT, "COUNTEREVIDENCE_MISSING", "No counterevidence refs provided")
    state_norm = _norm(state).upper()
    if state_norm not in {"RISK_ON", "RISK_OFF", "MIXED", "UNKNOWN", "TAIL"}:
        return _verdict(WAIT, "CONTEXT_STATE_UNKNOWN", f"Context state {state_norm!r} not recognized")
    return _verdict(
        PASS,
        "CONTEXT_FRESHNESS_PASS",
        f"Context fresh: paths={transmission_path_count}, "
        f"alternatives={len(alternative_explanations or [])}",
    )


def gate03_universe_completeness(denominator_count, members) -> dict:
    """Universe membership must match the denominator and carry reason codes."""
    members = members or []
    if len(members) != denominator_count:
        return _verdict(BLOCK, "UNIVERSE_DENOMINATOR_MISMATCH",
                        f"Universe members {len(members)} != denominator {denominator_count}")
    for member in members:
        codes = _get(member, "reason_codes")
        if codes is None or codes is _SENTINEL:
            label = _get(member, "symbol", _get(member, "object_id", "<unknown>"))
            return _verdict(BLOCK, "MEMBER_REASON_MISSING",
                            f"Universe member {label} missing reason_codes")
    return _verdict(PASS, "UNIVERSE_COMPLETENESS_PASS",
                    f"Universe complete: {len(members)} members with reason codes")


def gate04_candidate_admission(checks, tier, has_evidence_dependency_groups,
                               expires_at, now) -> dict:
    """All 8 candidate checks must be PASS/NOT_REQUIRED; tier/evidence/expiry enforced."""
    checks = checks or {}
    for key in _CANDIDATE_CHECKS:
        state_value = checks.get(key, "MISSING")
        if state_value not in ("PASS", "NOT_REQUIRED"):
            return _verdict(NO_TRADE, f"CANDIDATE_{key}_{state_value}",
                            f"Candidate check {key} not passed (state={state_value})")
    tier_norm = _norm(tier).upper()
    if tier_norm in ("EXCLUDE", "QUARANTINE"):
        return _verdict(NO_TRADE, f"TIER_{tier_norm}",
                        f"Candidate tier {tier_norm} is not tradable")
    if not has_evidence_dependency_groups:
        return _verdict(NO_TRADE, "EVIDENCE_DEPENDENCY_MISSING",
                        "Candidate has no evidence dependency groups")
    if _is_expired(expires_at, now):
        return _verdict(NO_TRADE, "CANDIDATE_EXPIRED", f"Candidate expired at {expires_at}")
    return _verdict(PASS, "CANDIDATE_ADMISSION_PASS", "Candidate admitted")


def gate05_bias_validity(bias) -> dict:
    """Bias hypothesis must carry all structural validity fields."""
    fields = (
        ("supporting", _get(bias, "supporting")),
        ("counterevidence", _get(bias, "counterevidence", _get(bias, "contradicting"))),
        ("trigger", _get(bias, "trigger")),
        ("invalidation", _get(bias, "invalidation")),
        ("timeframe_authority_ref", _get(bias, "timeframe_authority_ref")),
    )
    for name, value in fields:
        if value is None or value is _SENTINEL or value == "" or value == []:
            return _verdict(WAIT, f"BIAS_{name.upper()}_MISSING",
                            f"Bias field {name} is missing")
    return _verdict(PASS, "BIAS_VALIDITY_PASS", "Bias hypothesis is structurally valid")


def gate06_scenario_completeness(branches) -> dict:
    """Scenario tree must have exactly the 5 branches with correct branch rules."""
    if not isinstance(branches, dict):
        branches = _get(branches, "branches", None) or {}
    required = {"BASE", "BULL", "BEAR", "UNKNOWN", "TAIL"}
    present = set(branches.keys())
    missing = sorted(required - present)
    extra = sorted(present - required)
    if missing or extra:
        return _verdict(BLOCK, "SCENARIO_BRANCH_SET_INCOMPLETE",
                        f"Scenario branches must be exactly {sorted(required)}; "
                        f"missing={missing}, extra={extra}")
    unknown = str(branches.get("UNKNOWN", "")).upper()
    if not any(keyword in unknown for keyword in ("WAIT", "OBSERVE", "NO_TRADE")):
        return _verdict(BLOCK, "SCENARIO_UNKNOWN_BRANCH_RULE",
                        "UNKNOWN branch must reference WAIT/OBSERVE/NO_TRADE")
    tail = str(branches.get("TAIL", "")).upper()
    if not any(keyword in tail for keyword in ("REDUCE_RISK", "FLATTEN", "NO_TRADE")):
        return _verdict(BLOCK, "SCENARIO_TAIL_BRANCH_RULE",
                        "TAIL branch must reference REDUCE_RISK/FLATTEN/NO_TRADE")
    return _verdict(PASS, "SCENARIO_COMPLETENESS_PASS", "Scenario tree is complete")


def gate07_scenario_transition(old, new, evidence, checker_ack) -> dict:
    """Scenario transitions must be allowed, evidenced, and checker-acked."""
    old_norm = _norm(old).upper()
    new_norm = _norm(new).upper()
    if old_norm == new_norm:
        return _verdict(WAIT, "NO_STATE_CHANGE", f"Scenario already in {old_norm}")
    allowed = DEFAULT_ALLOWED_TRANSITIONS.get(old_norm)
    if allowed is None or new_norm not in allowed:
        return _verdict(BLOCK, "TRANSITION_NOT_ALLOWED",
                        f"Scenario transition {old_norm} -> {new_norm} not allowed")
    if not evidence:
        return _verdict(WAIT, "MISSING_TRANSITION_EVIDENCE",
                        f"No evidence for scenario transition {old_norm} -> {new_norm}")
    if not checker_ack:
        return _verdict(WAIT, "CHECKER_ACK_REQUIRED",
                        "Checker ack required for scenario transition")
    return _verdict(PASS, "SCENARIO_TRANSITION_PASS",
                    f"Scenario transition {old_norm} -> {new_norm} allowed")


def gate08_setup_qualification(component_results, decision) -> dict:
    """All 11 setup components must be VALID and the decision QUALIFIED."""
    component_results = component_results or {}
    for name in _QUALIFICATION_COMPONENTS:
        state_value = component_results.get(name, "MISSING")
        if state_value != "VALID":
            return _verdict(NO_TRADE, f"COMPONENT_{name}_{state_value}",
                            f"Setup component {name} not VALID (state={state_value})")
    decision_norm = _norm(decision).upper()
    if decision_norm != "QUALIFIED":
        return _verdict(NO_TRADE, f"DECISION_{decision_norm}",
                        f"Setup qualification decision {decision_norm} != QUALIFIED")
    return _verdict(PASS, "SETUP_QUALIFICATION_PASS", "Setup qualified on all components")


def gate09_risk_authorization(decision, ruin_invariant, liquidity_risk, event_risk,
                              borrow_risk, daily_loss_remaining, override_class) -> dict:
    """Risk authorization fail-closed across hard risk checks."""
    decision_norm = _norm(decision).upper()
    if decision_norm != "AUTHORIZED":
        return _verdict(NO_TRADE, f"RISK_{decision_norm}",
                        f"Risk decision {decision_norm} != AUTHORIZED")
    for name, value in (
        ("RUIN_INVARIANT", ruin_invariant),
        ("LIQUIDITY_RISK", liquidity_risk),
        ("EVENT_RISK", event_risk),
    ):
        if _norm(value).upper() != PASS:
            return _verdict(NO_TRADE, f"RISK_{name}_FAIL",
                            f"Risk check {name} not PASS (state={value})")
    borrow_norm = _norm(borrow_risk).upper()
    if borrow_norm not in ("PASS", "NOT_REQUIRED"):
        return _verdict(NO_TRADE, "RISK_BORROW_FAIL",
                        f"Borrow risk {borrow_norm} not PASS/NOT_REQUIRED")
    if daily_loss_remaining is None or daily_loss_remaining <= 0:
        return _verdict(NO_TRADE, "DAILY_LOSS_LIMIT_EXHAUSTED",
                        f"Daily loss remaining {daily_loss_remaining} <= 0 or missing")
    if _norm(override_class).upper() != "NON_OVERRIDABLE":
        return _verdict(NO_TRADE, "HARD_RISK_MUST_BE_NON_OVERRIDABLE",
                        f"Override class {override_class} != NON_OVERRIDABLE")
    return _verdict(PASS, "RISK_AUTHORIZATION_PASS", "Risk authorization granted")


def gate10_execution_state(prev_state, event_type, quantity, filled_delta,
                           duplicate_seen) -> dict:
    """Execution events must follow the canonical state machine and fill bounds."""
    if duplicate_seen:
        return _verdict(WAIT, "DUPLICATE_EVENT_IDEMPOTENTLY_IGNORED",
                        "Duplicate execution event; idempotently ignored")
    prev_norm = _norm(prev_state).upper()
    event_norm = _norm(event_type).upper()
    allowed = EXECUTION_TRANSITIONS.get(prev_norm)
    if allowed is None or event_norm not in allowed:
        return _verdict(KILL, "EXECUTION_TRANSITION_INVALID",
                        f"Execution transition {prev_norm} -> {event_norm} invalid")
    if filled_delta > quantity:
        return _verdict(KILL, "FILL_DELTA_EXCEEDS_ORDER_QUANTITY",
                        f"Filled delta {filled_delta} > order quantity {quantity}")
    return _verdict(PASS, "EXECUTION_STATE_PASS",
                    f"Execution transition {prev_norm} -> {event_norm} accepted")


def gate11_reconciliation(net_quantity, external_net, open_order_quantity,
                          external_open, reconciled) -> dict:
    """Internal vs external position and open-order quantities must agree."""
    if net_quantity != external_net:
        return _verdict(KILL, "POSITION_QUANTITY_MISMATCH",
                        f"Net position {net_quantity} != external {external_net}")
    if open_order_quantity != external_open:
        return _verdict(KILL, "OPEN_ORDER_QUANTITY_MISMATCH",
                        f"Open order qty {open_order_quantity} != external {external_open}")
    if not reconciled:
        return _verdict(KILL, "POSITION_NOT_RECONCILED", "Position not reconciled")
    return _verdict(PASS, "RECONCILIATION_PASS", "Position and open orders reconciled")


def gate12_overnight(position_reconciled, fresh_authorization, scenario, long_only,
                     net, after_cutoff) -> dict:
    """Overnight carry requires reconciliation, fresh auth, safe scenario, no cutoff."""
    if not position_reconciled:
        return _verdict(KILL, "POSITION_NOT_RECONCILED",
                        "Position not reconciled before overnight")
    if not fresh_authorization:
        return _verdict(KILL, "OVERNIGHT_AUTHORIZATION_MISSING_OR_STALE",
                        "No fresh authorization for overnight carry")
    scenario_norm = _norm(scenario).upper()
    if scenario_norm in ("UNKNOWN", "TAIL"):
        return _verdict(KILL, f"SCENARIO_{scenario_norm}_PROHIBITS_CARRY",
                        f"Scenario {scenario_norm} prohibits overnight carry")
    if long_only and net < 0:
        return _verdict(KILL, "T1_LONG_ONLY_VIOLATION",
                        f"Long-only violation: net {net} < 0")
    if after_cutoff:
        return _verdict(KILL, "OVERNIGHT_DECISION_AFTER_CUTOFF",
                        "Overnight decision after cutoff")
    return _verdict(PASS, "OVERNIGHT_PASS", "Overnight carry permitted")