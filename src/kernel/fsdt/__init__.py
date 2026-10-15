"""SQS-THC FSDT Financial Contract Kernel — package skeleton (TS-REF-02 / CH04).

This file is a PRE-SEEDED skeleton for the Codex bounded worker. The Windows
Codex sandbox cannot CREATE new files, so the contract surface is pre-seeded
and Codex FILLS the implementations + tests.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime
from enum import Enum


class FinancialState(str, Enum):
    RAW = "RAW"
    NORMALIZED = "NORMALIZED"
    PIT_VALIDATED = "PIT_VALIDATED"
    CONTRACT_VALID = "CONTRACT_VALID"


class FSDTKernelError(Exception):
    """Base error for the FSDT Financial Contract Kernel (CH04)."""

    code = "ERR_FSDT_KERNEL"


class CurrencyMismatchError(FSDTKernelError):
    code = "ERR_CURRENCY_MISMATCH"


class AdjustmentAmbiguousError(FSDTKernelError):
    code = "ERR_ADJUSTMENT_AMBIGUOUS"


class FinancialClockInvalidError(FSDTKernelError):
    code = "ERR_FINANCIAL_CLOCK_INVALID"


class OwnerMismatchError(FSDTKernelError):
    """Rejected forged/foreign owner_id (CH04-ADV-001)."""

    code = "ERR_OWNER_MISMATCH"


class CorporateActionAbstainError(FSDTKernelError):
    """Abstain-or-degraded-with-TT marker for pending corporate actions (CH04-EDGE-001)."""

    code = "ERR_ABSTAIN_OR_DEGRADED_WITH_TT"


@dataclass(frozen=True)
class InstrumentIdentity:
    id: str
    schema_version: str
    currency: str
    price_unit: str
    quantity_unit: str
    value_formula: str
    adjustment_policy: str
    financial_clock: str
    owner_id: str = "FSDT Financial Kernel Owner"


@dataclass(frozen=True)
class FinancialContract:
    id: str
    schema_version: str
    instrument_id: str
    currency: str
    price_unit: str
    quantity_unit: str
    value_formula: str
    adjustment_policy: str
    contract_multiplier: float = 1.0
    owner_id: str = "FSDT Financial Kernel Owner"


@dataclass(frozen=True)
class PriceQuantityValue:
    id: str
    schema_version: str
    instrument_id: str
    price: float
    quantity: float
    contract_multiplier: float = 1.0
    currency: str = "TWD"
    adjustment_policy: str = "UNADJUSTED"
    financial_clock: str = "2026-08-10T00:00:00+08:00"
    state: FinancialState = FinancialState.RAW
    owner_id: str = "FSDT Financial Kernel Owner"


KERNEL_OWNER_ID = "FSDT Financial Kernel Owner"
ADJUSTMENT_POLICY_UNADJUSTED = "UNADJUSTED"
ADJUSTMENT_POLICY_ADJUSTED = "ADJUSTED"
ADJUSTMENT_POLICY_CORPORATE_ACTION_PENDING = "CORPORATE_ACTION_PENDING"


def _require_kernel_owner(contract: FinancialContract, instrument: InstrumentIdentity) -> None:
    if contract.owner_id != KERNEL_OWNER_ID or instrument.owner_id != KERNEL_OWNER_ID:
        raise OwnerMismatchError(
            "forged owner_id rejected: owner must be 'FSDT Financial Kernel Owner'"
        )


def _require_currency_match(contract: FinancialContract, instrument: InstrumentIdentity) -> None:
    if contract.currency != instrument.currency:
        raise CurrencyMismatchError(
            f"currency mismatch: contract={contract.currency!r} instrument={instrument.currency!r}"
        )


def _require_adjustment_consistent(contract: FinancialContract, instrument: InstrumentIdentity) -> None:
    if contract.adjustment_policy != instrument.adjustment_policy:
        raise CurrencyMismatchError(
            "adjusted/unadjusted prices mixed without adjustment_policy: "
            f"contract={contract.adjustment_policy!r} instrument={instrument.adjustment_policy!r}"
        )


def _require_value_formula(contract: FinancialContract, instrument: InstrumentIdentity) -> None:
    if not contract.value_formula or contract.value_formula != instrument.value_formula:
        raise FSDTKernelError(
            "value formula not satisfied: "
            f"contract={contract.value_formula!r} instrument={instrument.value_formula!r}"
        )


def _require_valid_clock(clock: str) -> None:
    if not clock or not clock.strip():
        raise FinancialClockInvalidError("financial clock missing/empty")
    try:
        datetime.fromisoformat(clock)
    except (TypeError, ValueError):
        raise FinancialClockInvalidError(f"financial clock malformed: {clock!r}") from None


def _clocks_equal(a: str, b: str) -> bool:
    try:
        ta = datetime.fromisoformat(a)
        tb = datetime.fromisoformat(b)
    except (TypeError, ValueError):
        return False
    return ta == tb


def validate_contract(contract: FinancialContract, instrument: InstrumentIdentity) -> FinancialState:
    """CH04 core predicate: value = price*quantity*multiplier AND currency match AND PIT-valid."""
    _require_kernel_owner(contract, instrument)
    if contract.instrument_id != instrument.id:
        raise FSDTKernelError(
            f"instrument identity mismatch: contract.instrument_id={contract.instrument_id!r} "
            f"instrument.id={instrument.id!r}"
        )
    if contract.schema_version != instrument.schema_version:
        raise FSDTKernelError(
            f"schema version mismatch: contract={contract.schema_version!r} "
            f"instrument={instrument.schema_version!r}"
        )
    _require_currency_match(contract, instrument)
    _require_adjustment_consistent(contract, instrument)
    _require_value_formula(contract, instrument)
    _require_valid_clock(instrument.financial_clock)
    return FinancialState.CONTRACT_VALID


def normalize(pqv: PriceQuantityValue, contract: FinancialContract, instrument: InstrumentIdentity) -> PriceQuantityValue:
    """RAW -> NORMALIZED: bind contract terms + instrument facts onto the quote."""
    if pqv.state is not FinancialState.RAW:
        raise FSDTKernelError(f"normalize requires RAW input, got {pqv.state.value!r}")
    _require_kernel_owner(contract, instrument)
    if pqv.instrument_id != contract.instrument_id or pqv.instrument_id != instrument.id:
        raise FSDTKernelError(
            f"instrument identity mismatch during normalization: pqv={pqv.instrument_id!r} "
            f"contract={contract.instrument_id!r} instrument={instrument.id!r}"
        )
    _require_currency_match(contract, instrument)
    if pqv.currency != contract.currency:
        raise CurrencyMismatchError(
            f"pqv currency mismatch: pqv={pqv.currency!r} contract={contract.currency!r}"
        )
    return replace(
        pqv,
        contract_multiplier=contract.contract_multiplier,
        currency=instrument.currency,
        adjustment_policy=contract.adjustment_policy,
        financial_clock=instrument.financial_clock,
        state=FinancialState.NORMALIZED,
    )


def pit_validate(pqv: PriceQuantityValue, instrument: InstrumentIdentity) -> PriceQuantityValue:
    """NORMALIZED -> PIT_VALIDATED: point-in-time clock + adjustment-policy gates."""
    if pqv.adjustment_policy == ADJUSTMENT_POLICY_CORPORATE_ACTION_PENDING:
        raise CorporateActionAbstainError(
            "ABSTAIN_OR_DEGRADED_WITH_TT: corporate action pending between event and availability clocks"
        )
    if pqv.currency != instrument.currency:
        raise CurrencyMismatchError(
            f"currency mismatch at PIT validation: pqv={pqv.currency!r} instrument={instrument.currency!r}"
        )
    policy = (pqv.adjustment_policy or "").strip()
    if not policy:
        raise AdjustmentAmbiguousError("adjustment_policy empty/ambiguous")
    if policy not in (ADJUSTMENT_POLICY_UNADJUSTED, ADJUSTMENT_POLICY_ADJUSTED):
        raise AdjustmentAmbiguousError(f"adjustment_policy ambiguous: {pqv.adjustment_policy!r}")
    if not _clocks_equal(pqv.financial_clock, instrument.financial_clock):
        raise FinancialClockInvalidError(
            f"financial clock stale/divergent: pqv={pqv.financial_clock!r} "
            f"instrument={instrument.financial_clock!r}"
        )
    return replace(pqv, state=FinancialState.PIT_VALIDATED)


def compute_value(pqv: PriceQuantityValue) -> float:
    """value = price * quantity * contract_multiplier"""
    return float(pqv.price * pqv.quantity * pqv.contract_multiplier)
