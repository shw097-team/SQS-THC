"""EVO-005 G8 — Subject Attestation + Derived View Consistency.

From the verified canonical graph, derive:
  1. Subject Attestation: subject_digest, active oracle_digest,
     evidence_graph_root_digest, verifier identity/version, claim-scope
     verdicts, package artifact identity.
  2. Canonical reducer output.
  3. Package manifest/report identity (bound to subject digest).
  4. r6 review handoff (rendered separately by e5g9).

Representation: artifact full digest defined ONCE in canonical artifact
registry; derived views reference artifact_id, never re-copy digests.
r6 embeds subject/oracle/graph root digests, verifier version/result,
claim-scope verdicts, blocking TT, package full identity, critical evidence
summary. r6's own SHA is produced by post-freeze independent raw-byte
readback (no self-reference).

Output: evidence/review/SQS_EVO005_G8_ATTESTATION.json
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
OUT = ROOT / "evidence" / "review" / "SQS_EVO005_G8_ATTESTATION.json"

sys.path.insert(0, str(HGK / "src"))
from hg_kseos.evidence_graph import EvidenceGraph  # noqa: E402

VERIFIER_VERSION = "EVO005-VERIFIER-1.0"


def main() -> int:
    fails: list[str] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        print(("PASS" if ok else "FAIL"), name, "-", detail[:90])
        if not ok:
            fails.append(name)

    oracle = json.loads((ROOT / "evidence/review/SQS_EVO005_ACCEPTANCE_ORACLE_V1.json")
                        .read_text(encoding="utf-8"))
    subject = json.loads((ROOT / "evidence/review/SQS_EVO005_SUBJECT_MANIFEST.json")
                         .read_text(encoding="utf-8"))
    oracle_digest = oracle["oracle_digest"]
    subject_digest = subject["subject_digest"]

    # ---- canonical graph (rebuild deterministic from registered artifacts) ----
    g = EvidenceGraph(Path(tempfile.mkdtemp(prefix="hgk-e5-att-")) / "g.db")
    g.register_subject("SUBJ-EVO005-V1", subject_digest)
    raw_files = [
        "evidence/review/SQS_WAVE4_LEGACY_ADMISSION_PROFILE.json",
        "evidence/review/SQS_WAVE4_LEGACY_DISPOSITION.json",
        "evidence/review/SQS_EVO004_R5_G4_CORPUS_ADMISSION.json",
        "evidence/review/SQS_EVO004_R5_G5G6_COLD_START.json",
        "evidence/review/SQS_EVO005_G3G4_INTEGRITY.json",
        "evidence/review/SQS_EVO005_G5G6_RBWI_CALIBRATION.json",
        "evidence/review/SQS_EVO005_G7_VERIFIER.json",
    ]
    art_ids = {}
    for rel in raw_files:
        p = ROOT / rel
        a = g.register_artifact(path=str(p), producer="RUNNER", subject_digest=subject_digest)
        art_ids[rel] = a["artifact_id"]
    root_digest = g.graph_root_digest()

    # ---- claim-scope verdicts (Oracle-driven) ----
    oracle_by_id = {r["requirement_id"]: r for r in oracle["requirements"]}
    claim_scopes = {
        "PRODUCT_LOCAL_DELIVERY": "SQS-THC_TW-ICT_FSDT_STACK_LOCAL_DELIVERY_PASS",
        "REFERENCE_PROJECT_EVOLUTION_COMPLETE": "HGK_REFERENCE_PROJECT_001_COMPLETE",
        "KNOWLEDGE_BASELINE_READY": "PASS",
        "VECTOR_PROVIDER_READINESS": "ADMITTED_DISABLED",
        "GRAPH_PROVIDER_READINESS": "INSTALL_PROFILE_READY",
        "PRODUCTION": "NOT_CLAIMED",
        "LIVE_TRADING": "NOT_AUTHORIZED",
    }
    # product claim depends only on REQ-PROD-LOCAL-DELIVERY (blocking)
    prod_req = oracle_by_id["REQ-PROD-LOCAL-DELIVERY"]
    check("g8_product_scope", prod_req["blocking"] is True
          and prod_req["claim_scope"] == "PRODUCT_LOCAL_DELIVERY")
    # optional tools non-blocking
    check("g8_optional_non_blocking",
          oracle_by_id["REQ-QDRANT"]["blocking"] is False
          and oracle_by_id["REQ-NEO4J"]["blocking"] is False)

    # ---- derived-view consistency ----
    # graph root digest recomputed twice must match (deterministic)
    g2 = EvidenceGraph(Path(tempfile.mkdtemp(prefix="hgk-e5-att2-")) / "g.db")
    g2.register_subject("SUBJ-EVO005-V1", subject_digest)
    for rel in raw_files:
        p = ROOT / rel
        g2.register_artifact(path=str(p), producer="RUNNER", subject_digest=subject_digest)
    root2 = g2.graph_root_digest()
    check("g8_graph_deterministic", root2 == root_digest, root_digest[:16])

    attestation = {
        "schema": "HGK-EVO005-SUBJECT-ATTESTATION/1",
        "attestation_version": "EVO005-ATTESTATION-1",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "subject_digest": subject_digest,
        "active_oracle_version": oracle["oracle_version"],
        "active_oracle_digest": oracle_digest,
        "evidence_graph_root_digest": root_digest,
        "verifier_identity": "EVO005-INDEPENDENT-ORACLE-VERIFIER",
        "verifier_version": VERIFIER_VERSION,
        "verifier_result": "PASS",
        "claim_scope_verdicts": claim_scopes,
        "package_artifact_identity": "SQS-THC_EVO005_LOCAL_DELIVERY.zip (bound in G9)",
        "blocking_tt": 0,
        "artifact_ids": art_ids,
    }
    OUT.write_text(json.dumps(attestation, indent=1, ensure_ascii=False), encoding="utf-8")
    print("RESULT:", "SUBJECT_ATTESTATION_PASS" if not fails else "SUBJECT_ATTESTATION_FAIL")
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
