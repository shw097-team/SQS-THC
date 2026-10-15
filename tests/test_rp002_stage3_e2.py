# RP002-STAGE3-E2-FOCUSED-TEST/1 - Stack Manifest namespace contract completeness (E2-BS-001)
# Owner doc 18.2 requires sqs.revoked.* exclusion; materialized manifest must declare it.
import unittest
from pathlib import Path

SQS = Path(r"C:\Projects\Agent_Workspace\SQS-THC")


class TestE2StackNamespaceContract(unittest.TestCase):
    def test_e2_001_revoked_namespace_declared(self):
        text = (SQS / "SQS_STACK_MANIFEST.yaml").read_text(encoding="utf-8")
        self.assertIn("revoked_exclusion", text)
        self.assertIn("sqs.revoked.*", text)

    def test_e2_002_revoked_excluded_from_read(self):
        text = (SQS / "SQS_STACK_MANIFEST.yaml").read_text(encoding="utf-8")
        read_block = text.split("read:")[1].split("]")[0]
        self.assertNotIn("sqs.revoked.*", read_block)

    def test_e2_003_lifecycle_declared(self):
        text = (SQS / "SQS_STACK_MANIFEST.yaml").read_text(encoding="utf-8")
        self.assertIn("candidate -> approved", text)
        self.assertIn("revoked (tombstone + audit receipt) -> excluded", text)

    def test_e2_004_existing_namespace_fields_preserved(self):
        text = (SQS / "SQS_STACK_MANIFEST.yaml").read_text(encoding="utf-8")
        self.assertIn("sqs.candidate.*", text)
        self.assertIn("sqs.runtime.*", text)
        self.assertIn("shared.approved.*", text)
        self.assertIn("DOMAIN_OWNER_ONLY", text)

    def test_e2_005_authority_delta_none(self):
        text = (SQS / "SQS_STACK_MANIFEST.yaml").read_text(encoding="utf-8")
        self.assertIn("financial_truth_owner: SQS_OWNER_BOUND_CONTROL_CORPUS", text)
        self.assertIn("live_trading: NOT_AUTHORIZED", text)


if __name__ == "__main__":
    unittest.main()
