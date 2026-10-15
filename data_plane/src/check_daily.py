'''Read-only quality checker for the SQS-THC daily OHLCV layer.

Deterministic verification of the daily bars dataset produced by
backfill_daily.py: universe coverage, date range, OHLC invariants,
duplicate rows, calendar gaps, receipt integrity, layer row counts,
catalog registration, legacy cross-validation and point-in-time fields.
This checker never writes any file.
'''
import sys

sys.path.insert(0, r'C:\Projects\Agent_Workspace\SQS-THC\.venv-data\Lib\site-packages')

import polars as pl
import duckdb

import csv
import hashlib
import json
import random
import sqlite3
from datetime import date, datetime
from pathlib import Path

ROOT = Path(r'C:\Projects\Agent_Workspace\SQS-THC')
RAW_TWSE = ROOT / 'data_plane' / 'data' / 'raw' / 'daily_twse'
CORE = ROOT / 'data_plane' / 'data' / 'core' / 'daily'
RECEIPTS = ROOT / 'data_plane' / 'data' / 'metadata' / 'daily_acquisition_receipts.jsonl'
DUCKDB_PATH = ROOT / 'data_plane' / 'data' / 'backtest.duckdb'
CATALOG = ROOT / 'data_plane' / 'data' / 'metadata' / 'catalog.sqlite'
LEGACY_DIR = Path(r'C:\Projects\Agent_Workspace\知識庫\SQS-THC資料庫\台股價格歷史資料\Taiwan STOCK')
DATASET_VERSION = 'DSV-DAILY-2026-08-13-r2'
EXPECTED_SYMBOLS = 258
CMP_START = date(2023, 1, 3)
CMP_END = date(2025, 6, 26)

checks = []


def add_check(cid, passed, observed):
    checks.append({'id': cid, 'pass': bool(passed), 'observed': str(observed)})


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            digest.update(chunk)
    return digest.hexdigest()


def check_c1(bars):
    core_dirs = []
    if CORE.exists():
        core_dirs = [p for p in CORE.iterdir() if p.is_dir() and p.name.startswith('symbol=')]
    core_count = len(core_dirs)
    bars_symbols = bars.select(pl.col('symbol').n_unique()).item()
    add_check('C1', core_count == EXPECTED_SYMBOLS and bars_symbols == EXPECTED_SYMBOLS,
              'core_dirs={} bars_symbols={}'.format(core_count, bars_symbols))


def check_c2(bars):
    min_date = str(bars.select(pl.col('date').min()).item())
    max_date = str(bars.select(pl.col('date').max()).item())
    add_check('C2', min_date <= '2023-01-04' and max_date >= '2026-08-12',
              'min={} max={}'.format(min_date, max_date))


def check_c3(bars):
    violations = bars.filter(
        (pl.col('high') < pl.max_horizontal(pl.col('open'), pl.col('close')))
        | (pl.col('low') > pl.min_horizontal(pl.col('open'), pl.col('close')))
        | (pl.col('open') <= 0)
        | (pl.col('close') <= 0)
        | (pl.col('volume') < 0)
    )
    add_check('C3', violations.height == 0, 'violations={}'.format(violations.height))


def check_c4(bars):
    groups = bars.group_by(['symbol', 'date']).len().filter(pl.col('len') > 1)
    dup_rows = groups.select((pl.col('len') - 1).sum().fill_null(0)).item()
    add_check('C4', dup_rows == 0, 'duplicate_rows={}'.format(dup_rows))


def check_c5(bars):
    gaps = bars.select(['symbol', 'date']).sort(['symbol', 'date']).with_columns(
        pl.col('date').diff().over('symbol').dt.total_days().alias('gap')
    )
    max_gap = gaps.select(pl.col('gap').max().fill_null(0)).item()
    over14 = gaps.filter(pl.col('gap') > 14).select(pl.col('symbol').n_unique()).item()
    add_check('C5', over14 == 0, 'max_gap_days={} symbols_over_14={}'.format(max_gap, over14))


def check_c6():
    receipt_lines = []
    valid_lines = True
    if RECEIPTS.exists():
        with open(RECEIPTS, 'r', encoding='utf-8') as fh:
            for line in fh:
                line = line.strip()
                if line == '':
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    valid_lines = False
                    continue
                if not all(key in rec for key in ('symbol', 'sha256', 'status')):
                    valid_lines = False
                receipt_lines.append(rec)
    symbol_shas = {}
    for rec in receipt_lines:
        symbol_shas.setdefault(rec.get('symbol'), set()).add(rec.get('sha256'))
    parquet_files = []
    if RAW_TWSE.exists():
        parquet_files = sorted(RAW_TWSE.rglob('*.parquet'))
    rng = random.Random(20260813)
    sample = rng.sample(parquet_files, min(50, len(parquet_files)))
    mismatches = 0
    for path in sample:
        symbol = path.parent.name[len('symbol='):]
        digest = sha256_file(path)
        if digest not in symbol_shas.get(symbol, set()):
            mismatches += 1
    add_check('C6', valid_lines and bool(receipt_lines) and mismatches == 0,
              'lines={} sampled={} mismatches={}'.format(len(receipt_lines), len(sample), mismatches))


def check_c7(bars, con):
    latest_by_key = {}
    if RECEIPTS.exists():
        with open(RECEIPTS, 'r', encoding='utf-8') as fh:
            for line in fh:
                line = line.strip()
                if line == '':
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                latest_by_key[(rec.get('symbol'), rec.get('source'))] = rec
    receipts_rows = 0
    for rec in latest_by_key.values():
        receipts_rows += int(rec.get('rows') or 0)
    glob_pattern = str(CORE).replace('\\', '/') + '/symbol=*/daily.parquet'
    try:
        core_rows = con.execute('SELECT COUNT(*) FROM read_parquet(?)', [glob_pattern]).fetchone()[0]
    except Exception:
        core_rows = None
    bars_rows = bars.height
    add_check('C7', receipts_rows == core_rows and core_rows == bars_rows,
              'receipts={} core={} bars={}'.format(receipts_rows, core_rows, bars_rows))


def check_c8(bars):
    cat = sqlite3.connect('file:' + str(CATALOG).replace('\\', '/') + '?mode=ro', uri=True)
    columns = []
    for info in cat.execute('PRAGMA table_info(dataset_versions)'):
        columns.append(info[1])
    id_column = 'dataset_version' if 'dataset_version' in columns else ('version' if 'version' in columns else None)
    row = None
    if id_column is not None:
        row = cat.execute('SELECT rows FROM dataset_versions WHERE ' + id_column + ' = ?', (DATASET_VERSION,)).fetchone()
    cat.close()
    registered = int(row[0]) if row is not None else None
    add_check('C8', registered is not None and registered == bars.height,
              'registered={} bars={}'.format(registered, bars.height))


def legacy_prices(code):
    path = LEGACY_DIR / (code + '_history.csv')
    if not path.exists():
        return {}
    prices = {}
    with open(path, 'r', encoding='utf-8-sig', newline='') as fh:
        reader = csv.DictReader(fh)
        for rec in reader:
            raw_date = rec.get('date')
            raw_close = rec.get('close')
            if raw_date is None or raw_close is None or raw_close == '':
                continue
            try:
                parsed = date.fromisoformat(raw_date)
            except ValueError:
                continue
            if CMP_START <= parsed <= CMP_END:
                prices[parsed] = float(raw_close)
    return prices


def check_c9(bars):
    twse_syms = sorted(bars.filter(pl.col('provider') == 'TWSE_OFFICIAL').select('symbol').unique().to_series().to_list())
    yahoo_syms = sorted(bars.filter(pl.col('provider') == 'YAHOO_FINANCE').select('symbol').unique().to_series().to_list())
    rng = random.Random(20260813)
    sample = rng.sample(twse_syms, min(20, len(twse_syms))) + rng.sample(yahoo_syms, min(5, len(yahoo_syms)))
    bar_map = {}
    for rec in bars.select(['symbol', 'date', 'close']).to_dicts():
        d = rec['date']
        if isinstance(d, str):
            d = date.fromisoformat(d)
        bar_map.setdefault(rec['symbol'], {})[d] = rec['close']
    total_compared = 0
    total_matched = 0
    per_sample = []
    for code in sample:
        legacy = legacy_prices(code)
        current = bar_map.get(code, {})
        compared = 0
        matched = 0
        for d in sorted(legacy):
            close = current.get(d)
            if close is None:
                continue
            compared += 1
            if abs(close - legacy[d]) <= 0.01:
                matched += 1
        total_compared += compared
        total_matched += matched
        ratio = matched / compared if compared else 0.0
        per_sample.append(code + ':' + '{:.4f}'.format(ratio))
    overall = total_matched / total_compared if total_compared else 0.0
    add_check('C9', total_compared > 0 and overall >= 0.99,
              'samples={} matched={}/{} overall={:.4f} per_sample={}'.format(
                  len(sample), total_matched, total_compared, overall, ';'.join(per_sample)))


def check_c10(bars):
    pit_cols = ['asof', 'known_at', 'retrieved_at', 'provider', 'venue', 'source_identity']
    missing = [col for col in pit_cols if col not in bars.columns]
    nulls = 0
    wrong_clock = 0
    if not missing:
        counts = bars.select([pl.col(col).is_null().sum().alias(col) for col in pit_cols]).to_dicts()[0]
        nulls = 0
        for value in counts.values():
            nulls += value
        wrong_clock = bars.filter(pl.col('known_at') != pl.col('asof').dt.offset_by('1d')).height
    add_check('C10', not missing and nulls == 0 and wrong_clock == 0,
              'missing_cols={} nulls={} wrong_clock={}'.format(missing, nulls, wrong_clock))

def check_c11(bars):
    # Five-clocks causal ordering (FOCUSED-02 closure):
    #   event_time (asof) < publication_time (= availability_time = known_at)
    #   event_time (asof) <= ingest_time (retrieved_at)
    # publication == availability is structural: known_at is the single field
    # serving both, and C10 verifies known_at == asof + 1 day for every row.
    late_publication = bars.filter(pl.col('known_at') <= pl.col('asof')).height
    early_ingest = bars.filter(pl.col('retrieved_at').dt.date() < pl.col('asof')).height
    add_check('C11', late_publication == 0 and early_ingest == 0,
              'publication_not_after_event={} ingest_before_event={}'.format(late_publication, early_ingest))


def main():
    try:
        con = duckdb.connect(str(DUCKDB_PATH), read_only=True)
        bars = con.execute('SELECT * FROM daily_bars').pl()
        check_c1(bars)
        check_c2(bars)
        check_c3(bars)
        check_c4(bars)
        check_c5(bars)
        check_c6()
        check_c7(bars, con)
        check_c8(bars)
        check_c9(bars)
        check_c10(bars)
        check_c11(bars)
        con.close()
    except Exception as exc:
        add_check('FATAL', False, str(exc))
    verdict = 'PASS' if checks and all(c['pass'] for c in checks) else 'FAIL'
    report = {'checker': 'check_daily', 'checks': checks, 'verdict': verdict}
    print(json.dumps(report))
    sys.exit(0 if verdict == 'PASS' else 1)


if __name__ == '__main__':
    main()