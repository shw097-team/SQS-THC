"""A-phase MethodSpec/WF finalization tests (DOC-02 D02-OBJ-007)."""
import sys, unittest, json, tempfile
sys.path.insert(0, r"C:\Projects\Agent_Workspace\SQS-THC\src")
from kernel.method.method_finalization import (
    MethodSpec, MethodFinalizationMachine, MethodSpecError,
    MethodSpecOwnerViolation, schema_validate, MethodState, AdmissionState,
    CEILING)

BASE = dict(method_id="m-w34-overnight-pullback", version="1.0.0", state="DRAFT",
    owner="MethodGovernanceOwner", hypothesis="Overnight pullback to EQ50 reverts",
    inputs=["daily_bars"], invalidation=["trend_break"], capacity={"max_qty":100},
    cost={"fee_bps":14.25,"tax_bps":30,"slippage_bps":5})

class TestMethodSpec(unittest.TestCase):
    def test_valid_spec(self):
        s = MethodSpec(**BASE); s.validate()
        self.assertEqual(s.state, "DRAFT")
    def test_missing_hypothesis_fails(self):
        d = dict(BASE); d["hypothesis"] = ""
        with self.assertRaises(MethodSpecError): MethodSpec(**d).validate()
    def test_non_owner_violation(self):
        s = MethodSpec(**BASE); s.validate()
        m = MethodFinalizationMachine(s)
        with self.assertRaises(MethodSpecOwnerViolation):
            m.step_wf09_admission("intruder")
    def test_wf_chain_irreversible(self):
        s = MethodSpec(**BASE); s.validate()
        m = MethodFinalizationMachine(s)
        m.step_wf09_admission("MethodGovernanceOwner")
        with self.assertRaises(MethodSpecError):
            m.step_wf09_admission("MethodGovernanceOwner")  # re-entry blocked
    def test_wf10_no_self_validate(self):
        s = MethodSpec(**BASE); s.validate()
        m = MethodFinalizationMachine(s)
        m.step_wf09_admission("MethodGovernanceOwner")
        with self.assertRaises(MethodSpecError):
            m.step_wf10_validation("MethodGovernanceOwner", True)
    def test_wf10_independent_validation_then_finalize(self):
        s = MethodSpec(**BASE); s.validate()
        m = MethodFinalizationMachine(s)
        m.step_wf09_admission("MethodGovernanceOwner")
        st = m.step_wf10_validation("IndependentValidationOwner", True)
        self.assertEqual(st, "VALIDATED")
        m.finalize_research_only("MethodGovernanceOwner")
        self.assertEqual(m.admission_state, "RESEARCH_ONLY")
    def test_ceiling(self):
        self.assertIn("RESEARCH_ONLY", CEILING)

if __name__ == "__main__":
    unittest.main()
