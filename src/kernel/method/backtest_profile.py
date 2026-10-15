"""B-phase BacktestProfile (DOC-09 CH24.4). DRAFT->VALIDATED->ACTIVE with G06/G09/G11.
Dual-engine: screening (fast) + reference event replay (final baseline)."""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum

class BTState(str, Enum):
    DRAFT="DRAFT"; VALIDATED="VALIDATED"; ACTIVE="ACTIVE"
    STALE="STALE"; SUPERSEDED="SUPERSEDED"; REVOKED="REVOKED"; EXPIRED="EXPIRED"

PROMOTION_GATES = ["G06_PASS","G09_PASS","G11_PASS"]

class BTCError(Exception): pass

@dataclass
class BacktestProfile:
    profile_id: str
    calendar_ref: str
    fill_model_ref: str
    accounting_model_ref: str
    seed_set: list
    engine_identity: str
    engine_version: str
    environment_digest: str
    state: str = "DRAFT"
    parity: dict = field(default_factory=dict)

    def validate_draft_fields(self):
        required = [self.calendar_ref, self.fill_model_ref, self.accounting_model_ref,
                    self.engine_identity, self.engine_version, self.environment_digest]
        if any(not r for r in required):
            raise BTCError("BACKTESTPROFILE_INVALID: missing required field")
        if self.state != "DRAFT":
            raise BTCError("BACKTESTPROFILE_INVALID: state!=DRAFT on construction")

    def run_validation(self, screening_result, reference_replay_result):
        """DRAFT->VALIDATED: 雙引擎 screening + reference replay 比對 (CH24.4)."""
        eq = screening_result == reference_replay_result
        self.parity = {"screening": screening_result, "reference": reference_replay_result,
                       "equivalence": eq}
        if eq:
            self.state = "VALIDATED"
        else:
            raise BTCError("BACKTESTPROFILE_STALE: engine parity mismatch (reference is baseline)")
        return self.state

    def activate(self, gates: dict):
        """VALIDATED->ACTIVE: 需 G06/G09/G11 全 PASS (DOC-09 L6190-6193)."""
        if self.state != "VALIDATED":
            raise BTCError("BACKTESTPROFILE_GATE_BLOCK: must be VALIDATED first")
        missing = [g for g in PROMOTION_GATES if not gates.get(g)]
        if missing:
            raise BTCError(f"BACKTESTPROFILE_GATE_BLOCK: missing {missing}")
        self.state = "ACTIVE"
        return self.state
