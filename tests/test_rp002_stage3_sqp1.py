#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SQP1 acceptance predicates + negative fixtures (S3-T001..T011)."""
import json, unittest
from pathlib import Path

SQS = Path(r"C:\Projects\Agent_Workspace\SQS-THC")
PROFILE_ROOT = SQS / "agents" / "profiles"
EXPECTED = ["sqs-orchestrator", "sqs-data-analysis", "sqs-risk"]


class TestSQP1ProfileTeam(unittest.TestCase):
    def test_t001_exactly_3_persistent_profiles(self):
        dirs = sorted(d.name for d in PROFILE_ROOT.iterdir() if d.is_dir())
        self.assertEqual(sorted(EXPECTED), dirs)

    def test_t002_distributions_present_and_schema(self):
        for pid in EXPECTED:
            dist = PROFILE_ROOT / pid / "distribution.yaml"
            self.assertTrue(dist.exists(), f"{pid} distribution missing")
            text = dist.read_text(encoding="utf-8")
            self.assertIn("schema: RP002-PROFILE-RUNTIME-CONTRACT/2", text)
            self.assertIn(f"profile_id: {pid}", text)
            self.assertIn("stack_id: SQS_FINANCIAL", text)

    def test_t003_soul_config_mcp_fixtures_present(self):
        for pid in EXPECTED:
            for name in ["SOUL.md", "config.yaml", "mcp.json", "README.runtime-contract.md"]:
                self.assertTrue((PROFILE_ROOT / pid / name).exists(), f"{pid}/{name} missing")
            self.assertTrue((PROFILE_ROOT / pid / "fixtures").is_dir())

    def test_t004_team_consumed(self):
        team = (SQS / "TEAM.md").read_text(encoding="utf-8")
        for pid in EXPECTED:
            self.assertIn(pid, team)

    def test_t005_stack_manifest_authority_unchanged(self):
        stack = (SQS / "SQS_STACK_MANIFEST.yaml").read_text(encoding="utf-8")
        self.assertIn("financial_truth_owner: SQS_OWNER_BOUND_CONTROL_CORPUS", stack)
        self.assertIn("live_trading: NOT_AUTHORIZED", stack)
        self.assertIn("production_autonomy: NOT_CLAIMED", stack)

    def test_t006_abstraction_mapping_no_profile_explosion(self):
        mapping = (SQS / "SQS_RUNTIME_ABSTRACTION_MAPPING.yaml").read_text(encoding="utf-8")
        self.assertIn("ROLE != PROFILE", mapping)
        self.assertIn("PROFILE != WORKER", mapping)

    def test_t007_role_catalog_valid(self):
        catalog = (SQS / "SQS_MARCA_ROLE_CATALOG.yaml").read_text(encoding="utf-8")
        self.assertIn("persistent_profile_count: 3", catalog)
        self.assertIn("role_is_profile: false", catalog)

    def test_t008_no_4th_profile(self):
        dirs = sorted(d.name for d in PROFILE_ROOT.iterdir() if d.is_dir())
        self.assertEqual(3, len(dirs))

    def test_t009_profile_cannot_promote_financial_truth(self):
        for pid in EXPECTED:
            dist = (PROFILE_ROOT / pid / "distribution.yaml").read_text(encoding="utf-8")
            self.assertIn("FINANCIAL_SPEC_MUTATION", dist)
            self.assertIn("PROMOTION_TRANSACTION", dist)

    def test_t010_sqs_risk_cannot_emit_fabric_acceptance_receipt(self):
        dist = (PROFILE_ROOT / "sqs-risk" / "distribution.yaml").read_text(encoding="utf-8")
        self.assertIn("FABRIC_ACCEPTANCE_RECEIPT", dist)
        soul = (PROFILE_ROOT / "sqs-risk" / "SOUL.md").read_text(encoding="utf-8")
        self.assertIn("Fabric Acceptance Officer", soul)

    def test_t011_topology_and_fast_loop_guard(self):
        topo = (SQS / "SQS_TASK_TOPOLOGY_POLICY.yaml").read_text(encoding="utf-8")
        self.assertIn("FAST_LOOP_TOOL_INSTALL: FORBIDDEN", topo)
        self.assertIn("live_write: FORBIDDEN_FOR_RP002_STAGE3", topo)


if __name__ == "__main__":
    unittest.main()
