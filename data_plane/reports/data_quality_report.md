# WAVE3 G4 — Data Quality Analysis Report (SQS-THC backtest database)

> Deliverable for `data_plane/WORKORDER_CONTRACT_G4_DATA_QUALITY.md` · READ-ONLY analysis · sole artifact: this report

## 1. Scope, identity, and method

| Item | Value |
| --- | --- |
| Dataset version | `DSV-2026-08-11-r1` (manifest sha256 `15454c670182a4f6f6147af0b3a7d11df2d4a917baf73cdf2c5cf128a33289c7`, catalog-bound) |
| Source | Shioaji 1.7.2 historical 1-minute K-bars (TWSE/TPEx), raw parquet → core minute parquet → `backtest.duckdb` → `catalog.sqlite` |
| Window | 2025-08-11 .. 2026-08-10 (12 months) |
| Universe | 49/50 symbols with data (`2311:NO_CONTRACT` recorded failure in acquisition summary) |
| Rows | 2,793,223 (raw = core = duckdb = manifest; identical event sets at µs precision) |
| Raw artifacts | 637 window parquet files; 49 core files |
| Analysis stack | `.venv-data/Scripts/python.exe` — polars 1.43.2, duckdb 1.5.5, sqlite3; no data or source files modified |

Method: SQL/polars aggregation over `minute_bars` (and raw parquet for parity). All checks below are reproducible from the frozen DatasetVersion.

## 2. Verdict (summary)

**PASS (conditional)** — the dataset is structurally sound and usable for the project backtest contract: zero duplicates, zero OHLC-invariant violations, zero nulls, full raw↔core↔duckdb parity, PIT-clean clocks, and a coherent TWSE calendar. **Five conditions** must be respected by the backtest consumer (details in §7):

1. **Unadjusted corporate actions** — raw prices are not adjustment-factor-adjusted; the series contains 2 discontinuities >10.5% (2327 −73.99% on 2025-08-25 after a 7-session halt; 2105 −12.96% on 2026-06-17 ex-div) and ~460 moderate 5–10.5% overnight gaps (mostly ex-dividend days).
2. **No-trade minutes are absent** — the provider emits bars only for traded minutes; 59% of symbol-days have 1–N missing minutes (liquidity-driven), so minute series are not dense for illiquid names.
3. **Disposition (處置) 5-minute auction periods** — e.g., 1717, 2408, 3008, 4105, 6409 show ~54-bar days with every-5th-minute auction prints (OHLC all equal); must not be treated as data loss.
4. **Volume unit = board lots (張; 1 lot = 1,000 shares)** — Amount is TWD; implied price `Amount/(Volume×1000)` matches Close within 3.6% max / 0.07% mean.
5. **Session ceiling is 266 bars/day, not 300** — TWSE regular session is 270 minutes (09:00–13:30); the provider delivers 266 labels (09:01–13:25 + 13:30 closing-auction bar; labels 13:26–13:29 structurally absent). The work-order's '300-minute session' figure does not match the actual TWSE session and is not achievable from this feed.

## 3. Coverage — rows, trading days, calendar

- **Trading days:** 242 distinct dates with data (Mon–Fri only), first **2025-08-11**, last **2026-08-10**.
- **Calendar reconciliation:** 261 weekdays in window; **19 weekdays have zero data across all 49 symbols** → observed market-closure calendar (§3.2). Expected trading days = 242; per-symbol coverage is measured against 242.
- **Per-symbol:** rows 30,594–64,369; days 235–242; 47 symbols cover all 242 days.

### 3.1 Per-symbol summary

| sym | rows | days | full-266d | %full | min bars/d | max bars/d | missing trading days |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1101 | 63,859 | 241 | 137 | 56.8% | 257 | 266 | 2025-08-13 |
| 1216 | 62,902 | 242 | 89 | 36.8% | 192 | 266 | — |
| 1227 | 30,594 | 242 | 0 | 0.0% | 55 | 239 | — |
| 1301 | 63,943 | 242 | 142 | 58.7% | 239 | 266 | — |
| 1326 | 63,364 | 242 | 115 | 47.5% | 223 | 266 | — |
| 1717 | 61,026 | 242 | 105 | 43.4% | 54 | 266 | — |
| 1722 | 45,833 | 242 | 3 | 1.2% | 96 | 266 | — |
| 1736 | 30,756 | 242 | 0 | 0.0% | 50 | 254 | — |
| 2002 | 64,278 | 242 | 189 | 78.1% | 259 | 266 | — |
| 2105 | 61,514 | 242 | 71 | 29.3% | 174 | 266 | — |
| 2204 | 39,993 | 242 | 0 | 0.0% | 88 | 265 | — |
| 2206 | 35,118 | 242 | 0 | 0.0% | 57 | 255 | — |
| 2301 | 64,135 | 242 | 178 | 73.6% | 243 | 266 | — |
| 2303 | 62,224 | 242 | 213 | 88.0% | 53 | 266 | — |
| 2317 | 64,369 | 242 | 240 | 99.2% | 264 | 266 | — |
| 2327 | 60,072 | 235 | 173 | 73.6% | 53 | 266 | 2025-08-14, 2025-08-15, 2025-08-18, 2025-08-19, 2025-08-20, 2025-08-21, 2025-08-22 |
| 2330 | 64,362 | 242 | 234 | 96.7% | 263 | 266 | — |
| 2344 | 57,361 | 242 | 178 | 73.6% | 15 | 266 | — |
| 2353 | 64,077 | 242 | 138 | 57.0% | 253 | 266 | — |
| 2357 | 59,889 | 242 | 31 | 12.8% | 182 | 266 | — |
| 2368 | 63,065 | 242 | 89 | 36.8% | 109 | 266 | — |
| 2379 | 57,283 | 242 | 21 | 8.7% | 97 | 266 | — |
| 2382 | 64,311 | 242 | 209 | 86.4% | 262 | 266 | — |
| 2388 | 56,224 | 242 | 12 | 5.0% | 154 | 266 | — |
| 2408 | 57,560 | 242 | 179 | 74.0% | 15 | 266 | — |
| 2412 | 63,148 | 242 | 90 | 37.2% | 223 | 266 | — |
| 2454 | 60,502 | 242 | 83 | 34.3% | 54 | 266 | — |
| 2498 | 61,221 | 242 | 43 | 17.8% | 210 | 266 | — |
| 2603 | 63,355 | 242 | 95 | 39.3% | 239 | 266 | — |
| 2609 | 64,109 | 242 | 151 | 62.4% | 249 | 266 | — |
| 2610 | 63,941 | 242 | 158 | 65.3% | 232 | 266 | — |
| 2615 | 62,639 | 242 | 52 | 21.5% | 217 | 266 | — |
| 2637 | 54,651 | 242 | 12 | 5.0% | 107 | 266 | — |
| 2881 | 64,092 | 242 | 158 | 65.3% | 241 | 266 | — |
| 2882 | 63,822 | 242 | 129 | 53.3% | 248 | 266 | — |
| 2891 | 64,269 | 242 | 201 | 83.1% | 256 | 266 | — |
| 3008 | 37,463 | 242 | 0 | 0.0% | 45 | 265 | — |
| 3037 | 56,838 | 242 | 175 | 72.3% | 14 | 266 | — |
| 3231 | 64,357 | 242 | 227 | 93.8% | 265 | 266 | — |
| 3481 | 60,035 | 242 | 172 | 71.1% | 53 | 266 | — |
| 3702 | 61,974 | 242 | 87 | 36.0% | 172 | 266 | — |
| 4105 | 32,556 | 242 | 1 | 0.4% | 49 | 266 | — |
| 6139 | 59,585 | 242 | 16 | 6.6% | 177 | 266 | — |
| 6147 | 55,076 | 242 | 46 | 19.0% | 54 | 266 | — |
| 6182 | 53,151 | 242 | 36 | 14.9% | 14 | 266 | — |
| 6285 | 60,612 | 242 | 71 | 29.3% | 165 | 266 | — |
| 6409 | 35,260 | 242 | 0 | 0.0% | 59 | 261 | — |
| 8046 | 56,313 | 242 | 91 | 37.6% | 15 | 266 | — |
| 9933 | 56,142 | 242 | 14 | 5.8% | 154 | 266 | — |

Notes: `full-266d` = sessions achieving the 266-label ceiling. Liquid large-caps (2317 99.2%, 2330 96.7%, 3231 93.8%) are effectively complete; sparse/illiquid names (1736, 2204, 2206, 1227, 6409, 3008) never reach 266 (no-trade minutes). 3008 (大立光) trades only a few lots/minute — sparse by nature, not a defect.

### 3.2 Observed market-closure calendar (19 weekdays, zero data for all symbols)

| Date | Weekday | Classification / note |
| --- | --- | --- |
| 2025-09-29 | Monday | Observed all-market closure (not a statutory holiday) — likely typhoon day; verify vs TWSE closure archive |
| 2025-10-06 | Monday | Mid-Autumn Festival (observed holiday) |
| 2025-10-10 | Friday | National Day (Double Ten) |
| 2025-10-24 | Friday | Observed all-market closure — likely typhoon day; verify vs TWSE closure archive |
| 2025-12-25 | Thursday | Constitution Day (TWSE closed) |
| 2026-01-01 | Thursday | New Year's Day |
| 2026-02-12 | Thursday | Observed closure in CNY period — verify vs official 2026 holiday schedule |
| 2026-02-13 | Friday | Observed closure in CNY period — verify vs official 2026 holiday schedule |
| 2026-02-16 | Monday | Lunar New Year's Eve |
| 2026-02-17 | Tuesday | Lunar New Year Day 1 |
| 2026-02-18 | Wednesday | Lunar New Year Day 2 |
| 2026-02-19 | Thursday | Lunar New Year Day 3 |
| 2026-02-20 | Friday | Lunar New Year Day 4 |
| 2026-02-27 | Friday | Peace Memorial Day observed (2/28 Sat) |
| 2026-04-03 | Friday | Children's Day observed (4/4 Sat) |
| 2026-04-06 | Monday | Tomb Sweeping Day observed (4/5 Sun) |
| 2026-05-01 | Friday | Labor Day |
| 2026-06-19 | Friday | Dragon Boat Festival |
| 2026-07-10 | Friday | Observed all-market closure — likely typhoon day; verify vs TWSE closure archive |

> Reconciliation caveat: 2025-09-29, 2025-10-24, 2026-02-12, 2026-02-13, 2026-07-10 are observed closures that are not statutory holidays in the standard 2025/2026 ROC calendar (likely typhoon days or CNY-schedule adjustments). They are **empirically closed in this dataset** (0 bars for all 49 symbols) and should be cross-checked against the official TWSE closure archive before downstream use.

### 3.3 Symbol-level gaps (beyond all-market closures)

- **1101**: 1 missing day — **2025-08-13** (data exists 08-11/08-12 and 08-14+; single-day hole).
- **2327**: 7 consecutive missing days — **2025-08-14 .. 2025-08-22** — coincides with the corporate-action suspension that produced the −73.99% re-open on 2025-08-25 (§7.3).
- All other 47 symbols: no missing trading days.

## 4. Intraday session structure

- **Observed label range:** 09:01 → 13:30 (bar-end labeling; the 09:01 bar carries the opening auction print, the 13:30 bar carries the 13:25–13:30 closing-auction print). Zero rows outside 09:00–13:30.
- **Distinct minute labels:** 266 = 09:01..13:25 (265) + 13:30 (1). The theoretical continuous minute set is 270 (09:00–13:30); labels **13:26–13:29 are structurally absent** because TWSE runs a closing call auction 13:25–13:30 with a single print at 13:30. This is expected market microstructure, not data loss.
- **Session completeness:** 4854 / 11850 symbol-days (41.0%) achieve all 266 labels; 8.1% miss exactly 1, 4.2% miss 2, …; missing minutes are almost always isolated 1–4-minute blocks → minutes with no trades (provider emits no empty bars; `Volume=0` count = 0).
- **Delayed first bars:** 90 symbol-days start after 09:01 (worst: 4105×19 up to 09:15, 2206×18 up to 09:25) — delayed-open/illiquid/disposition sessions.
- **Missing closing bar:** 1 symbol-day — 6409 on 2026-06-08 ends at 13:25 (no 13:30 print).

| Stat | Value |
| --- | --- |
| Session labels | 09:01..13:25 + 13:30 = 266 |
| Continuous minutes in TWSE regular session | 270 (09:00–13:30) |
| Labels structurally absent | 13:26, 13:27, 13:28, 13:29 (closing auction) |
| Symbol-days at 266-label ceiling | 4,854 (41.0%) |
| Symbol-days missing ≥1 label | 6,996 (59.0%) |
| Delayed-open symbol-days (>09:01) | 90 |
| Symbol-days without 13:30 bar | 1 (6409, 2026-06-08) |

**Reading vs the contract's 'expected 300-minute session':** a literal 300 bars/session is **not achievable** from this feed. The TWSE regular session is 270 minutes; Shioaji's 1-minute feed yields at most 266 labels. If the backtest contract truly requires 300 bars, the spec figure is incorrect for TWSE and should be corrected to the 270/266 reality. No evidence this is a fetch defect.

## 5. OHLC sanity and price consistency

| Check | Result |
| --- | --- |
| high ≥ low | 0 violations |
| high ≥ max(open, close) | 0 violations |
| low ≤ min(open, close) | 0 violations |
| open/high/low/close > 0 | 0 non-positive |
| volume/amount ≥ 0 | 0 negative |
| nulls in any field | 0 |
| volume↔amount zero-mismatch | 0 |
| implied price Amount/(Volume×1000) vs Close | max dev 3.56% · mean dev 0.0735% · >5% dev rows: 0 |

- Implied-price test confirms **Volume is in board lots** (1 lot = 1,000 shares) and Amount is TWD: `Amount/(Volume×1000)` tracks Close to 0.07% mean, 3.56% max — consistent with per-minute VWAP vs last price. Consumers must scale Volume by 1000 for share-denominated models.
- No zero-volume bars exist anywhere (provider omits empty minutes — consistent with §4).

## 6. Volume / amount distribution tails

- Heavy right tails are present and **plausible**: 68 bars exceed 20× the symbol's p99 volume; the top bars are dominated by **13:30 closing-auction prints** (aggregates 13:25–13:30 volume) and large 3481/2344/2408/3037/8046/6147 intraday prints during the 2026 momentum episode. Example: 2353 2025-11-24 13:30 = 329,832 lots (≈NT$9.07bn), ~245× its p99.
- Max-to-p99 volume ratio per symbol ranges ~10× (2330) to ~245× (2353); no evidence of erroneous decimal/scale shifts — OHLC and implied price are internally consistent for every tail bar sampled.

| sym | v_p50 | v_p95 | v_p99 | v_max | a_p50 | a_p99 | a_max |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1101 | 40 | 456 | 1,216 | 145,020 | 956,301 | 29,414,838 | 3,386,217,000 |
| 1216 | 18 | 152 | 462 | 19,200 | 1,320,531 | 35,285,469 | 1,378,560,000 |
| 1227 | 3 | 29 | 78 | 3,659 | 85,974 | 2,330,798 | 112,514,250 |
| 1301 | 47 | 485 | 1,408 | 123,889 | 2,124,635 | 71,192,665 | 6,405,061,300 |
| 1326 | 46 | 503 | 1,440 | 15,749 | 1,880,541 | 75,602,138 | 1,221,677,400 |
| 1717 | 34 | 493 | 1,508 | 14,327 | 1,936,122 | 101,132,549 | 1,271,441,100 |
| 1722 | 5 | 54 | 160 | 7,568 | 232,941 | 7,576,771 | 388,523,900 |
| 1736 | 2 | 21 | 50 | 631 | 322,568 | 7,262,400 | 92,793,500 |
| 2002 | 57 | 634 | 2,144 | 323,897 | 1,085,436 | 41,663,407 | 6,186,432,700 |
| 2105 | 16 | 154 | 418 | 127,909 | 522,791 | 13,443,490 | 4,003,551,700 |
| 2204 | 3 | 28 | 71 | 2,711 | 171,778 | 4,020,852 | 148,833,900 |
| 2206 | 3 | 25 | 64 | 999 | 173,509 | 3,894,448 | 61,038,900 |
| 2301 | 37 | 392 | 1,125 | 25,864 | 6,465,343 | 212,400,109 | 6,065,108,000 |
| 2303 | 163 | 2,091 | 6,265 | 109,231 | 10,094,796 | 633,758,290 | 15,783,879,500 |
| 2317 | 98 | 909 | 2,744 | 25,905 | 22,516,333 | 644,788,300 | 7,486,370,500 |
| 2327 | 57 | 663 | 1,748 | 13,414 | 16,913,196 | 818,907,260 | 12,113,206,000 |
| 2330 | 38 | 366 | 1,545 | 50,967 | 67,386,960 | 2,561,787,174 | 120,027,285,000 |
| 2344 | 344 | 3,436 | 8,020 | 82,843 | 29,616,570 | 796,661,743 | 9,489,679,500 |
| 2353 | 40 | 408 | 1,347 | 329,832 | 1,143,619 | 42,519,255 | 9,070,380,000 |
| 2357 | 7 | 57 | 170 | 3,475 | 4,399,338 | 111,184,787 | 2,266,524,000 |
| 2368 | 15 | 117 | 298 | 24,860 | 10,896,085 | 227,108,963 | 13,424,400,000 |
| 2379 | 5 | 47 | 146 | 12,187 | 3,009,079 | 91,562,590 | 5,843,666,500 |
| 2382 | 35 | 291 | 865 | 10,662 | 10,556,667 | 269,616,204 | 3,614,418,000 |
| 2388 | 10 | 124 | 392 | 4,933 | 580,398 | 27,416,219 | 412,743,700 |
| 2408 | 184 | 1,881 | 4,427 | 30,254 | 40,160,818 | 1,007,939,063 | 9,479,485,000 |
| 2412 | 12 | 123 | 609 | 31,990 | 1,602,164 | 81,609,066 | 4,270,665,000 |
| 2454 | 12 | 134 | 392 | 8,798 | 21,607,577 | 926,213,487 | 37,919,380,000 |
| 2498 | 17 | 291 | 1,070 | 14,004 | 799,097 | 67,040,949 | 845,506,700 |
| 2603 | 16 | 184 | 605 | 12,130 | 3,090,708 | 122,465,855 | 2,595,820,000 |
| 2609 | 29 | 308 | 1,043 | 36,216 | 1,571,450 | 58,500,912 | 1,894,096,800 |
| 2610 | 44 | 491 | 1,459 | 245,856 | 885,916 | 29,684,898 | 4,695,849,600 |
| 2615 | 15 | 167 | 551 | 32,648 | 1,208,056 | 45,344,386 | 2,579,192,000 |
| 2637 | 7 | 68 | 218 | 4,824 | 480,391 | 15,134,183 | 339,127,200 |
| 2881 | 35 | 317 | 859 | 88,007 | 3,388,030 | 95,251,976 | 9,680,770,000 |
| 2882 | 40 | 324 | 868 | 32,630 | 3,049,141 | 71,014,378 | 2,796,391,000 |
| 2891 | 66 | 447 | 1,208 | 113,463 | 3,377,939 | 67,451,057 | 4,952,659,950 |
| 3008 | 3 | 27 | 76 | 996 | 8,490,637 | 262,982,545 | 4,242,590,000 |
| 3037 | 47 | 528 | 1,367 | 31,465 | 18,097,793 | 625,261,533 | 19,697,090,000 |
| 3231 | 63 | 774 | 2,241 | 36,888 | 8,867,004 | 334,458,395 | 6,418,512,000 |
| 3481 | 341 | 5,793 | 14,897 | 172,443 | 8,372,578 | 578,321,289 | 8,946,692,600 |
| 3702 | 17 | 149 | 406 | 127,836 | 1,429,866 | 38,685,702 | 8,104,802,400 |
| 4105 | 3 | 21 | 49 | 565 | 199,057 | 3,850,999 | 48,194,500 |
| 6139 | 8 | 81 | 226 | 2,669 | 4,792,691 | 129,736,663 | 969,391,000 |
| 6147 | 12 | 372 | 1,154 | 10,311 | 930,089 | 218,554,855 | 2,712,569,000 |
| 6182 | 22 | 571 | 1,825 | 18,200 | 810,528 | 190,584,916 | 2,696,645,000 |
| 6285 | 15 | 252 | 772 | 7,978 | 2,594,242 | 164,957,287 | 2,280,474,500 |
| 6409 | 2 | 21 | 61 | 9,169 | 2,288,021 | 59,145,394 | 9,013,127,000 |
| 8046 | 27 | 305 | 811 | 7,280 | 12,110,766 | 456,327,281 | 5,605,836,000 |
| 9933 | 8 | 79 | 209 | 4,402 | 266,118 | 7,439,146 | 127,695,900 |

Top-12 volume bars (all verified OHLC-consistent):

| sym | timestamp | Volume (lots) | Amount (NT$) |
| --- | --- | ---: | ---: |
| 2353 | 2025-11-24 13:30 | 329,832 | 9,070,380,000 |
| 2002 | 2026-06-18 13:30 | 323,897 | 6,186,432,700 |
| 2610 | 2026-05-29 13:30 | 245,856 | 4,695,849,600 |
| 3481 | 2026-05-26 09:03 | 172,443 | 8,946,692,600 |
| 1101 | 2025-09-19 13:30 | 145,020 | 3,386,217,000 |
| 2105 | 2026-02-26 13:30 | 127,909 | 4,003,551,700 |
| 3702 | 2025-11-24 13:30 | 127,836 | 8,104,802,400 |
| 1301 | 2026-06-18 13:30 | 123,889 | 6,405,061,300 |
| 3481 | 2026-02-25 09:18 | 116,718 | 3,186,185,150 |
| 2891 | 2025-09-19 13:30 | 113,463 | 4,952,659,950 |
| 2303 | 2026-05-29 13:30 | 109,231 | 15,783,879,500 |
| 3481 | 2026-05-12 10:00 | 105,685 | 3,745,928,250 |

## 7. Duplicates, gaps, and anomalies

### 7.1 Duplicates — none
- Core `(symbol, event_time)` duplicate groups: **0**.
- Raw parquet: **0** duplicate `(symbol,event_time)` rows and **0** exact-row duplicates across all 637 files (window boundaries are adjacent, never overlapping, and re-fetch produced no repeats).
- Parity: raw total 2,793,223 = raw-unique 2,793,223 = core 2,793,223 = duckdb 2,793,223 = manifest 2,793,223; raw↔core `(symbol,event_time)` sets identical at µs precision (ns→µs conversion lossless; 0 sub-µs timestamps).

### 7.2 Gaps
- 19 all-market closure weekdays (§3.2) — calendar, not data gaps.
- 8 symbol-day gaps: 1101 (1) + 2327 (7) — see §3.3.
- Intraday: missing minutes = no-trade minutes (59% of symbol-days, §4); 1 missing closing print (6409 2026-06-08).

### 7.3 Price anomalies / discontinuities
- **Overnight gaps >10.5%: 2** — both corporate-action events:
  - **2105** 2026-06-17: open 29.55 vs prev close 33.95 → **-12.96%**
  - **2327** 2025-08-25: open 142.0 vs prev close 546.0 → **-73.99%**
- Overnight gaps 5–10.5%: **460** (typical ex-dividend/limit-move days, June–July 2026 ex-div season concentrated).
- **Within-day bar-to-bar moves >10.5% (excluding first bar of day): 0** — the price series contains no intraday jumps beyond the daily limit; all large moves are legitimate opening (09:01) prints.
- **PIT/clocks:** `known_at == asof == event_time` for all 2,793,223 rows (0 mismatches); single provider (SHIOAJI), single venue label (`TWSE_OR_TPEX`), 637 per-file `retrieved_at` stamps from the single 2026-08-11 backfill run (02:44–02:48 UTC).

## 8. Minor issues (non-blocking)

1. **DuckDB symbol type coercion** — `minute_bars.symbol` was inferred as `BIGINT` by the glob read (`read_parquet('.../**/*.parquet')`) while core parquet stores `String`. All 49 symbols are numeric so the coercion is lossless, but SQL consumers must `CAST(symbol AS VARCHAR)` when joining to string-keyed reference data.
2. **Manifest `pit_fields` lists `ts`** but core files contain no `ts` column (`asof`, `known_at`, `event_time` only) — manifest/schema documentation mismatch, no data impact.
3. **Venue is a generic placeholder** `TWSE_OR_TPEX` on every row; symbol-level TWSE/TPEx attribution is not recorded.
4. **Corporate actions are unadjusted** — the dataset ships raw provider prices; no adjustment-factor table is present. Mandatory for backtests: exclude/adjust 2327 (2025-08-25) and handle ex-dividend days (see §2.1).

## 9. Verdict — usable for the project backtest contract?

**PASS (conditional).** Evidence basis:

| Contract requirement | Result | Evidence |
| --- | --- | --- |
| Row/day coverage vs TWSE calendar | PASS | 242/242 expected trading days per symbol for 47/49 symbols; 1101 −1, 2327 −7 (documented) |
| Intraday session completeness | PASS (with caveat) | 266-label ceiling = full 270-min TWSE session minus 4 closing-auction labels; 300-bar spec figure is incorrect for TWSE |
| OHLC sanity | PASS | 0 violations of all invariants; 0 nulls/non-positive/negative |
| Volume/amount consistency & tails | PASS | implied-price max dev 3.56%; tails heavy but internally consistent |
| Duplicates | PASS | 0 duplicate rows in raw and core |
| Gaps | PASS (with caveat) | closures=calendar; symbol gaps documented; intraday gaps = no-trade minutes |
| Price anomalies | PASS (with caveat) | 2 corporate-action discontinuities, 0 intraday anomalies — must be handled by consumer |
| PIT / determinism / lineage | PASS | PIT clean; frozen manifest sha256 catalog-bound; raw=core=duckdb parity |

**Conditions for safe use** (backtest layer must): (1) treat missing minutes as no-trade (do not forward-fill blindly into illiquid names); (2) apply corporate-action handling (at minimum exclude 2327 2025-08-25 and ex-div reference-price gaps); (3) detect 5-min-auction disposition periods and model them as auction prints; (4) scale Volume by 1,000 for share units; (5) correct the 300-minute session expectation to the 266-label/270-minute TWSE reality.

---

*Generated: read-only analysis of `DSV-2026-08-11-r1` (manifest sha256 `15454c670182a4f6f6147af0b3a7d11df2d4a917baf73cdf2c5cf128a33289c7`; catalog version `DSV-2026-08-11-r1`, rows 2,793,223). No data files or source code were modified.*
