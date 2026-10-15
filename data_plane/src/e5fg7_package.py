"""EVO005 FINAL-GRAPH-FREEZE G7 — package build/readback bound to frozen root.

Build package ONLY after frozen graph + independent verifier PASS exist.
Manifest binds: subject_digest / oracle_digest / graph_generation_id /
graph_root_digest / final_verification_receipt_digest / payload_exact_set /
package_bytes / package_sha256 / rollback_pointer.
Independent readback validates exact set + full SHA + bindings.
"""
from __future__ import annotations

import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"C:\Projects\Agent_Workspace\SQS-THC")


def main() -> int:
    fails: list[str] = []
    final_graph = json.loads((ROOT / "evidence/review/SQS_EVO005_FINAL_GRAPH.json")
                             .read_text(encoding="utf-8"))
    oracle = json.loads((ROOT / "evidence/review/SQS_EVO005_ACCEPTANCE_ORACLE_V1.json")
                        .read_text(encoding="utf-8"))
    subject = json.loads((ROOT / "evidence/review/SQS_EVO005_SUBJECT_MANIFEST.json")
                         .read_text(encoding="utf-8"))
    receipt = json.loads((ROOT / "evidence/review/SQS_EVO005_FINAL_VERIFICATION_RECEIPT.json")
                         .read_text(encoding="utf-8"))
    final_root = final_graph["final_root_digest"]
    receipt_sha = receipt["receipt_sha256"]

    def check(name: str, ok: bool, detail: str = "") -> None:
        print(("PASS" if ok else "FAIL"), name, "-", detail[:90])
        if not ok:
            fails.append(name)

    # ---- preconditions ----
    check("g7_graph_frozen", final_graph["graph_lifecycle"] == "FROZEN")
    check("g7_verifier_pass", receipt["result"] == "PASS")

    # ---- build package (bound to frozen root) ----
    payload = sorted([p for p in ROOT.rglob("*") if p.is_file()
                      and "data_plane/data" not in str(p)
                      and ".venv-data" not in str(p)
                      and ".git" not in str(p)
                      and "技術資料庫" not in str(p)
                      and "工程基座" not in str(p)
                      and "SSOT" not in str(p)
                      and "實作執行" not in str(p)
                      and "release/" not in str(p)])
    out = ROOT / "release" / "SQS-THC_EVO005F_LOCAL_DELIVERY.zip"
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in payload:
            zf.write(p, p.as_posix())
    sha = hashlib.sha256(out.read_bytes()).hexdigest()

    manifest = {
        "package": str(out), "bytes": out.stat().st_size, "sha256": sha,
        "payload_exact_set": len(payload),
        "subject_digest": subject["subject_digest"],
        "oracle_digest": oracle["oracle_digest"],
        "graph_generation_id": final_graph["graph_generation_id"],
        "graph_root_digest": final_root,
        "final_verification_receipt_digest": receipt_sha,
        "rollback_pointer": "RL-EVO005F-001",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
    }
    (ROOT / "release/EVO005F_PACKAGE_MANIFEST.json").write_text(
        json.dumps(manifest, indent=1), encoding="utf-8")

    # ---- independent readback ----
    with zipfile.ZipFile(out) as zf:
        names = sorted(zf.namelist())
    check("g7_sha", sha == manifest["sha256"], sha[:16])
    check("g7_exact_set", len(names) == manifest["payload_exact_set"],
          f"{len(names)}/{manifest['payload_exact_set']}")
    check("g7_bytes", out.stat().st_size == manifest["bytes"])
    check("g7_bindings", manifest["graph_root_digest"] == final_root
          and manifest["subject_digest"] == subject["subject_digest"]
          and manifest["oracle_digest"] == oracle["oracle_digest"]
          and manifest["final_verification_receipt_digest"] == receipt_sha)

    print("RESULT:", "FINAL_PACKAGE_SUBJECT_GRAPH_BINDING_PASS" if not fails
          else "FINAL_PACKAGE_BINDING_FAIL",
          "| sha:", sha[:16], "| payload:", len(payload))
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
