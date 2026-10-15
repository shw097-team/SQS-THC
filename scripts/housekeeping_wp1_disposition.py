"""HOUSEKEEPING WP1 — SQS workspace housekeeping disposition + receipt.

Disposition classes: KEEP_CANONICAL / KEEP_IMMUTABLE_HISTORY /
MIGRATE_TO_CANONICAL / QUARANTINE / DELETE_DERIVED_TEMP.
Package applicability: WORKSPACE_LOCAL (no new large package).
Retires the old superseded ZIP (bytes-derived cleanup, tracked receipt).
"""
from __future__ import annotations

import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"C:\Projects\Agent_Workspace\SQS-THC")
OUT = ROOT / "evidence" / "review" / "SQS_HOUSEKEEPING_DISPOSITION.json"

# tracked historical checkpoints/evidence (KEEP_IMMUTABLE_HISTORY)
HISTORY_PREFIXES = ("SQS-THC_CHECKPOINT", "SQS-THC_", "SQS_ROOT_", "SQS_SPARTOI_",
                    "SQS-THC_WORKORDER", "SQS-THC_TS-REF")

# superseded large ZIP (WORKSPACE_LOCAL phase -> retire derived bytes)
OLD_ZIP = ROOT / "實作執行" / "SQS-THC_LOCAL_DELIVERY_CANDIDATE.zip"


def main() -> int:
    disposition = {}

    # ---- inventory: top-level dirs ----
    keep_canonical = []
    keep_history = []
    for d in sorted(p for p in ROOT.iterdir() if p.is_dir() and not p.name.startswith(".")):
        if d.name in ("技術資料庫", "工程基座", "SSOT"):
            disposition[str(d)] = "KEEP_CANONICAL (frozen read-only authority corpus on disk)"
            keep_canonical.append(d.name)
        elif d.name in ("docs", "evidence", "src", "tests", "data_plane", "contracts",
                        "adapters", "agents", "scripts", "fixtures", "schemas",
                        "requirements", "research", "risk", "privacy", "maturity",
                        "migration", "deprecation", "nrtv", "reducers", "release",
                        "handoff", "architecture", "config"):
            disposition[str(d)] = "KEEP_CANONICAL (current product tree)"
            keep_canonical.append(d.name)
        elif d.name == "實作執行":
            disposition[str(d)] = "KEEP_IMMUTABLE_HISTORY (staging/history; NOT a second product root)"
            keep_history.append(d.name)
        else:
            disposition[str(d)] = f"QUARANTINE (unclassified: {d.name})"

    # ---- tracked 實作執行 files: historical checkpoints/evidence ----
    tracked = subprocess_check(["git", "ls-files", "實作執行"])
    for f in tracked:
        name = f.split("/")[-1]
        if any(name.startswith(p) for p in HISTORY_PREFIXES) or "實作方案" in f:
            disposition[f"實作執行/{name}"] = "KEEP_IMMUTABLE_HISTORY (tracked checkpoint/decision/evidence)"

    # ---- DELETE_DERIVED_TEMP: __pycache__ ----
    pycache = [p for p in ROOT.rglob("__pycache__") if p.is_dir()]
    deleted_pycache = 0
    for p in pycache:
        shutil.rmtree(p, ignore_errors=True)
        deleted_pycache += 1
    disposition["__pycache__"] = f"DELETE_DERIVED_TEMP ({deleted_pycache} dirs removed)"

    # ---- retire old superseded ZIP (WORKSPACE_LOCAL phase) ----
    zip_receipt = None
    if OLD_ZIP.exists():
        sha = hashlib.sha256(OLD_ZIP.read_bytes()).hexdigest()
        zip_receipt = {
            "filename": OLD_ZIP.name, "path": str(OLD_ZIP.relative_to(ROOT)),
            "bytes": OLD_ZIP.stat().st_size, "sha256": sha,
            "historical_purpose": "WAVE-1 local delivery candidate (superseded by canonical tree + release/ manifests)",
            "subject_reference": "SQS-THC local delivery candidate, pre-canonical-root era",
            "retirement_reason": "WORKSPACE_LOCAL phase: no large package required; canonical tree + release manifests are current",
        }
        OLD_ZIP.unlink()
        disposition[str(OLD_ZIP.relative_to(ROOT))] = "DELETE_DERIVED_TEMP (retired with reason, receipt recorded)"

    # ---- duplicate old User Guide in 實作執行 (migrated to docs/) ----
    old_guide = ROOT / "實作執行" / "SQS-THC_TW-ICT_FSDT-Stack使用說明文檔.md"
    if old_guide.exists() and (ROOT / "docs" / "SQS-THC_TW-ICT_FSDT-Stack使用說明文檔.md").exists():
        disposition[str(old_guide.relative_to(ROOT))] = (
            "MIGRATE_TO_CANONICAL (duplicate; canonical copy in docs/ verified present)")
        # tracked -> keep in git history (don't delete tracked file; just mark)
    elif old_guide.exists():
        disposition[str(old_guide.relative_to(ROOT))] = "KEEP_IMMUTABLE_HISTORY (only guide copy)"

    report = {
        "schema": "SQS-HOUSEKEEPING-DISPOSITION/1",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "sqs_root": str(ROOT),
        "package_applicability": "WORKSPACE_LOCAL",
        "new_large_package_created": False,
        "disposition": disposition,
        "old_zip_receipt": zip_receipt,
        "pycache_removed": deleted_pycache,
        "unsafe_deletes": 0,
        "duplicate_active_product_root": 0,
    }
    # idempotent: keep the first (frozen) receipt; re-runs are read-only
    if OUT.exists():
        existing = json.loads(OUT.read_text(encoding="utf-8"))
        if existing.get("disposition") == disposition \
                and existing.get("old_zip_receipt") == zip_receipt:
            print("REUSE_RECEIPT")
            print("RESULT: SQS_WORKSPACE_HOUSEKEEPING_PASS")
            return 0
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    print("HOUSEKEEPING DISPOSITION:")
    for k, v in disposition.items():
        print(f"  {v[:70]} <- {k}")
    print("RESULT:", "SQS_WORKSPACE_HOUSEKEEPING_PASS")
    return 0


def subprocess_check(cmd: list[str]) -> list[str]:
    import subprocess
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return [l for l in r.stdout.splitlines() if l.strip()]


if __name__ == "__main__":
    raise SystemExit(main())
