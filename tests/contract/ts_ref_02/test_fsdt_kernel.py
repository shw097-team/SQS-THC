"""Frozen acceptance tests for the FSDT Financial Contract Kernel (CH04).

Codex bounded worker must FILL the test bodies so they pass against the
implemented kernel. Fixtures match P0-CIP CH04 frozen fixtures:
CH04-POS-001 / CH04-NEG-001 / CH04-EDGE-001 / CH04-ADV-001.
"""
import unittest

from kernel.fsdt import (
    AdjustmentAmbiguousError,
    CurrencyMismatchError,
    FinancialClockInvalidError,
    FinancialContract,
    FinancialState,
    InstrumentIdentity,
    PriceQuantityValue,
    compute_value,
    normalize,
    pit_validate,
    validate_contract,
)


def make_instrument() -> InstrumentIdentity:
    return InstrumentIdentity(
        id="ch04-instrument-id-001",
        schema_version="1.0.0",
        currency="TWD",
        price_unit="TWD",
        quantity_unit="shares",
        value_formula="price*quantity*multiplier",
        adjustment_policy="UNADJUSTED",
        financial_clock="2026-08-10T00:00:00+08:00",
    )


def make_contract() -> FinancialContract:
    return FinancialContract(
        id="ch04-contract-001",
        schema_version="1.0.0",
        instrument_id="ch04-instrument-id-001",
        currency="TWD",
        price_unit="TWD",
        quantity_unit="shares",
        value_formula="price*quantity*multiplier",
        adjustment_policy="UNADJUSTED",
        contract_multiplier=1000.0,
    )


class CH04PositiveTests(unittest.TestCase):
    def test_pos_001_valid_contract_passes(self):
        """CH04-POS-001: valid instrument+contract -> CONTRACT_VALID."""
        state = validate_contract(make_contract(), make_instrument())
        self.assertEqual(state, FinancialState.CONTRACT_VALID)

    def test_pos_002_value_formula(self):
        """value = price * quantity * contract_multiplier."""
        pqv = PriceQuantityValue(
            id="ch04-valid-001", schema_version="1.0.0",
            instrument_id="ch04-instrument-id-001",
            price=12.5, quantity=2, contract_multiplier=1000.0,
        )
        self.assertEqual(compute_value(pqv), 25000.0)

    def test_pos_003_normalize_then_pit_validate(self):
        """RAW -> NORMALIZED -> PIT_VALIDATED transition chain."""
        pqv = PriceQuantityValue(
            id="ch04-valid-002", schema_version="1.0.0",
            instrument_id="ch04-instrument-id-001",
            price=12.5, quantity=2, contract_multiplier=1000.0,
        )
        norm = normalize(pqv, make_contract(), make_instrument())
        self.assertEqual(norm.state, FinancialState.NORMALIZED)
        pit = pit_validate(norm, make_instrument())
        self.assertEqual(pit.state, FinancialState.PIT_VALIDATED)


class CH04NegativeTests(unittest.TestCase):
    def test_neg_001_currency_mismatch(self):
        """CH04-NEG-001: adjusted/unadjusted mixed without policy -> ERR_CURRENCY_MISMATCH."""
        instrument = make_instrument()
        contract = FinancialContract(
            id="ch04-invalid-001", schema_version="1.0.0",
            instrument_id="ch04-instrument-id-001",
            currency="USD",  # mismatched
            price_unit="TWD", quantity_unit="shares",
            value_formula="price*quantity*multiplier",
            adjustment_policy="UNADJUSTED", contract_multiplier=1000.0,
        )
        with self.assertRaises(CurrencyMismatchError):
            validate_contract(contract, instrument)

    def test_neg_002_adjustment_ambiguous(self):
        """adjusted price without adjustment_policy -> ERR_ADJUSTMENT_AMBIGUOUS."""
        pqv = PriceQuantityValue(
            id="ch04-invalid-002", schema_version="1.0.0",
            instrument_id="ch04-instrument-id-001",
            price=12.5, quantity=2, contract_multiplier=1000.0,
            adjustment_policy="",  # ambiguous
        )
        with self.assertRaises(AdjustmentAmbiguousError):
            pit_validate(pqv, make_instrument())

    def test_neg_003_clock_invalid(self):
        """reconcile key divergence -> ERR_FINANCIAL_CLOCK_INVALID."""
        pqv = PriceQuantityValue(
            id="ch04-invalid-003", schema_version="1.0.0",
            instrument_id="ch04-instrument-id-001",
            price=12.5, quantity=2, contract_multiplier=1000.0,
            financial_clock="2026-08-09T00:00:00+08:00",  # stale clock
        )
        with self.assertRaises(FinancialClockInvalidError):
            pit_validate(pqv, make_instrument())


class CH04EdgeTests(unittest.TestCase):
    def test_edge_001_corporate_action_between_clocks(self):
        """corporate action effective between event and availability clocks -> ABSTAIN_OR_DEGRADED_WITH_TT."""
        pqv = PriceQuantityValue(
            id="ch04-edge-001", schema_version="1.0.0",
            instrument_id="ch04-instrument-id-001",
            price=12.5, quantity=2, contract_multiplier=1000.0,
            adjustment_policy="CORPORATE_ACTION_PENDING",
        )
        # contract either abstains (raises) or degrades with TT marker, never silent pass
        with self.assertRaises(Exception):
            pit_validate(pqv, make_instrument())


class CH04AdversarialTests(unittest.TestCase):
    def test_adv_001_forged_owner_rejected(self):
        """CH04-ADV-001: forged owner_id must be rejected."""
        instrument = make_instrument()
        forged = InstrumentIdentity(
            id="ch04-instrument-id-001", schema_version="1.0.0",
            currency="TWD", price_unit="TWD", quantity_unit="shares",
            value_formula="price*quantity*multiplier",
            adjustment_policy="UNADJUSTED", financial_clock="2026-08-10T00:00:00+08:00",
            owner_id="attacker",
        )
        with self.assertRaises(Exception):
            validate_contract(make_contract(), forged)


if __name__ == "__main__":
    unittest.main()
