"""Frozen acceptance tests for the Capability / Tool Lifecycle kernel (CH16).

Fixtures match P0-CIP CH16 frozen fixtures:
CH16-POS-001 / CH16-NEG-001 / CH16-EDGE-001 / CH16-ADV-001.
"""
import unittest

from kernel.capability import (
    CapabilitySlot,
    ExportUnreadableError,
    NativeControlUnsuppressedError,
    ProviderUnqualifiedError,
    QualificationReceipt,
    ToolDecisionCard,
    designate,
    finalize,
    qualify,
)


def make_slot(**kw) -> CapabilitySlot:
    base = dict(
        id="ch16-slot-001", schema_version="1.0.0",
        capability_id="ch16-capability-id-001",
        component_id="ch16-component-id-001",
        skill_id="ch16-skill-id-001",
        provider_id="ch16-provider-id-001",
        tool_decision_id="ch16-tool-decision-id-001",
    )
    base.update(kw)
    return CapabilitySlot(**base)


def make_receipt(**kw) -> QualificationReceipt:
    base = dict(
        id="ch16-receipt-001", schema_version="1.0.0",
        capability_id="ch16-capability-id-001",
        skill_id="ch16-skill-id-001",
        provider_id="ch16-provider-id-001",
        tool_decision_id="ch16-tool-decision-id-001",
    )
    base.update(kw)
    return QualificationReceipt(**base)


class CH16PositiveTests(unittest.TestCase):
    def test_pos_001_qualified_pipeline(self):
        """CH16-POS-001: designate -> qualify -> QUALIFIED."""
        slot = make_slot()
        d = designate(slot)
        self.assertEqual(d.admission_status, "DESIGNATED")
        r = make_receipt(admission_status="QUALIFYING", exit_manifest="exit-manifest.json")
        q = qualify(d, r)
        self.assertEqual(q.admission_status, "QUALIFIED")

    def test_pos_002_finalize_allowed(self):
        """disposition ALLOWED + QUALIFIED + exit manifest -> final."""
        card = ToolDecisionCard(
            id="ch16-card-001", schema_version="1.0.0",
            component_id="ch16-component-id-001", skill_id="ch16-skill-id-001",
            provider_id="ch16-provider-id-001",
            tool_decision_id="ch16-tool-decision-id-001",
            admission_status="QUALIFIED", exit_manifest="exit-manifest.json",
            disposition="ALLOWED",
        )
        self.assertEqual(finalize(card), card)


class CH16NegativeTests(unittest.TestCase):
    def test_neg_001_provider_unqualified(self):
        """CH16-NEG-001: installed tool treated as admitted -> ERR_PROVIDER_UNQUALIFIED."""
        slot = make_slot(provider_id="unqualified-provider")
        with self.assertRaises(ProviderUnqualifiedError):
            designate(slot)

    def test_neg_002_export_unreadable(self):
        """missing exit manifest -> ERR_EXPORT_UNREADABLE."""
        slot = make_slot()
        d = designate(slot)
        r = make_receipt(exit_manifest="")  # no manifest
        with self.assertRaises(ExportUnreadableError):
            qualify(d, r)

    def test_neg_003_native_control_unsuppressed(self):
        """disposition != ALLOWED -> ERR_NATIVE_CONTROL_UNSUPPRESSED."""
        card = ToolDecisionCard(
            id="ch16-invalid-001", schema_version="1.0.0",
            component_id="ch16-component-id-001", skill_id="ch16-skill-id-001",
            provider_id="ch16-provider-id-001",
            tool_decision_id="ch16-tool-decision-id-001",
            admission_status="QUALIFIED", exit_manifest="exit-manifest.json",
            disposition="PROHIBITED",
        )
        with self.assertRaises(NativeControlUnsuppressedError):
            finalize(card)


class CH16EdgeTests(unittest.TestCase):
    def test_edge_001_qualified_provider_withdrawn(self):
        """qualified provider withdrawn; fallback parity pending -> abstain/degrade."""
        slot = make_slot(provider_id="withdrawn-provider")
        with self.assertRaises(Exception):
            designate(slot)


class CH16AdversarialTests(unittest.TestCase):
    def test_adv_001_forged_owner_rejected(self):
        """CH16-ADV-001: forged owner_id must be rejected."""
        slot = make_slot(owner_id="attacker")
        with self.assertRaises(Exception):
            designate(slot)


if __name__ == "__main__":
    unittest.main()
