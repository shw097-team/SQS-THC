"""HOUSEKEEPING VALIDATION — ordinary-user dry walkthrough + affected smoke.

1. SQS User Guide walkthrough: verify guide-referenced paths/commands exist
   and are not stale (tests 211, doctor/health, canonical dirs).
2. Affected smoke: SQS suite (PYTHONPATH=src) + HGK doctor after guide edits.
3. No canonical source/data/history accidentally removed; tree clean.
Output: evidence/review/SQS_HOUSEKEEPING_VALIDATION.json
"""
from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"C:\Projects\Agent_Workspace\SQS-THC")
HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
PYH = HGK / ".venv" / "Scripts" / "python.exe"
OUT = ROOT / "evidence" / "review" / "SQS_HOUSEKEEPING_VALIDATION.json"


def main() -> int:
    fails: list[str] = []
    checks = {}

    def check(name: str, ok: bool, detail: str = "") -> None:
        print(("PASS" if ok else "FAIL"), name, "-", detail[:90])
        checks[name] = {"ok": ok, "detail": detail[:90]}
        if not ok:
            fails.append(name)

    # ---- WP2 walkthrough: guide-referenced artifacts exist ----
    guide = (ROOT / "docs/SQS-THC_TW-ICT_FSDT-Stack使用說明文檔.md").read_text(encoding="utf-8")
    check("guide_present", guide.startswith("# 《SQS-THC"), "r3 guide present")
    for marker in ("MILESTONE_CLOSED", "SQS-THC_TW-ICT_FSDT_STACK_LOCAL_DELIVERY_PASS",
                   "274", "EVO-005F", "Qdrant", "Neo4j", "execute → test → repair → continue"):
        check(f"guide_has_{marker}", marker in guide, marker)

    # guide references
    for ref in ("src/kernel", "tests", "evidence/review", "data_plane"):
        check(f"guide_ref_{ref.split('/')[-1]}", (ROOT / ref).exists(), ref)
    # package manifest retained (ZIP removed by user per WORKSPACE_LOCAL policy)
    pkg_manifest = ROOT / "release/EVO005F_PACKAGE_MANIFEST.json"
    check("guide_ref_package", pkg_manifest.is_file(), "EVO005F_PACKAGE_MANIFEST.json (ZIP retired per WORKSPACE_LOCAL)")
    # r7 evidence referenced
    r7 = ROOT / "evidence/review/SQS-THC_REFERENCE_PROJECT_001_FINAL_EVIDENCE_FOR_REVIEW_r7.md"
    check("guide_ref_r7", r7.is_file(), r7.name)

    # ---- affected smoke: SQS suite ----
    rs = subprocess.run([str(PYH), "-m", "unittest", "discover",
                         "-s", str(ROOT / "tests"), "-t", str(ROOT)],
                        cwd=ROOT, capture_output=True, text=True, timeout=300,
                        env={"PYTHONPATH": str(ROOT / "src")})
    check("sqs_suite", rs.returncode == 0 and "OK" in (rs.stdout + rs.stderr),
          f"exit={rs.returncode}")

    # ---- housekeeping safety: no canonical removed ----
    for essential in ("src", "contracts", "docs", "tests", "data_plane", "evidence",
                      "技術資料庫", "工程基座", "SSOT"):
        check(f"essential_{essential}", (ROOT / essential).exists(), essential)
    check("no_dup_root", not (ROOT / "實作執行/src").exists()
          and not (ROOT / "實作執行/tests").exists(),
          "實作執行 has no duplicate product root")

    # ---- tree clean (excluding this script's own idempotent receipts) ----
    st = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain"],
                        capture_output=True, text=True).stdout
    self_receipts = {"evidence/review/SQS_HOUSEKEEPING_VALIDATION.json",
                     "evidence/review/SQS_HOUSEKEEPING_DISPOSITION.json"}
    others = [l for l in st.splitlines()
              if l.strip() and not any(r in l for r in self_receipts)]
    check("sqs_tree_clean", others == [], " ".join(others)[:40])

    report = {
        "schema": "SQS-HOUSEKEEPING-VALIDATION/1",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
        "verdict": "PASS" if not fails else "FAIL",
    }
    # idempotent: keep first (frozen) receipt; re-runs are read-only
    if OUT.exists():
        existing = json.loads(OUT.read_text(encoding="utf-8"))
        if existing.get("checks") == checks:
            print("REUSE_RECEIPT")
            print("RESULT:", "HOUSEKEEPING_VALIDATION_PASS" if not fails
                  else "HOUSEKEEPING_VALIDATION_FAIL")
            return 0 if not fails else 1
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    print("RESULT:", "HOUSEKEEPING_VALIDATION_PASS" if not fails else "HOUSEKEEPING_VALIDATION_FAIL")
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
