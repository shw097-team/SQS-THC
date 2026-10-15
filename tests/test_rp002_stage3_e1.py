# RP002-STAGE3-E1-FOCUSED-TEST/1 - doc currentness regression
# Operability docs must project current accepted knowledge-governance state
# (Stage-2 KG1/F1/CF1 PASS), not the stale DEFERRED_TO_RP002 claim.
import unittest
from pathlib import Path

SQS = Path(r"C:\Projects\Agent_Workspace\SQS-THC")


class TestE1DocCurrentness(unittest.TestCase):
    def test_e1_001_readme_no_stale_deferred_claim(self):
        text = (SQS / "README.md").read_text(encoding="utf-8")
        self.assertNotIn("DEFERRED_TO_RP002", text)

    def test_e1_002_user_guide_no_stale_deferred_claim(self):
        text = (SQS / "docs" / "SQS-THC_TW-ICT_FSDT-Stack使用說明文檔.md").read_text(encoding="utf-8")
        self.assertNotIn("DEFERRED_TO_RP002", text)

    def test_e1_003_docs_project_stage2_knowledge_governance_active(self):
        text = (SQS / "README.md").read_text(encoding="utf-8")
        self.assertIn("KG1", text)
        self.assertIn("SQLite", text)
        self.assertIn("FTS5", text)

    def test_e1_004_provider_states_preserved(self):
        text = (SQS / "README.md").read_text(encoding="utf-8")
        self.assertIn("ADMITTED_DISABLED", text)
        self.assertIn("default OFF", text)


if __name__ == "__main__":
    unittest.main()
