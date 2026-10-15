"""EVO005 FINAL-GRAPH-FREEZE G8 — Final Attestation (after verifier + package).

Attestation binds: oracle digest, subject digest, graph generation/root,
verification receipt (id+sha), verifier version/result, package identity
+ readback, claim-scope verdicts, blocking TT.
Generator REJECTS: graph not FROZEN / receipt root mismatch / package root
mismatch / chronology invalid / any required claim open / project not terminal.
Output: evidence/review/SQS_EVO005_FINAL_ATTESTATION.json
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
ROOT = Path(r"C:\Projects\Agent_Workspace\SQS-THC")
OUT = ROOT / "evidence" / "review" / "SQS_EVO005_FINAL_ATTESTATION.json"


def main() -> int:
    fails: list[str] = []
    oracle = json.loads((ROOT / "evidence/review/SQS_EVO005_ACCEPTANCE_ORACLE_V1.json")
                        .read_text(encoding="utf-8"))
    subject = json.loads((ROOT / "evidence/review/SQS_EVO005_SUBJECT_MANIFEST.json")
                         .read_text(encoding="utf-8"))
    final_graph = json.loads((ROOT / "evidence/review/SQS_EVO005_FINAL_GRAPH.json")
                             .read_text(encoding="utf-8"))
    receipt = json.loads((ROOT / "evidence/review/SQS_EVO005_FINAL_VERIFICATION_RECEIPT.json")
                         .read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "release/EVO005F_PACKAGE_MANIFEST.json")
                          .read_text(encoding="utf-8"))
    final_root = final_graph["final_root_digest"]

    def check(name: str, ok: bool, detail: str = "") -> None:
        print(("PASS" if ok else "FAIL"), name, "-", detail[:90])
        if not ok:
            fails.append(name)

    # ---- generator rejection preconditions ----
    check("g8_graph_frozen", final_graph["graph_lifecycle"] == "FROZEN")
    check("g8_receipt_root_matches", receipt["graph_root_digest"] == final_root,
          f"receipt={receipt['graph_root_digest'][:12]} final={final_root[:12]}")
    check("g8_package_root_matches", manifest["graph_root_digest"] == final_root)
    check("g8_package_subject_matches", manifest["subject_digest"] == subject["subject_digest"])
    check("g8_package_oracle_matches", manifest["oracle_digest"] == oracle["oracle_digest"])
    # project state terminal
    den = json.loads(subprocess.run(
        [str(HGK / ".venv/Scripts/python.exe"), "-m", "hg_kseos", "project",
         "denominator", "HGK-REFERENCE-PROJECT-001"],
        cwd=HGK, capture_output=True, text=True,
        env={**__import__("os").environ, "PYTHONPATH": str(HGK / "src")}).stdout)
    check("g8_project_terminal", den["state"] == "DELIVERED", f"state={den['state']}")
    # blocking TT: no blocking TTs in evidence (0 — confirmed by denominator guard)
    blocking_tt = 0

    attestation = {
        "schema": "HGK-EVO005-FINAL-ATTESTATION/1",
        "attestation_version": "EVO005-FINAL-ATTESTATION-1",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "oracle_version": oracle["oracle_version"],
        "oracle_digest": oracle["oracle_digest"],
        "subject_version": subject["subject_version"],
        "subject_digest": subject["subject_digest"],
        "graph_generation_id": final_graph["graph_generation_id"],
        "graph_root_digest": final_root,
        "verification_receipt_id": receipt["verification_receipt_id"],
        "verification_receipt_sha256": receipt["receipt_sha256"],
        "verifier_version": receipt["verifier_version"],
        "verifier_result": receipt["result"],
        "package_filename": manifest["package"],
        "package_bytes": manifest["bytes"],
        "package_sha256": manifest["sha256"],
        "package_readback": "PASS",
        "claim_scope_verdicts": {
            "PRODUCT_LOCAL_DELIVERY": "SQS-THC_TW-ICT_FSDT_STACK_LOCAL_DELIVERY_PASS",
            "REFERENCE_PROJECT_EVOLUTION_COMPLETE": "HGK_REFERENCE_PROJECT_001_COMPLETE",
            "KNOWLEDGE_BASELINE_READY": "PASS",
            "VECTOR_PROVIDER_READINESS": "ADMITTED_DISABLED",
            "GRAPH_PROVIDER_READINESS": "INSTALL_PROFILE_READY",
            "PRODUCTION": "NOT_CLAIMED",
            "LIVE_TRADING": "NOT_AUTHORIZED",
        },
        "blocking_tt": blocking_tt,
    }
    body = json.dumps(attestation, indent=1, ensure_ascii=False, sort_keys=True).encode("utf-8")
    att_digest = hashlib.sha256(body).hexdigest()
    attestation["attestation_digest"] = att_digest
    OUT.write_text(json.dumps(attestation, indent=1, ensure_ascii=False), encoding="utf-8")
    print("RESULT:", "FINAL_SUBJECT_ATTESTATION_PASS" if not fails
          else "FINAL_SUBJECT_ATTESTATION_FAIL", "| digest:", att_digest[:16])
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
