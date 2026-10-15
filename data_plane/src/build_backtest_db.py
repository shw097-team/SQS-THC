"""G2/G3 — build canonical backtest database from raw shioaji parquet.

Pipeline:
  raw (immutable provider parquet)
    -> core minute parquet (canonical, normalized, PIT fields, dedup)
    -> DuckDB analytical layer (views/table for backtest queries)
    -> SQLite metadata catalog (DatasetVersion + lineage + rights + receipts)

Produces a frozen DatasetVersion manifest (hash of all core files).
"""
from __future__ import annotations

import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import duckdb
import polars as pl

ROOT = Path(r"C:\Projects\Agent_Workspace\SQS-THC")
RAW = ROOT / "data_plane" / "data" / "raw" / "shioaji_kbars"
CORE = ROOT / "data_plane" / "data" / "core" / "minute"
META = ROOT / "data_plane" / "data" / "metadata"
DB = ROOT / "data_plane" / "data" / "backtest.duckdb"
CATALOG = ROOT / "data_plane" / "data" / "metadata" / "catalog.sqlite"


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def main() -> int:
    files = sorted(RAW.rglob("*.parquet"))
    print(f"raw files: {len(files)}")
    # load all raw into one canonical frame with PIT fields
    frames = []
    for f in files:
        df = pl.read_parquet(f)
        frames.append(df)
    if not frames:
        print("RESULT: FAIL (no raw data)")
        return 1
    all_df = pl.concat(frames)
    all_df = all_df.unique(subset=["symbol", "event_time"], keep="first")  # dedup
    all_df = all_df.sort(["symbol", "event_time"])
    # normalize event_time to microsecond (DuckDB native) + PIT fields.
    # raw carries ns epoch (Shioaji); convert via /1000 to us.
    all_df = all_df.with_columns([
        (pl.col("event_time").cast(pl.Int64) / 1000).cast(pl.Datetime("us")).alias("event_time"),
        (pl.col("event_time").cast(pl.Int64) / 1000).cast(pl.Datetime("us")).alias("asof"),
        (pl.col("event_time").cast(pl.Int64) / 1000).cast(pl.Datetime("us")).alias("known_at"),
        pl.lit("TWSE_OR_TPEX").alias("venue"),
    ])
    print(f"core rows: {all_df.height}  symbols: {all_df['symbol'].n_unique()}")
    # write core parquet per symbol (immutable canonical)
    core_files = []
    for sym, sub in all_df.group_by("symbol"):
        s = sub["symbol"][0]
        out = CORE / f"symbol={s}" / "minute.parquet"
        out.parent.mkdir(parents=True, exist_ok=True)
        sub.write_parquet(out, compression="zstd")
        core_files.append(out)
    print(f"core files: {len(core_files)}")
    # duckdb analytical layer
    con = duckdb.connect(str(DB))
    con.execute("DROP TABLE IF EXISTS minute_bars")
    con.execute(f"""
        CREATE TABLE minute_bars AS
        SELECT * FROM read_parquet('{CORE.as_posix()}/**/*.parquet')
    """)
    n = con.execute("SELECT COUNT(*) FROM minute_bars").fetchone()[0]
    con.close()
    print(f"duckdb rows: {n}")
    # DatasetVersion manifest + catalog
    manifest = {
        "dataset_version": "DSV-2026-08-11-r1",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "source_provider": "SHIOAJI",
        "provider_version": "1.7.2",
        "universe": sorted(all_df["symbol"].unique().to_list()),
        "rows": all_df.height,
        "core_files": [{"path": str(f.relative_to(ROOT)), "bytes": f.stat().st_size,
                        "sha256": sha256_file(f)} for f in core_files],
        "lineage_parent": "shioaji-kbars-raw (acquisition receipts journal)",
        "pit_fields": ["asof", "known_at", "event_time", "ts"],
        "rights": "SHIOAJI data-read license; research-only; no redistribution",
    }
    manifest_path = META / "dataset_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=1, ensure_ascii=False), encoding="utf-8")
    conn = sqlite3.connect(CATALOG)
    conn.execute("""CREATE TABLE IF NOT EXISTS dataset_versions(
        version TEXT PRIMARY KEY, manifest_sha256 TEXT, rows INTEGER,
        symbols INTEGER, created_at_utc TEXT)""")
    mh = sha256_file(manifest_path)
    conn.execute("INSERT OR REPLACE INTO dataset_versions VALUES(?,?,?,?,?)",
                 (manifest["dataset_version"], mh, all_df.height,
                  all_df["symbol"].n_unique(), manifest["created_at_utc"]))
    conn.commit()
    conn.close()
    print(f"manifest sha256: {mh}")
    print("RESULT: BACKTEST_DB_BUILT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
