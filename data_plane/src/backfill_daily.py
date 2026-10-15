'''Daily OHLCV backfill for the SQS-THC data plane.

Acquires the daily OHLCV layer for the 263-symbol TWSE/TPEx universe over
2023-01-03 .. 2026-08-13 per user decision UD-DAILY-OHLCV-2026-08-13-001.
TWSE official monthly JSON is the primary provider and the Yahoo Finance
chart API is the read-only fallback for symbols not listed on TWSE. Raw
parquet artifacts are immutable and idempotent, a sha256 receipts journal
backs the skip-if-unchanged policy, and the core layer plus the DuckDB
table are rebuilt deterministically on every run.
'''
import sys

sys.path.insert(0, r'C:\Projects\Agent_Workspace\SQS-THC\.venv-data\Lib\site-packages')

import polars as pl
import duckdb

import calendar
import concurrent.futures
import hashlib
import json
import os
import re
import sqlite3
import threading
import time
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(r'C:\Projects\Agent_Workspace\SQS-THC')
UNIVERSE_FILE = ROOT / 'data_plane' / 'config' / 'daily_universe_263.txt'
RAW_TWSE = ROOT / 'data_plane' / 'data' / 'raw' / 'daily_twse'
CORE = ROOT / 'data_plane' / 'data' / 'core' / 'daily'
RECEIPTS = ROOT / 'data_plane' / 'data' / 'metadata' / 'daily_acquisition_receipts.jsonl'
DUCKDB_PATH = ROOT / 'data_plane' / 'data' / 'backtest.duckdb'
MANIFEST_PATH = ROOT / 'data_plane' / 'data' / 'metadata' / 'daily_dataset_manifest.json'
CATALOG = ROOT / 'data_plane' / 'data' / 'metadata' / 'catalog.sqlite'
LEGACY_DIR = Path(r'C:\Projects\Agent_Workspace\知識庫\SQS-THC資料庫\台股價格歷史資料\Taiwan STOCK')
DEFAULT_START = date(2023, 1, 3)
DEFAULT_END = date(2026, 8, 13)
TWSE_URL = 'https://www.twse.com.tw/exchangeReport/STOCK_DAY'
YAHOO_URL = 'https://query1.finance.yahoo.com/v8/finance/chart/'
WORKERS = 8
REQUEST_TIMEOUT = 20
RETRY = 3
DELAY = 0.2
DATASET_VERSION = 'DSV-DAILY-2026-08-13-r2'

BAR_SCHEMA = {
    'symbol': pl.Utf8,
    'date': pl.Date,
    'open': pl.Float64,
    'high': pl.Float64,
    'low': pl.Float64,
    'close': pl.Float64,
    'volume': pl.Int64,
    'amount': pl.Float64,
    'provider': pl.Utf8,
    'venue': pl.Utf8,
    'source_identity': pl.Utf8,
    'retrieved_at': pl.Datetime(time_unit='us', time_zone='UTC'),
    'asof': pl.Date,
    'known_at': pl.Date,
}

HTTP_SEM = threading.Semaphore(4)
_RECEIPT_LOCK = threading.Lock()


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            digest.update(chunk)
    return digest.hexdigest()


def load_universe():
    codes = []
    with open(UNIVERSE_FILE, 'r', encoding='utf-8') as fh:
        for line in fh:
            token = line.strip()
            if token == '':
                continue
            if not re.fullmatch(r'\d{4}', token):
                raise RuntimeError('invalid universe code: ' + token)
            codes.append(token)
    if len(codes) < 100:
        raise RuntimeError('universe must contain at least 100 codes, got ' + str(len(codes)))
    return codes


def month_windows():
    windows = []
    year = DEFAULT_START.year
    month = DEFAULT_START.month
    while (year, month) <= (DEFAULT_END.year, DEFAULT_END.month):
        windows.append((year, month))
        month += 1
        if month > 12:
            year += 1
            month = 1
    return windows


def last_day_of_month(year, month):
    return calendar.monthrange(year, month)[1]


def epoch_seconds(value):
    return str(int(datetime(value.year, value.month, value.day, tzinfo=timezone.utc).timestamp()))


def http_get_json(url):
    last_error = None
    for attempt in range(RETRY):
        try:
            time.sleep(DELAY)
            request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with HTTP_SEM:
                with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
                    raw = response.read()
            return json.loads(raw.decode('utf-8'))
        except Exception as exc:
            last_error = exc
            time.sleep(DELAY * (attempt + 1))
    raise RuntimeError('http failure after ' + str(RETRY) + ' attempts: ' + str(last_error))


def roc_date_to_iso(value):
    parts = value.split('/')
    year = int(parts[0]) + 1911
    month = int(parts[1])
    day = int(parts[2])
    return date(year, month, day)


def fetch_twse_month(code, year, month):
    first_day = date(year, month, 1)
    query = urllib.parse.urlencode({'response': 'json', 'date': first_day.strftime('%Y%m') + '01', 'stockNo': code})
    url = TWSE_URL + '?' + query
    payload = http_get_json(url)
    stat = payload.get('stat')
    if stat != 'OK':
        return None
    data = payload.get('data')
    if not data:
        return None
    month_key = '{:04d}-{:02d}'.format(year, month)
    now_utc = datetime.now(timezone.utc)
    rows = []
    for item in data:
        if len(item) < 9:
            continue
        try:
            bar_date = roc_date_to_iso(item[0])
        except (ValueError, IndexError):
            continue
        if bar_date < DEFAULT_START or bar_date > DEFAULT_END:
            continue
        try:
            volume = int(item[1].replace(',', ''))
            amount = float(item[2].replace(',', ''))
            open_price = float(item[3].replace(',', ''))
            high = float(item[4].replace(',', ''))
            low = float(item[5].replace(',', ''))
            close = float(item[6].replace(',', ''))
            trades = int(item[8].replace(',', '')) if item[8] else 0
        except (TypeError, ValueError):
            continue
        rows.append({
            'symbol': code,
            'date': bar_date,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume,
            'amount': amount,
            'provider': 'TWSE_OFFICIAL',
            'venue': 'TWSE',
            'source_identity': 'TWSE_STOCK_DAY:' + month_key,
            'retrieved_at': now_utc,
            'asof': bar_date,
            'known_at': bar_date,
        })
    return rows


def fetch_yahoo_suffix(code, suffix, venue):
    url = (YAHOO_URL + code + suffix + '?period1=' + epoch_seconds(DEFAULT_START)
           + '&period2=' + epoch_seconds(DEFAULT_END + timedelta(days=1)) + '&interval=1d')
    payload = http_get_json(url)
    chart = payload.get('chart') or {}
    result = chart.get('result')
    if not result:
        return []
    res = result[0]
    timestamps = res.get('timestamp') or []
    quote = (res.get('indicators') or {}).get('quote')
    if not quote:
        return []
    quote = quote[0]
    opens = quote.get('open') or []
    highs = quote.get('high') or []
    lows = quote.get('low') or []
    closes = quote.get('close') or []
    volumes = quote.get('volume') or []
    now_utc = datetime.now(timezone.utc)
    rows = []
    for idx, ts in enumerate(timestamps):
        if idx >= len(closes):
            break
        close = closes[idx]
        if close is None:
            continue
        bar_date = datetime.fromtimestamp(ts, tz=timezone.utc).date()
        if bar_date < DEFAULT_START or bar_date > DEFAULT_END:
            continue
        open_price = opens[idx] if idx < len(opens) and opens[idx] is not None else close
        high = highs[idx] if idx < len(highs) and highs[idx] is not None else close
        low = lows[idx] if idx < len(lows) and lows[idx] is not None else close
        volume_raw = volumes[idx] if idx < len(volumes) else None
        volume = int(volume_raw) if volume_raw is not None else 0
        amount = round(close * volume, 2)
        rows.append({
            'symbol': code,
            'date': bar_date,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume,
            'amount': amount,
            'provider': 'YAHOO_FINANCE',
            'venue': venue,
            'source_identity': 'YAHOO_CHART:' + suffix + ':full',
            'retrieved_at': now_utc,
            'asof': bar_date,
            'known_at': bar_date,
        })
    return rows


def fetch_yahoo(code):
    for suffix in ('.TWO', '.TW'):
        venue = 'TWO' if suffix == '.TWO' else 'TW'
        rows = fetch_yahoo_suffix(code, suffix, venue)
        if rows:
            return rows, venue
    return [], None


def build_frame(rows):
    if rows:
        return pl.DataFrame(rows)
    return pl.DataFrame(schema=BAR_SCHEMA)


def load_receipts():
    receipts = []
    if not RECEIPTS.exists():
        return receipts
    with open(RECEIPTS, 'r', encoding='utf-8') as fh:
        for line in fh:
            line = line.strip()
            if line == '':
                continue
            try:
                receipts.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return receipts


def append_receipt(record):
    line = json.dumps(record, sort_keys=True) + '\n'
    with _RECEIPT_LOCK:
        with open(RECEIPTS, 'a', encoding='utf-8') as fh:
            fh.write(line)


def latest_receipt(receipts, code, source):
    found = None
    for rec in receipts:
        if rec.get('symbol') == code and rec.get('source') == source:
            found = rec
    return found


def record_skip(target, code, source, start, end):
    frame = pl.read_parquet(target)
    record = {
        'symbol': code,
        'source': source,
        'start': start,
        'end': end,
        'rows': frame.height,
        'bytes': target.stat().st_size,
        'sha256': sha256_file(target),
        'status': 'SKIP_EXISTS',
        'at_utc': datetime.now(timezone.utc).isoformat(),
    }
    append_receipt(record)
    return record


def persist_artifact(target, frame, code, source, start, end, receipts):
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        digest = sha256_file(target)
        latest = latest_receipt(receipts, code, source)
        if latest is not None and latest.get('sha256') == digest:
            return record_skip(target, code, source, start, end)
    tmp = target.with_name(target.name + '.tmp')
    frame.write_parquet(tmp, compression='zstd')
    os.replace(tmp, target)
    record = {
        'symbol': code,
        'source': source,
        'start': start,
        'end': end,
        'rows': frame.height,
        'bytes': target.stat().st_size,
        'sha256': sha256_file(target),
        'status': 'FETCHED',
        'at_utc': datetime.now(timezone.utc).isoformat(),
    }
    append_receipt(record)
    return record


def process_symbol(code, receipts):
    windows = month_windows()
    twse_rows = {}
    failures = []
    for year, month in windows:
        try:
            result = fetch_twse_month(code, year, month)
            twse_rows[(year, month)] = result if result is not None else []
        except Exception as exc:
            failures.append(((year, month), str(exc)))
    if failures:
        remaining = []
        for key, reason in failures:
            try:
                result = fetch_twse_month(code, key[0], key[1])
                twse_rows[key] = result if result is not None else []
            except Exception as exc:
                remaining.append((key, str(exc)))
        if remaining:
            detail = '; '.join('{}-{:02d}:{}'.format(key[0], key[1], reason) for key, reason in remaining)
            return {'code': code, 'status': 'failed', 'reason': 'TWSE_NETWORK_FAILURE ' + detail}
    if any(twse_rows.values()):
        total_rows = 0
        for year, month in windows:
            rows = twse_rows[(year, month)]
            month_key = '{:04d}-{:02d}'.format(year, month)
            source = 'TWSE_STOCK_DAY:' + month_key
            start = month_key + '-01'
            end = month_key + '-' + '{:02d}'.format(last_day_of_month(year, month))
            target = RAW_TWSE / ('symbol=' + code) / ('start=' + month_key + '_end=' + month_key + '.parquet')
            frame = build_frame(rows)
            record = persist_artifact(target, frame, code, source, start, end, receipts)
            total_rows += record['rows']
        return {'code': code, 'status': 'ok', 'venue': 'TWSE', 'rows': total_rows}
    rows, venue = fetch_yahoo(code)
    if not rows:
        return {'code': code, 'status': 'failed', 'reason': 'NO_YAHOO_DATA'}
    suffix = '.TWO' if venue == 'TWO' else '.TW'
    source = 'YAHOO_CHART:' + suffix + ':full'
    start = DEFAULT_START.isoformat()
    end = DEFAULT_END.isoformat()
    target = RAW_TWSE / ('symbol=' + code) / ('yahoo_' + code + '.parquet')
    frame = build_frame(rows)
    record = persist_artifact(target, frame, code, source, start, end, receipts)
    return {'code': code, 'status': 'ok', 'venue': venue, 'rows': record['rows']}


def rebuild_core_symbol(code):
    symbol_dir = RAW_TWSE / ('symbol=' + code)
    if not symbol_dir.exists():
        return None
    parquet_files = sorted(symbol_dir.glob('*.parquet'))
    if not parquet_files:
        return None
    frames = []
    for path in parquet_files:
        frames.append(pl.read_parquet(path))
    combined = pl.concat(frames)
    combined = combined.sort('date')
    combined = combined.unique(subset=['symbol', 'date'], keep='last')
    # Five-clocks correction: known_at is the authorized-available time.
    # For TWSE official EOD, the close of trading day D is conservatively
    # knowable from D+1 00:00 local. Raw artifacts keep the as-received
    # clock (known_at == asof); the canonical core layer applies the
    # conservative EOD availability so the predicate
    # known_at <= decision_time never leaks the same-day close.
    combined = combined.with_columns(pl.col('asof').dt.offset_by('1d').alias('known_at'))
    target = CORE / ('symbol=' + code) / 'daily.parquet'
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_name(target.name + '.tmp')
    combined.write_parquet(tmp, compression='zstd')
    os.replace(tmp, target)
    return combined


def build_duckdb():
    glob_pattern = str(CORE).replace('\\', '/') + '/symbol=*/daily.parquet'
    con = duckdb.connect(str(DUCKDB_PATH))
    try:
        con.execute('CREATE OR REPLACE TABLE daily_bars AS SELECT CAST(symbol AS VARCHAR) AS symbol, date, open, high, low, close, volume, amount, provider, venue, source_identity, retrieved_at, "asof", "known_at" FROM read_parquet(?) ORDER BY symbol, date', [glob_pattern])
    finally:
        con.close()


def receipts_sha256():
    if RECEIPTS.exists():
        return sha256_file(RECEIPTS)
    return ''


def write_manifest(codes, rows_total, coverage_start, coverage_end, failures, raw_artifact_count):
    parent_version = None
    parent_manifest_sha256 = None
    try:
        con = sqlite3.connect(str(CATALOG))
        row = con.execute('SELECT version, manifest_sha256 FROM dataset_versions ORDER BY created_at_utc DESC, version DESC LIMIT 1').fetchone()
        con.close()
        if row:
            parent_version = row[0]
            parent_manifest_sha256 = row[1]
    except sqlite3.OperationalError:
        pass
    manifest = {
        'dataset_version': DATASET_VERSION,
        'created_at_utc': datetime.now(timezone.utc).isoformat(),
        'source_provider': 'TWSE_OFFICIAL_PLUS_YAHOO_FALLBACK',
        'parent_version': parent_version,
        'parent_manifest_sha256': parent_manifest_sha256,
        'universe': codes,
        'rows': rows_total,
        'symbol_count': len(codes),
        'coverage_start': coverage_start,
        'coverage_end': coverage_end,
        'failures': failures,
        'raw_artifact_count': raw_artifact_count,
        'receipts_sha256': receipts_sha256(),
    }
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MANIFEST_PATH, 'w', encoding='utf-8') as fh:
        json.dump(manifest, fh, indent=2, sort_keys=True)
        fh.write('\n')
    return manifest


def register_catalog(manifest):
    con = sqlite3.connect(str(CATALOG))
    try:
        con.execute('CREATE TABLE IF NOT EXISTS dataset_versions (dataset_version TEXT, manifest_sha256 TEXT, rows INTEGER, symbol_count INTEGER, created_at_utc TEXT)')
    except sqlite3.OperationalError:
        pass
    columns = []
    for info in con.execute('PRAGMA table_info(dataset_versions)'):
        columns.append(info[1])
    id_column = 'dataset_version' if 'dataset_version' in columns else ('version' if 'version' in columns else None)
    if id_column is None:
        raise RuntimeError('catalog dataset_versions table has no version column')
    digest = sha256_file(MANIFEST_PATH)
    values = (manifest['dataset_version'], digest, manifest['rows'], manifest['symbol_count'], manifest['created_at_utc'])
    con.execute('DELETE FROM dataset_versions WHERE ' + id_column + ' = ?', (manifest['dataset_version'],))
    if 'dataset_version' in columns and 'symbol_count' in columns:
        con.execute('INSERT INTO dataset_versions (dataset_version, manifest_sha256, rows, symbol_count, created_at_utc) VALUES (?, ?, ?, ?, ?)', values)
    else:
        # legacy catalog schema uses version and symbols column names
        con.execute('INSERT INTO dataset_versions (version, manifest_sha256, rows, symbols, created_at_utc) VALUES (?, ?, ?, ?, ?)', values)
    con.commit()
    con.close()


def last_n_months(today, n):
    months = []
    year = today.year
    month = today.month
    for _ in range(n):
        months.append((year, month))
        month -= 1
        if month < 1:
            year -= 1
            month = 12
    return list(reversed(months))


def next_dsv_version(today):
    prefix = 'DSV-DAILY-' + today.isoformat() + '-r'
    con = sqlite3.connect(str(CATALOG))
    try:
        rows = con.execute('SELECT version FROM dataset_versions WHERE version LIKE ?', (prefix + '%',)).fetchall()
    finally:
        con.close()
    revs = []
    for row in rows:
        tail = row[0][len(prefix):]
        if tail.isdigit():
            revs.append(int(tail))
    return prefix + str((max(revs) + 1) if revs else 1)


def update_incremental(today=None, months_back=1):
    global DATASET_VERSION
    today = today or date.today()
    codes = load_universe()
    receipts = load_receipts()
    windows = last_n_months(today, months_back + 1)
    global DEFAULT_END
    old_end = DEFAULT_END
    if today > DEFAULT_END:
        DEFAULT_END = today
    fetched = 0
    skipped = 0
    failed = []
    new_rows = 0
    try:
        for code in codes:
            for (year, month) in windows:
                month_key = '{:04d}-{:02d}'.format(year, month)
                source = 'TWSE_STOCK_DAY:' + month_key
                start = month_key + '-01'
                end = month_key + '-' + '{:02d}'.format(last_day_of_month(year, month))
                target = RAW_TWSE / ('symbol=' + code) / ('start=' + month_key + '_end=' + month_key + '.parquet')
                latest = latest_receipt(receipts, code, source)
                if latest is not None and target.exists() and latest.get('sha256') == sha256_file(target):
                    skipped += 1
                    continue
                try:
                    rows = fetch_twse_month(code, year, month)
                except Exception as exc:
                    failed.append(code + ':' + month_key + ':' + str(exc)[:80])
                    continue
                frame = build_frame(rows or [])
                record = persist_artifact(target, frame, code, source, start, end, receipts)
                if record.get('status') == 'FETCHED':
                    fetched += 1
                    new_rows += int(record.get('rows') or 0)
                else:
                    skipped += 1
            print('UPDATE_PROGRESS symbol={} skipped={} fetched={} new_rows={}'.format(
                code, skipped, fetched, new_rows), flush=True)
    finally:
        DEFAULT_END = old_end
    if new_rows == 0:
        return {'status': 'NO_CHANGE', 'new_rows': 0, 'fetched_artifacts': fetched,
                'skipped': skipped, 'failures': failed, 'dataset_version': DATASET_VERSION}
    rows_total = 0
    coverage_start = None
    coverage_end = None
    raw_artifact_count = 0
    for code in codes:
        symbol_dir = RAW_TWSE / ('symbol=' + code)
        if symbol_dir.exists():
            raw_artifact_count += len(list(symbol_dir.glob('*.parquet')))
        frame = rebuild_core_symbol(code)
        if frame is None:
            continue
        rows_total += frame.height
        if frame.height:
            code_min = str(frame['date'].min())
            code_max = str(frame['date'].max())
            if coverage_start is None or code_min < coverage_start:
                coverage_start = code_min
            if coverage_end is None or code_max > coverage_end:
                coverage_end = code_max
    build_duckdb()
    old_version = DATASET_VERSION
    new_version = next_dsv_version(today)
    DATASET_VERSION = new_version
    try:
        manifest = write_manifest(codes, rows_total, coverage_start, coverage_end, failed, raw_artifact_count)
        register_catalog(manifest)
    finally:
        DATASET_VERSION = old_version
    return {'status': 'UPDATED', 'dataset_version': new_version, 'parent_version': old_version,
            'new_rows': new_rows, 'rows_total': rows_total, 'fetched_artifacts': fetched,
            'skipped': skipped, 'failures': failed}


def main():
    codes = load_universe()
    receipts = load_receipts()
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as executor:
        future_map = {executor.submit(process_symbol, code, receipts): code for code in codes}
        for future in concurrent.futures.as_completed(future_map):
            code = future_map[future]
            try:
                results[code] = future.result()
            except Exception as exc:
                results[code] = {'code': code, 'status': 'failed', 'reason': 'UNEXPECTED ' + str(exc)}
            result = results[code]
            print('PROGRESS symbol={} status={} rows={} venue={}'.format(
                code, result.get('status', 'failed'), result.get('rows', 0), result.get('venue', 'NA')), flush=True)
    failures = []
    twse_count = 0
    yahoo_count = 0
    for code in codes:
        result = results.get(code)
        if result is None or result.get('status') != 'ok':
            reason = 'missing result' if result is None else result.get('reason', 'unknown')
            failures.append(code + ':' + reason)
        elif result.get('venue') == 'TWSE':
            twse_count += 1
        else:
            yahoo_count += 1
    rows_total = 0
    coverage_start = None
    coverage_end = None
    raw_artifact_count = 0
    for code in codes:
        symbol_dir = RAW_TWSE / ('symbol=' + code)
        if symbol_dir.exists():
            raw_artifact_count += len(list(symbol_dir.glob('*.parquet')))
        frame = rebuild_core_symbol(code)
        if frame is None:
            continue
        rows_total += frame.height
        if frame.height:
            code_min = str(frame['date'].min())
            code_max = str(frame['date'].max())
            if coverage_start is None or code_min < coverage_start:
                coverage_start = code_min
            if coverage_end is None or code_max > coverage_end:
                coverage_end = code_max
    build_duckdb()
    manifest = write_manifest(codes, rows_total, coverage_start, coverage_end, failures, raw_artifact_count)
    register_catalog(manifest)
    symbol_ok = len(codes) - len(failures)
    symbol_failed = len(failures)
    print('DAILY_BACKFILL_SUMMARY symbol_ok={} symbol_failed={} rows_total={} twse_symbols={} yahoo_symbols={} failures={}'.format(
        symbol_ok, symbol_failed, rows_total, twse_count, yahoo_count, failures))
    sys.exit(0 if symbol_failed == 0 else 1)


if __name__ == '__main__':
    main()