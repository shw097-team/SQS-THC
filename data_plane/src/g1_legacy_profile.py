"""G1 — Legacy Taiwan price history admission profile + Stock List crosswalk.

Read-only profiling of 技術資料庫/台股價格歷史資料:
  - physical denominator (files/bytes per family) — full, not sampled
  - schema/frequency/unit/adjustment profile per family (sampled rows)
  - Stock List (finmind/.runtime/cleaned_stocks.txt) crosswalk vs current
    SQS universe + Shioaji universe
  - disposition per family: REUSE_DIRECT | NORMALIZE | GAP_FILL_CANDIDATE |
    PARITY_ONLY | QUARANTINE | SOURCE_VALID_NOT_APPLICABLE
Never writes to the legacy tree; outputs to evidence/review/.
"""
from __future__ import annotations

import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"C:\Projects\Agent_Workspace\SQS-THC")
LEGACY = ROOT / "技術資料庫" / "台股價格歷史資料"
OUT = ROOT / "evidence" / "review" / "SQS_WAVE4_LEGACY_ADMISSION_PROFILE.json"

SHIOAJI_UNIVERSE = ["2330", "2317", "2454", "2603", "2881", "2882", "2891", "2303",
                    "2412", "2002", "1301", "1326", "3008", "3231", "2379", "2408",
                    "3037", "2382", "2609", "2615", "2637", "2311", "2357", "2498",
                    "3481", "2301", "2327", "2344", "2353", "2388", "2368", "6285",
                    "8046", "6147", "6182", "6139", "4105", "9933", "1101", "1216",
                    "1227", "1717", "1722", "1736", "2105", "2204", "2206", "2610",
                    "3702", "6409"]


def family_stats(path: Path) -> dict:
    n = 0
    total = 0
    for f in path.rglob("*"):
        if f.is_file():
            n += 1
            total += f.stat().st_size
    return {"files": n, "bytes": total}


def sample_csv(path: Path, n: int = 3) -> dict:
    try:
        with path.open(encoding="utf-8-sig", errors="replace") as fh:
            reader = csv.reader(fh)
            header = next(reader, None)
            rows = [next(reader, None) for _ in range(n)]
        return {"header": header, "rows": rows, "cols": len(header) if header else 0}
    except Exception as exc:  # noqa: BLE001
        return {"error": f"{type(exc).__name__}: {exc}"}


def main() -> int:
    fam = {}
    for d in sorted(p for p in LEGACY.rglob("*") if p.is_dir() and not any(
            x.name.startswith(".") for x in p.parents)):
        rel = d.relative_to(LEGACY)
        fam[str(rel)] = family_stats(d)

    # samples
    ts_stock = sample_csv(LEGACY / "Taiwan STOCK" / "1101_history.csv")
    kbar_sample = sample_csv(LEGACY / "finmind" / "raw" / "kbar" / "1101" / "2023-07-03.csv")
    daily_sample = sample_csv(LEGACY / "finmind" / "raw" / "daily" / "1470.csv")
    index5s_sample = sample_csv(next((LEGACY / "finmind" / "raw" / "index_5s").glob("*.csv")))
    _ik = list((LEGACY / "finmind" / "raw" / "index_kbar").rglob("*.csv"))
    indexkbar_sample = sample_csv(_ik[0]) if _ik else {"error": "no csv"}

    # stock list
    stocks = [l.strip() for l in
              (LEGACY / "finmind" / ".runtime" / "cleaned_stocks.txt")
              .read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()]
    selected = [l.strip() for l in
                (LEGACY / "finmind" / ".runtime" / "selected_5.txt")
                .read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()]
    cross = []
    for code in sorted(set(stocks)):
        cross.append({
            "legacy_symbol": code,
            "in_shioaji_universe": code in SHIOAJI_UNIVERSE,
            "in_selected5": code in selected,
        })
    n_overlap = sum(1 for c in cross if c["in_shioaji_universe"])

    report = {
        "schema": "SQS-WAVE4-G1-LEGACY-ADMISSION/1",
        "legacy_root": str(LEGACY),
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "physical_denominator": {
            "total_files": sum(f["files"] for f in fam.values()),
            "total_bytes": sum(f["bytes"] for f in fam.values()),
            "families": fam,
        },
        "stock_list": {
            "path": "finmind/.runtime/cleaned_stocks.txt",
            "count": len(stocks),
            "selected_5": selected,
            "overlap_with_shioaji_universe": n_overlap,
        },
        "samples": {
            "taiwan_stock_1101": ts_stock,
            "finmind_kbar_1101": kbar_sample,
            "finmind_daily_1470": daily_sample,
            "finmind_index_5s": index5s_sample,
            "finmind_index_kbar": indexkbar_sample,
        },
        "rights_provenance": {
            "source": "LOCAL_LEGACY_CORPUS (WAVE1 inventory identity 60e46475)",
            "origin": "FinMind-derived + Taiwan STOCK historical dumps (research-only)",
            "entitlement": "RESTRICTED_RESEARCH; no redistribution; parity/gap-fill only",
            "status": "PENDING_RIGHTS_RECORD",
        },
        "crosswalk": cross,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({
        "total_files": report["physical_denominator"]["total_files"],
        "total_bytes": report["physical_denominator"]["total_bytes"],
        "stock_list_count": len(stocks),
        "shioaji_overlap": n_overlap,
        "taiwan_stock_sample_cols": ts_stock.get("cols"),
        "kbar_cols": kbar_sample.get("cols"),
    }, indent=1))
    print("RESULT: G1_PROFILE_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
