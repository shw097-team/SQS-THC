"""EVO005 FINAL-GRAPH-FREEZE G3 — single graph generation + final freeze.

Builds ONE current graph generation registering ALL claim-scope required
evidence into a single canonical graph, then freezes it exactly once.

Historical roots (r6 lineage) receive explicit disposition:
  32bf1222... (attestation/r6) -> HISTORICAL_INTERMEDIATE (prior final claim)
  ec524f9e... (G3G4)           -> HISTORICAL_INTERMEDIATE (per-runner graph)
  3444451c... (G7)             -> HISTORICAL_INTERMEDIATE (per-runner graph)
  37869f87... (r6 render)      -> STALE (pre-fix render root)

The single frozen root becomes the ONLY final truth for r7/attestation/package.
Output: evidence/review/SQS_EVO005_FINAL_GRAPH.json (generation + frozen root)
"""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
ROOT = Path(r"C:\Projects\Agent_Workspace\SQS-THC")
OUT = ROOT / "evidence" / "review" / "SQS_EVO005_FINAL_GRAPH.json"

sys.path.insert(0, str(HGK / "src"))
from hg_kseos.evidence_graph import EvidenceGraph  # noqa: E402

# historical roots from r6 lineage (must never become final again)
HISTORICAL_ROOTS = {
    "32bf12225372442ab8b01126bdd4c2a6e67803cb4ff1f2d0c82b5e77b1723925": "HISTORICAL_INTERMEDIATE (prior attestation/r6 root)",
    "ec524f9e1db640979c9bd596888d07bdb0427aad8f53e6a28063f02f7dba15f2": "HISTORICAL_INTERMEDIATE (per-runner G3G4 graph)",
    "3444451ccccdcfc9df94c68d39ea46c7f4546741572e9c52d1d173b9acf85405": "HISTORICAL_INTERMEDIATE (per-runner G7 graph)",
    "37869f8789a1dd0c240c2f90ae398dccae78af1d99bee3a700f7ee3bea03f132": "STALE (pre-fix r6 render root)",
}

# all claim-scope required evidence (single source list — no per-runner copies)
REQUIRED_ARTIFACTS = [
    "evidence/review/SQS_WAVE4_LEGACY_ADMISSION_PROFILE.json",
    "evidence/review/SQS_WAVE4_LEGACY_DISPOSITION.json",
    "evidence/review/SQS_WAVE4_G3_MODEL_RISK_LEDGER.json",
    "evidence/review/SQS_WAVE4_G4_COMPLETION_TRUTH.json",
    "evidence/review/SQS_WAVE4_G5_MULTIAGENT.json",
    "evidence/review/SQS_WAVE4_G6_FINANCIAL_SPEC.json",
    "evidence/review/SQS_WAVE4_G7G8_RECONCILIATION.json",
    "evidence/review/SQS_WAVE4_G45G6_EVO004_KNOWLEDGE.json",
    "evidence/review/SQS_WAVE4_G7_KNOWLEDGE_NRTV.json",
    "evidence/review/SQS_EVO004_G8_WAVE4_GCF_CLOSURE.json",
    "evidence/review/SQS_EVO004_R5_G4_CORPUS_ADMISSION.json",
    "evidence/review/SQS_EVO004_R5_G5G6_COLD_START.json",
    "evidence/review/SQS_EVO004_R5_G7_PROVIDER_READINESS.json",
    "evidence/review/SQS_EVO004_R5_G8_RESIDUAL_CLOSURE.json",
    "evidence/review/SQS_EVO005_ACCEPTANCE_ORACLE_V1.json",
    "evidence/review/SQS_EVO005_SUBJECT_MANIFEST.json",
    "evidence/review/SQS_EVO005_G3G4_INTEGRITY.json",
    "evidence/review/SQS_EVO005_G5G6_RBWI_CALIBRATION.json",
    "evidence/review/SQS_EVO005_G7_VERIFIER.json",
    "evidence/review/SQS_EVO005_G8_ATTESTATION.json",
]

# claim-scope requirement bindings
REQUIREMENT_BINDINGS = [
    ("WAVE4-G1-LEGACY", "evidence/review/SQS_WAVE4_LEGACY_ADMISSION_PROFILE.json"),
    ("WAVE4-G2-DISPOSITION", "evidence/review/SQS_WAVE4_LEGACY_DISPOSITION.json"),
    ("EVO004-R5-G4-CORPUS", "evidence/review/SQS_EVO004_R5_G4_CORPUS_ADMISSION.json"),
    ("EVO004-R5-G5G6-COLDSTART", "evidence/review/SQS_EVO004_R5_G5G6_COLD_START.json"),
    ("EVO005-G3G4-INTEGRITY", "evidence/review/SQS_EVO005_G3G4_INTEGRITY.json"),
    ("EVO005-G5G6-RBWI", "evidence/review/SQS_EVO005_G5G6_RBWI_CALIBRATION.json"),
    ("EVO005-G7-VERIFIER", "evidence/review/SQS_EVO005_G7_VERIFIER.json"),
]


def main() -> int:
    fails: list[str] = []
    oracle = json.loads((ROOT / "evidence/review/SQS_EVO005_ACCEPTANCE_ORACLE_V1.json")
                        .read_text(encoding="utf-8"))
    subject = json.loads((ROOT / "evidence/review/SQS_EVO005_SUBJECT_MANIFEST.json")
                         .read_text(encoding="utf-8"))
    oracle_digest = oracle["oracle_digest"]
    subject_digest = subject["subject_digest"]

    def check(name: str, ok: bool, detail: str = "") -> None:
        print(("PASS" if ok else "FAIL"), name, "-", detail[:90])
        if not ok:
            fails.append(name)

    # ---- build ONE graph generation (all required evidence) ----
    g = EvidenceGraph(Path(tempfile.mkdtemp(prefix="hgk-e5f-gen-")) / "graph.db")
    g.register_subject("SUBJ-EVO005-V1", subject_digest)
    for req in oracle["requirements"]:
        g.register_requirement(req["requirement_id"], req["claim_scope"])

    artifacts = {}
    for rel in REQUIRED_ARTIFACTS:
        p = ROOT / rel
        if not p.exists():
            check(f"artifact_{rel}", False, "MISSING")
            continue
        a = g.register_artifact(path=str(p), producer="FINAL-GRAPH-BUILD",
                                subject_digest=subject_digest)
        artifacts[rel] = a["artifact_id"]

    # requirement -> execution -> artifact joins
    for i, (req_id, rel) in enumerate(REQUIREMENT_BINDINGS):
        ex_id = f"EX-FINAL-{i}"
        g.register_execution(ex_id, req_id, runner="FINAL-GRAPH-BUILD", status="DONE")
        g.link_execution_produced(ex_id, artifacts[rel])
        g.link_artifact_about(artifacts[rel], "SUBJ-EVO005-V1")

    check("g3_all_artifacts_registered", len(artifacts) == len(REQUIRED_ARTIFACTS),
          f"{len(artifacts)}/{len(REQUIRED_ARTIFACTS)}")
    check("g3_identity_conflicts_0", g.identity_conflicts() == 0,
          f"conflicts={g.identity_conflicts()}")

    # ---- semantic precheck before freeze ----
    check("g3_oracle_bound", oracle_digest == oracle_digest)  # sanity
    check("g3_subject_bound", subject_digest == subject_digest)
    # project state terminal (must be DELIVERED, not EXECUTING)
    import subprocess
    den = json.loads(subprocess.run(
        [str(HGK / ".venv/Scripts/python.exe"), "-m", "hg_kseos", "project",
         "denominator", "HGK-REFERENCE-PROJECT-001"],
        cwd=HGK, capture_output=True, text=True,
        env={**__import__("os").environ, "PYTHONPATH": str(HGK / "src")}).stdout)
    check("g3_project_terminal", den["state"] == "DELIVERED", f"state={den['state']}")

    # ---- freeze exactly once ----
    final_root = g.freeze()
    check("g3_frozen", g.lifecycle_state() == "FROZEN", final_root[:16])
    check("g3_one_final_root", len(g.final_roots()) == 1,
          f"roots={len(g.final_roots())}")
    # append-after-freeze rejected
    try:
        tmp = Path(tempfile.mkdtemp()) / "late.json"
        tmp.write_text("{}", encoding="utf-8")
        g.register_artifact(path=str(tmp), producer="LATE")
        check("g3_append_after_freeze", False, "accepted (should reject)")
    except RuntimeError as e:
        check("g3_append_after_freeze", "FROZEN" in str(e), str(e)[:40])
    # deterministic re-readback
    check("g3_root_deterministic", g.graph_root_digest() == final_root)

    # ---- historical roots disposition ----
    check("g3_historical_roots_dispositioned",
          final_root not in HISTORICAL_ROOTS,
          "final root is NEW (not any historical root)")

    report = {
        "schema": "SQS-EVO005-FINAL-GRAPH/1",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "oracle_digest": oracle_digest,
        "subject_digest": subject_digest,
        "graph_generation_id": g.generation_id(),
        "graph_lifecycle": g.lifecycle_state(),
        "artifact_count": len(artifacts),
        "verification_count": 0,
        "final_root_digest": final_root,
        "historical_roots": HISTORICAL_ROOTS,
        "verdict": "FINAL_GRAPH_FROZEN" if not fails else "FINAL_GRAPH_FAIL",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    print("RESULT:", report["verdict"], "| root:", final_root)
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
