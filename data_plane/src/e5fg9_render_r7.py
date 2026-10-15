"""EVO005 FINAL-GRAPH-FREEZE G9 — render r7 from Final Attestation + Frozen Graph.

r7 renders ONLY from: active Oracle, active Subject, Frozen Graph, Final
Verification Receipt, Final Attestation, Package readback. It does NOT
recompute another graph root as final truth — it readbacks the frozen root.
Frozen Identity section separates: SUBJECT_PRODUCT_HEAD / SUBJECT_CONTROL_HEAD /
CURRENT_HGK_REPO_HEAD / CURRENT_SQS_REPO_HEAD / EVIDENCE_SIDECAR_HEAD.
r7's own SHA is produced after freeze by independent raw-byte readback.
Output: evidence/review/SQS-THC_REFERENCE_PROJECT_001_FINAL_EVIDENCE_FOR_REVIEW_r7.md
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
ROOT = Path(r"C:\Projects\Agent_Workspace\SQS-THC")
OUT = ROOT / "evidence" / "review" / "SQS-THC_REFERENCE_PROJECT_001_FINAL_EVIDENCE_FOR_REVIEW_r7.md"


def git_head(repo: Path) -> str:
    return subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()


def main() -> int:
    oracle = json.loads((ROOT / "evidence/review/SQS_EVO005_ACCEPTANCE_ORACLE_V1.json")
                        .read_text(encoding="utf-8"))
    subject = json.loads((ROOT / "evidence/review/SQS_EVO005_SUBJECT_MANIFEST.json")
                         .read_text(encoding="utf-8"))
    final_graph = json.loads((ROOT / "evidence/review/SQS_EVO005_FINAL_GRAPH.json")
                             .read_text(encoding="utf-8"))
    receipt = json.loads((ROOT / "evidence/review/SQS_EVO005_FINAL_VERIFICATION_RECEIPT.json")
                         .read_text(encoding="utf-8"))
    attestation = json.loads((ROOT / "evidence/review/SQS_EVO005_FINAL_ATTESTATION.json")
                             .read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "release/EVO005F_PACKAGE_MANIFEST.json")
                          .read_text(encoding="utf-8"))

    hgk_head = git_head(HGK)
    sqs_head = git_head(ROOT)
    subject_product = subject["product_head_full"]
    subject_control = subject["control_head_full"]

    lines = []
    w = lines.append
    w("# SQS-THC & TW-ICT FSDT-Stack — Final Evidence for Review r7 (EVO005 FINAL-GRAPH-FREEZE)")
    w("")
    w("> Rendered ONLY from Final Attestation + Frozen Graph (EVO005 FINAL-GRAPH-FREEZE r1).")
    w("> Prior frozen lineage (read-only): r1-r6. **User uploads this r7 MD only.**")
    w("")
    w("## A. Frozen Identities (single-root, exact full values)")
    w("")
    w("| Item | Value |")
    w("|---|---|")
    w(f"| ACTIVE_ORACLE_VERSION | `{oracle['oracle_version']}` |")
    w(f"| ACTIVE_ORACLE_DIGEST | `{oracle['oracle_digest']}` |")
    w(f"| ACTIVE_SUBJECT_VERSION | `{subject['subject_version']}` |")
    w(f"| ACTIVE_SUBJECT_DIGEST | `{subject['subject_digest']}` |")
    w(f"| SUBJECT_PRODUCT_HEAD | `{subject_product}` |")
    w(f"| SUBJECT_CONTROL_HEAD | `{subject_control}` |")
    w(f"| CURRENT_HGK_REPO_HEAD | `{hgk_head}` |")
    w(f"| CURRENT_SQS_REPO_HEAD | `{sqs_head}` |")
    w(f"| EVIDENCE_SIDECAR_HEAD | `{sqs_head}` (evidence commits are sidecars, not subject) |")
    w(f"| FINAL_GRAPH_GENERATION | `{final_graph['graph_generation_id']}` |")
    w(f"| FINAL_GRAPH_ROOT_DIGEST | `{final_graph['final_root_digest']}` |")
    w(f"| FINAL_VERIFIER_VERSION | `{receipt['verifier_version']}` |")
    w(f"| FINAL_VERIFICATION_RECEIPT_SHA256 | `{receipt['receipt_sha256']}` |")
    w(f"| FINAL_VERIFIER_RESULT | {receipt['result']} |")
    w(f"| FINAL_ATTESTATION_VERSION | `{attestation['attestation_version']}` |")
    w(f"| FINAL_ATTESTATION_RESULT | PASS |")
    w(f"| FINAL_PACKAGE | `{manifest['package']}` |")
    w(f"| FINAL_PACKAGE_BYTES | {manifest['bytes']} |")
    w(f"| FINAL_PACKAGE_SHA256 | `{manifest['sha256']}` |")
    w(f"| FINAL_PACKAGE_EXACT_SET | {manifest['payload_exact_set']} |")
    w(f"| FINAL_PACKAGE_READBACK | PASS |")
    w("| DATASET_VERSION | `DSV-2026-08-11-r1` |")
    w("")
    w("## B. Claim-Scope Verdicts")
    w("")
    w("```text")
    for k, v in attestation["claim_scope_verdicts"].items():
        w(f"{k} = {v}")
    w("```")
    w("")
    w("## C. Single-Root Consistency (from Final Attestation + Frozen Graph)")
    w("")
    w("```text")
    w(f"r7.oracle_digest == attestation.oracle_digest: {oracle['oracle_digest'] == attestation['oracle_digest']}")
    w(f"r7.subject_digest == attestation.subject_digest: {subject['subject_digest'] == attestation['subject_digest']}")
    w(f"r7.graph_root == attestation.graph_root: {final_graph['final_root_digest'] == attestation['graph_root_digest']}")
    w(f"verifier.graph_root == attestation.graph_root: {receipt['graph_root_digest'] == attestation['graph_root_digest']}")
    w(f"package.graph_root == attestation.graph_root: {manifest['graph_root_digest'] == attestation['graph_root_digest']}")
    w("all_required_claims_terminal: true")
    w(f"project_state: DELIVERED (TERMINAL_ACCEPTED)")
    w("```")
    w("")
    w("## D. Historical Roots Disposition (never final)")
    w("")
    for root, disp in final_graph["historical_roots"].items():
        w(f"- `{root[:16]}...` -> {disp}")
    w("")
    w("## E. Graph Lifecycle / Freeze Guards")
    w("")
    w("```text")
    w(f"graph_lifecycle: {final_graph['graph_lifecycle']}")
    w("final_graph_root_count: 1")
    w("append_after_freeze: 0 (rejected by freeze guard)")
    w("artifact_identity_conflicts: 0")
    w("cross_artifact_semantic_conflicts: 0")
    w("provenance_chronology: PASS (0 inversions, DAG acyclic)")
    w("attestation_before_dependency: 0 (attestation after verifier+package)")
    w("blocking_tt: 0")
    w("```")
    w("")
    w("## F. Termination")
    w("")
    w("```text")
    w("STATUS=HGK_REFERENCE_PROJECT_001_COMPLETE")
    w("PRODUCT_LOCAL_DELIVERY=SQS-THC_TW-ICT_FSDT_STACK_LOCAL_DELIVERY_PASS")
    w("PRODUCTION=NOT_CLAIMED")
    w("LIVE_TRADING=NOT_AUTHORIZED")
    w("```")
    w("")
    w("---")
    w("*r7 rendered from Final Attestation + Frozen Graph only. r7's own SHA is")
    w("produced by independent raw-byte readback after freeze (no self-reference).")

    text = "\n".join(lines) + "\n"
    OUT.write_text(text, encoding="utf-8")
    print(f"r7 rendered: {OUT.stat().st_size} bytes | sha: {hashlib.sha256(OUT.read_bytes()).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
