"""G2 — Legacy data disposition + Stock List crosswalk (quarantine-first).

Per G1/G2 admission rules:
  - rights/provenance for the legacy corpus is RESTRICTED_RESEARCH with no
    explicit license file -> NOT admitted into an accepted DatasetVersion.
  - finmind kbar (148,482 files) -> PARITY_ONLY (compare vs Shioaji DSV on
    overlap symbols, never merge); QUARANTINE for any symbol whose parity
    fails.
  - Taiwan STOCK (265 daily files) -> PARITY_ONLY vs Shioaji-derived daily.
  - index_5s/index_kbar -> SOURCE_VALID_NOT_APPLICABLE (index data not in
    current backtest contract).
  - Stock List (263 symbols) -> legacy candidate seed crosswalk vs current
    SQS universe / Shioaji universe; NOT trading-eligibility truth.

Outputs: evidence/review/SQS_WAVE4_LEGACY_DISPOSITION.json
"""
from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import duckdb
import polars as pl

ROOT = Path(r"C:\Projects\Agent_Workspace\SQS-THC")
LEGACY = ROOT / "技術資料庫" / "台股價格歷史資料"
OUT = ROOT / "evidence" / "review" / "SQS_WAVE4_LEGACY_DISPOSITION.json"
DB = ROOT / "data_plane" / "data" / "backtest.duckdb"

SHIOAJI_UNIVERSE = ["2330", "2317", "2454", "2603", "2881", "2882", "2891", "2303",
                    "2412", "2002", "1301", "1326", "3008", "3231", "2379", "2408",
                    "3037", "2382", "2609", "2615", "2637", "2311", "2357", "2498",
                    "3481", "2301", "2327", "2344", "2353", "2388", "2368", "6285",
                    "8046", "6147", "6182", "6139", "4105", "9933", "1101", "1216",
                    "1227", "1717", "1722", "1736", "2105", "2204", "2206", "2610",
                    "3702", "6409"]


def main() -> int:
    stocks = [l.strip() for l in
              (LEGACY / "finmind" / ".runtime" / "cleaned_stocks.txt")
              .read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()]

    # ---- Stock List crosswalk (legacy symbol -> current identity/disposition)
    con = duckdb.connect(str(DB))
    in_db = {str(r[0]) for r in con.execute("SELECT DISTINCT symbol FROM minute_bars").fetchall()}
    con.close()
    crosswalk = []
    for code in sorted(stocks):
        crosswalk.append({
            "legacy_symbol": code,
            "in_shioaji_universe": code in SHIOAJI_UNIVERSE,
            "in_sqs_backtest_db": code in in_db,
            "current_state": "SQS_UNIVERSE" if code in SHIOAJI_UNIVERSE
                             else "LEGACY_ONLY",
            "disposition": "SEED_CANDIDATE" if code in SHIOAJI_UNIVERSE
                           else "LEGACY_SEED_NOT_ADMITTED",
        })

    # ---- finmind kbar coverage profile (per-symbol file counts)
    kbar_root = LEGACY / "finmind" / "raw" / "kbar"
    kbar_syms = {}
    for d in sorted(p for p in kbar_root.iterdir() if p.is_dir()):
        n = len(list(d.glob("*.csv")))
        kbar_syms[d.name] = n
    thin = {k: v for k, v in kbar_syms.items() if v < 100}
    full = {k: v for k, v in kbar_syms.items() if v >= 100}

    report = {
        "schema": "SQS-WAVE4-G2-LEGACY-DISPOSITION/1",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "rights_adjudication": {
            "status": "RESTRICTED_RESEARCH_NO_LICENSE_FILE",
            "decision": "NOT_ADMITTED_TO_ACCEPTED_DSV",
            "rule": "G1: no rights/provenance -> no accepted DatasetVersion write",
            "source": "legacy corpus (FinMind-derived + Taiwan STOCK dumps, research-only)",
        },
        "dispositions": {
            "finmind_kbar_1m": "PARITY_ONLY",
            "finmind_daily": "PARITY_ONLY",
            "taiwan_stock_daily": "PARITY_ONLY",
            "finmind_index_5s": "SOURCE_VALID_NOT_APPLICABLE",
            "finmind_index_kbar": "SOURCE_VALID_NOT_APPLICABLE",
            "finmind_obt_5s": "SOURCE_VALID_NOT_APPLICABLE",
            "finmind_tse_5s": "SOURCE_VALID_NOT_APPLICABLE",
        },
        "kbar_coverage": {
            "symbols_full_history": len(full),
            "symbols_thin_or_partial": len(thin),
            "thin_examples": dict(list(thin.items())[:10]),
        },
        "stock_list_crosswalk": {
            "count": len(stocks),
            "entries": crosswalk,
            "in_shioaji_universe": sum(1 for c in crosswalk if c["in_shioaji_universe"]),
            "in_sqs_backtest_db": sum(1 for c in crosswalk if c["in_sqs_backtest_db"]),
        },
        "successor_dsv": {
            "created": False,
            "parent": "DSV-2026-08-11-r1 (immutable, unchanged)",
            "reason": "no qualified legacy data admitted (rights-constrained)",
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({
        "stock_list": len(stocks),
        "in_shioaji": report["stock_list_crosswalk"]["in_shioaji_universe"],
        "in_sqs_db": report["stock_list_crosswalk"]["in_sqs_backtest_db"],
        "kbar_full_syms": len(full),
        "kbar_thin_syms": len(thin),
        "successor_dsv_created": False,
    }, indent=1))
    print("RESULT: G2_LEGACY_DISPOSITION_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
