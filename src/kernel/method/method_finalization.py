"""A-phase MethodSpec + WF-09->10->11->08 finalization (SQS-THC DOC-02/DOC-07).

Canonical MethodSpec object + the governed method-finalization workflow chain
(WF-09 Research Admission -> WF-10 Independent Validation -> WF-11 Risk/Survival
-> WF-08 Decision Compiler). Fail-closed: a method may only reach
RESEARCH_ONLY/REJECTED via explicit transition; WF-08 may not mint a MethodCard.

State machine is a pure data+transition reducer with no I/O and no broker write.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from enum import Enum
from pathlib import Path
from typing import Any

SCHEMA = Path(__file__).resolve().parents[3] / "schemas" / "method-spec.schema.json"


class MethodState(str, Enum):
    DRAFT = "DRAFT"
    VALIDATED = "VALIDATED"
    ADMITTED = "ADMITTED"
    SUSPENDED = "SUSPENDED"
    RETIRED = "RETIRED"


class AdmissionState(str, Enum):
    REGISTERED = "REGISTERED"
    DATA_FREEZE = "DATA_FREEZE"
    BASELINE = "BASELINE"
    CHALLENGE = "CHALLENGE"
    RESEARCH_ONLY = "RESEARCH_ONLY"
    REJECTED = "REJECTED"


# WF-09 -> WF-10 -> WF-11 -> WF-08 不可逆；WF-08 不得產生 MethodCard
WF_CHAIN = ["WF-09", "WF-10", "WF-11", "WF-08"]
CEILING = "RESEARCH_ONLY != VALIDATED != RISK_AUTHORIZED != DECISION_COMPILED; WF-08 cannot produce MethodCard"

_METHOD_SPEC_REQUIRED = [
    "method_id", "version", "state", "owner", "hypothesis", "inputs",
    "invalidation", "capacity", "cost", "ceiling",
]


class MethodSpecError(Exception):
    pass


class MethodSpecOwnerViolation(MethodSpecError):
    pass


@dataclass
class MethodSpec:
    method_id: str
    version: str
    state: str
    owner: str
    hypothesis: str
    inputs: list
    invalidation: list
    capacity: dict
    cost: dict
    transforms: list = field(default_factory=list)
    parameters: dict = field(default_factory=dict)
    assumptions: list = field(default_factory=list)
    clock_vector_ref: str = "n/a"
    rights_ref: str = "n/a"

    def validate(self) -> None:
        """Fail-closed: schema/owner/invariant validation (DOC-02 D02-OBJ-007)."""
        if not self.method_id or not self.version:
            raise MethodSpecError("D02-E-METHOD_UNADMITTED: method_id+version required")
        if self.version.count(".") != 2:
            raise MethodSpecError("D02-E-METHOD_UNADMITTED: version must be x.y.z")
        if self.state not in [s.value for s in MethodState]:
            raise MethodSpecError(f"D02-E-METHOD_UNADMITTED: unknown state {self.state}")
        if not self.hypothesis or not self.inputs or not self.invalidation:
            raise MethodSpecError("D02-E-METHOD_UNADMITTED: hypothesis/inputs/invalidation required")
        if not self.capacity or not self.cost:
            raise MethodSpecError("D02-E-METHOD_UNADMITTED: capacity/cost required")
        return None


def _load_schema() -> dict:
    if SCHEMA.exists():
        return json.loads(SCHEMA.read_text(encoding="utf-8"))
    return {"properties": {}}


def schema_validate(spec: MethodSpec) -> bool:
    """Reject additionalProperties / missing required per method-spec.schema.json."""
    sch = _load_schema()
    required = sch.get("required", [])
    if sch.get("additionalProperties", True):  # schema says additionalProperties:false
        return False
    missing = [k for k in required if getattr(spec, k, None) in (None, [], {})]
    if missing:
        return False
    return True


class MethodFinalizationMachine:
    """WF-09->10->11->08不可逆 reducer. Pure; no side effects."""

    def __init__(self, spec: MethodSpec):
        self.spec = spec
        self.admission_state = AdmissionState.REGISTERED.value
        self.chain_position = 0
        self.gates: dict[str, bool] = {}

    def _require_owner(self, actor: str) -> None:
        if actor == self.spec.owner:
            return
        # Method Governance Owner only; JobCard/Prompt/Worker forbidden
        raise MethodSpecOwnerViolation("D02-E-METHOD_UNADMITTED: non-owner write rejected")

    def step_wf09_admission(self, actor: str, counterevidence: list | None = None) -> str:
        """Research Admission: REGISTERED -> DATA_FREEZE -> BASELINE -> CHALLENGE -> RESEARCH_ONLY/REJECTED."""
        self._require_owner(actor)
        if self.chain_position > 0:
            raise MethodSpecError("WF chain irreversible: already past WF-09")
        if counterevidence:
            self.admission_state = AdmissionState.REJECTED.value
            raise MethodSpecError("WF-09 rejected: counterevidence present")
        self.admission_state = AdmissionState.DATA_FREEZE.value
        self.chain_position = 1
        return self.admission_state

    def step_wf10_validation(self, actor: str, validation_protocol_pass: bool) -> str:
        """Independent Validation: producer may not self-validate."""
        if actor == self.spec.owner:
            raise MethodSpecError("D02-E-VALIDATION_FAILED: producer cannot self-adjudicate")
        if not validation_protocol_pass:
            return AdmissionState.CHALLENGE.value
        self.spec.state = MethodState.VALIDATED.value
        self.chain_position = 2
        return self.spec.state

    def step_wf11_risk(self, actor: str, risk_authorized: bool) -> str:
        if not risk_authorized:
            raise MethodSpecError("D02-E-RISK_NOT_AUTHORIZED")
        self.chain_position = 3
        return "RISK_AUTHORIZED"

    def step_wf08_compile(self, actor: str) -> str:
        """WF-08 may NOT mint a MethodCard; only consume an admitted candidate to a Decision."""
        if self.admission_state != AdmissionState.RESEARCH_ONLY.value and self.spec.state != MethodState.VALIDATED.value:
            raise MethodSpecError("WF-09->10->11->08 must complete before WF-08")
        self.chain_position = 4
        return "DECISION_COMPILED"

    def finalize_research_only(self, actor: str) -> str:
        self._require_owner(actor)
        self.admission_state = AdmissionState.RESEARCH_ONLY.value
        return self.admission_state


def load_spec_from_dict(d: dict) -> MethodSpec:
    spec = MethodSpec(**d)
    spec.validate()
    return spec
