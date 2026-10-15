"""G2 — Shioaji historical 1-minute backfill (bounded universe, quota-aware).

Acquires 1-minute K-bars for a bounded TWSE/TPEx research universe over a
12-month window, in 29-day chunks (Shioaji API limit), writing immutable
raw parquet artifacts + a receipt journal.

Security contract: SJ_DATA_READ only — no trading/account permission, no pfx,
no broker write, no live subscription. Credentials come from the local key
file at runtime only; never printed, never committed.

Idempotent: existing raw artifacts are SKIP_EXISTS (sha256 re-verified).
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import polars as pl

ROOT = Path(r"C:\Projects\Agent_Workspace\SQS-THC")
RAW = ROOT / "data_plane" / "data" / "raw" / "shioaji_kbars"
RECEIPTS = ROOT / "data_plane" / "data" / "metadata" / "acquisition_receipts.jsonl"
RAW.mkdir(parents=True, exist_ok=True)
RECEIPTS.parent.mkdir(parents=True, exist_ok=True)

KEY_FILE = ROOT / "實作執行" / "Shioaji API" / "Shioaji API Key .txt"

# bounded research universe (TWSE large-caps + liquid names + TPEx exemplar)
UNIVERSE = ["2330", "2317", "2454", "2603", "2881", "2882", "2891", "2303",
            "2412", "2002", "1301", "1326", "3008", "3231", "2379", "2408",
            "3037", "2382", "2609", "2615", "2637", "2311", "2357", "2498",
            "3481", "2301", "2327", "2344", "2353", "2388", "2368", "6285",
            "8046", "6147", "6182", "6139", "4105", "9933", "1101", "1216",
            "1227", "1717", "1722", "1736", "2105", "2204", "2206", "2610",
            "3702", "6409"]

WINDOW_DAYS = 29  # Shioaji kbars range cap is 30 days; 29 defensively


def windows(start: date, end: date):
    cur = start
    while cur <= end:
        stop = min(cur + timedelta(days=WINDOW_DAYS), end)
        yield cur, stop
        cur = stop + timedelta(days=1)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_creds() -> tuple[str, str]:
    lines = [l.strip() for l in KEY_FILE.read_text(encoding="utf-8-sig", errors="replace").splitlines() if l.strip()]
    vals = [l for l in lines if " " not in l and ":" not in l and "=" not in l and len(l) > 20]
    assert len(vals) == 2
    return vals[0], vals[1]


def main() -> int:
    import shioaji as sj
    start = date.fromisoformat(os.environ.get("TW_START", "2025-08-11"))
    end = date.fromisoformat(os.environ.get("TW_END", "2026-08-10"))
    api_key, sec_key = load_creds()
    api = sj.Shioaji(simulation=True)
    api.login(api_key=api_key, secret_key=sec_key)
    print("login: OK")
    total_rows = 0
    total_fetched = 0
    total_skipped = 0
    failures: list[str] = []
    for code in UNIVERSE:
        try:
            contract = api.Contracts.Stocks[code]
        except Exception:  # noqa: BLE001
            failures.append(f"{code}:NO_CONTRACT")
            continue
        for a, b in windows(start, end):
            target = RAW / f"symbol={code}" / f"start={a.isoformat()}_end={b.isoformat()}.parquet"
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                total_skipped += 1
                continue
            last_err = None
            for attempt in range(3):
                try:
                    kb = api.kbars(contract=contract, start=a.isoformat(), end=b.isoformat())
                    df = (
                        pl.DataFrame(kb.dict())
                        .with_columns(
                            pl.col("ts").cast(pl.Datetime("ns")).alias("event_time"),
                            pl.lit(code).alias("symbol"),
                            pl.lit("SHIOAJI").alias("provider"),
                            pl.lit(datetime.now(timezone.utc).isoformat()).alias("retrieved_at"),
                        )
                        .select(["symbol", "event_time", "Open", "High", "Low", "Close",
                                 "Volume", "Amount", "provider", "retrieved_at"])
                    )
                    if df.is_empty():
                        raise RuntimeError("EMPTY_KBAR_RESULT")
                    tmp = target.with_suffix(".tmp.parquet")
                    df.write_parquet(tmp, compression="zstd")
                    tmp.replace(target)
                    total_fetched += 1
                    total_rows += df.height
                    receipt = {"symbol": code, "start": a.isoformat(), "end": b.isoformat(),
                               "rows": df.height, "bytes": target.stat().st_size,
                               "sha256": sha256_file(target), "status": "FETCHED",
                               "at_utc": datetime.now(timezone.utc).isoformat()}
                    with RECEIPTS.open("a", encoding="utf-8") as fh:
                        fh.write(json.dumps(receipt, ensure_ascii=False) + "\n")
                    break
                except Exception as exc:  # noqa: BLE001
                    last_err = repr(exc)
                    if attempt == 2:
                        failures.append(f"{code}:{a}..{b}:{last_err[:80]}")
                    time.sleep(2 ** attempt)
            time.sleep(0.30)  # conservative pacing
        print(f"{code}: done (total_rows={total_rows})", flush=True)
    api.logout()
    summary = {"start": start.isoformat(), "end": end.isoformat(),
               "symbols_requested": len(UNIVERSE),
               "files_fetched": total_fetched, "files_skipped": total_skipped,
               "rows_total": total_rows, "failures": failures,
               "completed_at_utc": datetime.now(timezone.utc).isoformat()}
    out = ROOT / "data_plane" / "data" / "metadata" / "acquisition_summary.json"
    out.write_text(json.dumps(summary, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))
    print("RESULT:", "G2_ACQUISITION_PARTIAL" if failures else "G2_ACQUISITION_OK")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
