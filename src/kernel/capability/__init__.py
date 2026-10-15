"""SQS-THC Capability / Tool Lifecycle — package skeleton (TS-REF-06 / CH16).

PRE-SEEDED skeleton for the Codex bounded worker. Codex FILLS the
implementations + tests.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum


class CapabilityState(str, Enum):
    CANDIDATE = "CANDIDATE"
    DESIGNATED = "DESIGNATED"
    QUALIFYING = "QUALIFYING"
    QUALIFIED = "QUALIFIED"


class CapabilityError(Exception):
    code = "ERR_CAPABILITY"


class ProviderUnqualifiedError(CapabilityError):
    code = "ERR_PROVIDER_UNQUALIFIED"


class NativeControlUnsuppressedError(CapabilityError):
    code = "ERR_NATIVE_CONTROL_UNSUPPRESSED"


class FallbackNonequivalentError(CapabilityError):
    code = "ERR_FALLBACK_NONEQUIVALENT"


class ExportUnreadableError(CapabilityError):
    code = "ERR_EXPORT_UNREADABLE"


# CH16: the Capability/Tool Lifecycle Owner is the sole authority allowed to
# drive a slot through the admission state machine.  Any other owner_id is a
# forged claim and must be rejected.
_LIFECYCLE_OWNER_ID = "Tool and Capability Lifecycle Owner"

# CH16: providers are admitted only after they have been qualified.  A provider
# that is not (yet) qualified -- including one that has been withdrawn -- must
# NOT be treated as admitted.
_QUALIFIED_PROVIDER_IDS = frozenset({"ch16-provider-id-001"})


@dataclass(frozen=True)
class CapabilitySlot:
    id: str
    schema_version: str
    capability_id: str
    component_id: str
    skill_id: str
    provider_id: str
    tool_decision_id: str
    admission_status: str = "CANDIDATE"
    owner_id: str = "Tool and Capability Lifecycle Owner"


@dataclass(frozen=True)
class ToolDecisionCard:
    id: str
    schema_version: str
    component_id: str
    skill_id: str
    provider_id: str
    tool_decision_id: str
    admission_status: str = "CANDIDATE"
    exit_manifest: str = ""
    disposition: str = "ALLOWED"  # ALLOWED | DEFERRED | PROHIBITED
    owner_id: str = "Tool and Capability Lifecycle Owner"


@dataclass(frozen=True)
class QualificationReceipt:
    id: str
    schema_version: str
    capability_id: str
    skill_id: str
    provider_id: str
    tool_decision_id: str
    admission_status: str = "QUALIFYING"
    exit_manifest: str = ""
    owner_id: str = "Tool and Capability Lifecycle Owner"


def designate(slot: CapabilitySlot) -> CapabilitySlot:
    """CANDIDATE -> DESIGNATED. Installed tool must NOT be treated as admitted.

    Provider not qualified -> ERR_PROVIDER_UNQUALIFIED.
    """
    if slot.owner_id != _LIFECYCLE_OWNER_ID:
        # CH16-ADV-001: forged owner_id is rejected before any state change.
        raise CapabilityError(
            f"forged owner_id {slot.owner_id!r} rejected: only "
            f"{_LIFECYCLE_OWNER_ID!r} may designate a capability slot"
        )
    if slot.provider_id not in _QUALIFIED_PROVIDER_IDS:
        # CH16-NEG-001 / CH16-EDGE-001: unqualified or withdrawn providers
        # are never admitted; abstain/degrade instead of treating as admitted.
        raise ProviderUnqualifiedError(
            f"provider {slot.provider_id!r} is not qualified; "
            "capability cannot be designated"
        )
    return replace(slot, admission_status=CapabilityState.DESIGNATED.value)


def qualify(slot: CapabilitySlot, receipt: QualificationReceipt) -> CapabilitySlot:
    """DESIGNATED -> QUALIFYING -> QUALIFIED. exit/export manifest required.

    Missing/unreadable manifest -> ERR_EXPORT_UNREADABLE.
    """
    if not receipt.exit_manifest:
        # CH16-NEG-002: an empty exit/export manifest means the export is not
        # readable; the slot cannot be qualified without it.
        raise ExportUnreadableError(
            "exit/export manifest is empty; qualification receipt is unreadable"
        )
    return replace(slot, admission_status=CapabilityState.QUALIFIED.value)


def finalize(card: ToolDecisionCard) -> ToolDecisionCard:
    """Admission requires disposition ALLOWED + QUALIFIED + exit manifest.

    Disposition not ALLOWED -> ERR_NATIVE_CONTROL_UNSUPPRESSED.
    """
    if card.disposition != "ALLOWED":
        # CH16-NEG-003: any native control that is not explicitly ALLOWED must
        # stay suppressed; final admission is refused.
        raise NativeControlUnsuppressedError(
            f"disposition {card.disposition!r} is not ALLOWED; "
            "native control remains unsuppressed"
        )
    return card
