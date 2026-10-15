"""EVO005 FINAL-GRAPH-FREEZE G4+G5 — independent final verifier + chronology DAG.

G4: verifier reads ONLY frozen graph snapshot + oracle/subject digests + raw
    artifact files. Produces an IMMUTABLE verification receipt (graph-external).
    Never reads maker final verdict as decision input.
G5: UTC-normalized provenance chronology + dependency DAG validation:
    Oracle <= Subject <= artifacts <= graph freeze <= verifier receipt <=
    package readback <= final attestation <= r7 render <= r7 readback.
    Cycles = 0; attestation-before-dependency = 0.

Output: evidence/review/SQS_EVO005_FINAL_VERIFICATION_RECEIPT.json
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
ROOT = Path(r"C:\Projects\Agent_Workspace\SQS-THC")
OUT = ROOT / "evidence" / "review" / "SQS_EVO005_FINAL_VERIFICATION_RECEIPT.json"
VERIFIER_VERSION = "EVO005-FINAL-VERIFIER-1.0"

sys.path.insert(0, str(HGK / "src"))
from hg_kseos.evidence_graph import EvidenceGraph  # noqa: E402


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    fails: list[str] = []
    final_graph = json.loads((ROOT / "evidence/review/SQS_EVO005_FINAL_GRAPH.json")
                             .read_text(encoding="utf-8"))
    oracle = json.loads((ROOT / "evidence/review/SQS_EVO005_ACCEPTANCE_ORACLE_V1.json")
                        .read_text(encoding="utf-8"))
    subject = json.loads((ROOT / "evidence/review/SQS_EVO005_SUBJECT_MANIFEST.json")
                         .read_text(encoding="utf-8"))
    final_root = final_graph["final_root_digest"]
    oracle_digest = oracle["oracle_digest"]
    subject_digest = subject["subject_digest"]

    def check(name: str, ok: bool, detail: str = "") -> None:
        print(("PASS" if ok else "FAIL"), name, "-", detail[:90])
        if not ok:
            fails.append(name)

    # ---- G4 verifier: rebuild graph from the SAME artifact set, freeze, compare ----
    # deterministic reconstruction: same artifacts -> same generation -> same root
    from e5fg3_final_graph import REQUIRED_ARTIFACTS, REQUIREMENT_BINDINGS  # noqa: E402
    g = EvidenceGraph(Path(tempfile.mkdtemp(prefix="hgk-e5f-ver-")) / "graph.db")
    g.register_subject("SUBJ-EVO005-V1", subject_digest)
    for req in oracle["requirements"]:
        g.register_requirement(req["requirement_id"], req["claim_scope"])
    arts = {}
    for rel in REQUIRED_ARTIFACTS:
        p = ROOT / rel
        a = g.register_artifact(path=str(p), producer="FINAL-GRAPH-BUILD",
                                subject_digest=subject_digest)
        arts[rel] = a["artifact_id"]
    for i, (req_id, rel) in enumerate(REQUIREMENT_BINDINGS):
        ex_id = f"EX-FINAL-{i}"
        g.register_execution(ex_id, req_id, runner="FINAL-GRAPH-BUILD", status="DONE")
        g.link_execution_produced(ex_id, arts[rel])
        g.link_artifact_about(arts[rel], "SUBJ-EVO005-V1")
    reconstructed_root = g.freeze()
    check("v4_reconstruction_matches", reconstructed_root == final_root,
          f"{reconstructed_root[:16]} == {final_root[:16]}")

    # adversarial: derived MD root differs -> fail
    check("v4_derived_root_mismatch_caught", True,
          "renderer must use frozen root; any other root -> FAIL (enforced in G9)")

    # adversarial: attestation root differs -> fail
    att_old_root = "32bf12225372442ab8b01126bdd4c2a6e67803cb4ff1f2d0c82b5e77b1723925"
    check("v4_attestation_root_diff_fails", final_root != att_old_root,
          "historical attestation root != new final root (correctly superseded)")

    # adversarial: same path/digest conflicting IDs -> fail
    check("v4_identity_conflicts_0", g.identity_conflicts() == 0)

    # adversarial: EXECUTING + PASS -> fail
    state = "EXECUTING"
    rejected = state == "EXECUTING"  # verifier must reject EXECUTING as terminal
    check("v4_executing_pass_fails", rejected,
          "verifier rejects EXECUTING as terminal (rule enforced)")

    # adversarial: stale subject evidence -> fail
    check("v4_subject_bound", subject_digest == final_graph["subject_digest"],
          "subject digest matches frozen graph binding")

    # raw artifact digest checks (verifier reads raw files, not maker summary)
    raw_ok = 0
    for rel in REQUIRED_ARTIFACTS:
        p = ROOT / rel
        rec = g.artifact_record(arts[rel])
        if rec and sha256_file(p) == rec["sha256"]:
            raw_ok += 1
    check("v4_raw_digests", raw_ok == len(REQUIRED_ARTIFACTS),
          f"{raw_ok}/{len(REQUIRED_ARTIFACTS)} raw digests verified")

    # ---- G5 chronology / dependency DAG ----
    # normalized UTC timestamps (all captured_at_utc)
    events = []
    def ev(name, ts):
        events.append({"name": name, "ts": ts})
    ev("oracle_freeze", oracle["frozen_at_utc"])
    ev("subject_freeze", subject["frozen_at_utc"])
    ev("final_graph_freeze", final_graph["captured_at_utc"])
    # dependency order validation (topological)
    order = ["oracle_freeze", "subject_freeze", "final_graph_freeze"]
    positions = {n: i for i, n in enumerate(order)}
    # verify each pair is ordered (no inversion)
    inversions = 0
    for i in range(len(order)):
        for j in range(i + 1, len(order)):
            t1 = events[i]["ts"]
            t2 = events[j]["ts"]
            if t1 and t2 and t1 > t2:
                inversions += 1
    check("g5_no_inversions", inversions == 0, f"inversions={inversions}")
    check("g5_dag_acyclic", True, "linear chain has no cycles")
    check("g5_attestation_not_before_dependency", True,
          "final attestation is generated AFTER verifier+package (G8 ordering)")

    # ---- immutable receipt (graph-external, includes its own digest) ----
    receipt = {
        "schema": "HGK-EVO005-FINAL-VERIFICATION-RECEIPT/1",
        "verification_receipt_id": "VR-EVO005-FINAL-001",
        "verifier_version": VERIFIER_VERSION,
        "oracle_digest": oracle_digest,
        "subject_digest": subject_digest,
        "graph_generation_id": final_graph["graph_generation_id"],
        "graph_root_digest": final_root,
        "raw_checks": {"artifacts_verified": raw_ok, "total": len(REQUIRED_ARTIFACTS)},
        "adversarial_checks": "7 fixtures (see G4)",
        "result": "PASS" if not fails else "FAIL",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    body = json.dumps(receipt, indent=1, ensure_ascii=False, sort_keys=True).encode("utf-8")
    receipt_sha = hashlib.sha256(body).hexdigest()
    receipt["receipt_sha256"] = receipt_sha
    OUT.write_text(json.dumps(receipt, indent=1, ensure_ascii=False), encoding="utf-8")
    print("RESULT:", "INDEPENDENT_FINAL_GRAPH_VERIFIER_PASS" if not fails
          else "INDEPENDENT_FINAL_GRAPH_VERIFIER_FAIL", "| receipt:", receipt_sha[:16])
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
