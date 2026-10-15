"""B-phase BacktestProfile tests (DOC-09 CH24.4)."""
import sys, unittest
sys.path.insert(0, r"C:\Projects\Agent_Workspace\SQS-THC\src")
from kernel.method.backtest_profile import BacktestProfile, BTCError, PROMOTION_GATES

def mk():
    return BacktestProfile("BP-01","TWSE_CAL","FILL","ACCT",[42],"duckdb","1.5.5","env-digest")

class TestBacktestProfile(unittest.TestCase):
    def test_draft_valid(self):
        p = mk(); p.validate_draft_fields(); self.assertEqual(p.state,"DRAFT")
    def test_missing_field_fails(self):
        p = mk(); p.calendar_ref=""
        with self.assertRaises(BTCError): p.validate_draft_fields()
    def test_validation_parity_pass(self):
        p=mk(); p.validate_draft_fields()
        self.assertEqual(p.run_validation("h1","h1"),"VALIDATED")
    def test_parity_mismatch_fails(self):
        p=mk(); p.validate_draft_fields()
        with self.assertRaises(BTCError): p.run_validation("h1","h2")
    def test_activate_requires_all_gates(self):
        p=mk(); p.validate_draft_fields(); p.run_validation("h","h")
        with self.assertRaises(BTCError): p.activate({"G06_PASS":True,"G09_PASS":True})
    def test_activate_pass(self):
        p=mk(); p.validate_draft_fields(); p.run_validation("h","h")
        self.assertEqual(p.activate({g:True for g in PROMOTION_GATES}),"ACTIVE")

if __name__=="__main__": unittest.main()
