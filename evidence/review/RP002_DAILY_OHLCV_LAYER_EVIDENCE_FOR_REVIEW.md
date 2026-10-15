# RP-002 v2.0｜Daily OHLCV Layer 建置證據（WO-RP2-DAILY-001）

```yaml
artifact_id: RP002_DAILY_OHLCV_LAYER_EVIDENCE_FOR_REVIEW
project_id: HGK-REFERENCE-PROJECT-002
workorder: WO-RP2-DAILY-001
writer: codex
checker: swarm-lane-b-acceptance-officer
workorder_state: VERIFIED
generated_at: 2026-08-13
dataset_version: DSV-DAILY-2026-08-13-r1
```

## 1. 任務與決策

用戶決策 **UD-DAILY-OHLCV-2026-08-13-001**：Daily OHLCV 由「5 年全 eligible」改為「**3~4 年（2023-01-03→2026-08-13）、全 eligible TWSE/TPEx、263 檔目標**」。
用戶決策 **UD-UNIVERSE-REMOVAL-2026-08-13-001**：停牌個股直接自清單刪除並留存證據（執行 5 檔除名，263→258）。

## 2. 最終資料層（DSV-DAILY-2026-08-13-r1）

| 項目 | 值 |
|---|---|
| Universe | **258 symbols**（v1 263 減除 1225/1236/9918/9931/5906） |
| 範圍 | **2023-01-03 → 2026-08-13**（3.6 年，全含今日） |
| Rows | **221,349** |
| Raw artifacts | 11,352 parquet（symbol=XXX/start=YYYY-MM_end=YYYY-MM，zstd，逐窗 sha256 receipts） |
| Core | `data_plane/data/core/daily/symbol=*/daily.parquet`（258 檔，symbol VARCHAR） |
| Analytical | `backtest.duckdb` → `daily_bars`（221,349 rows，symbol VARCHAR） |
| Metadata | `catalog.sqlite` dataset_versions：DSV-DAILY-2026-08-13-r1，rows=221,349 |
| Receipts | `daily_acquisition_receipts.jsonl` 13,332 行；latest-per-(symbol,source) 加總 = 221,349 |
| Provider | **TWSE_OFFICIAL**（STOCK_DAY，實測涵蓋上市櫃代碼）；Yahoo `.TWO` 為明示 fallback（0 次使用） |
| PIT | asof/known_at/retrieved_at/venue/source_identity 逐列齊全（C10） |
| 除名歸檔 | `raw/daily_twse_removed_archive/`（1225/1236/9918/9931/5906，含 ARCHIVE_MANIFEST.json） |

## 3. 執行面（六面全啟用）

| 面 | 證據 |
|---|---|
| HGK | REQ-DAILY-001 **FROZEN**（EVT-2d94adb9, v1）→ TS-DAILY-001 → **WO-RP2-DAILY-001（writer=codex）VERIFIED**；EV-DAILY-001..007 註冊 |
| KANBAN | board `rp002-daily-ohlcv`：D0–D4 done、D5 done、D6 done（claim/heartbeat/complete 全履約） |
| SWARM | deleg_2efaafa4 雙 lane 平行：Lane-A 8/8 PASS、Lane-B 8/8 PASS（overlap 124s 內並行） |
| GSTACK/OPENSPEC | `S2R_ROUTER_EVIDENCE_DAILY.json`：brownfield→OPENSPEC CERTIFIED_ACTIVE_BROWNFIELD；review/qa→GSTACK |
| CODEX | 5 次 tracked writes（EXIT=0）：backfill_daily.py、check_daily.py、universe 檔、check patch×2、universe patch；provider receipt opencode-go/deepseek-v4-flash/status=200 |

## 4. 驗證結果

- **check_daily 10/10 PASS**（CHECK_DAILY_VERDICT.json `31def72b…`）：C1 258 覆蓋、C2 範圍、C3 OHLC 0 違規、C4 0 重複、C5 max_gap 14d、C6 receipts 完整性、C7 receipts=core=bars=221,349、C8 DSV 註冊、C9 legacy 交叉 100%（11,630/11,630）、C10 PIT
- **SWARM Lane-A 8/8 PASS**：含 fresh-seed legacy 交叉 5,729/5,729=100%、sha256 抽驗 20/20
- **SWARM Lane-B 8/8 PASS**：證據鏈/lineage/router/Kanban/產品碼/canonical suite 231 OK/Codex receipt/無生產宣稱
- **SQS canonical suite**：231 tests OK（0.501s）

## 5. 缺陷與修補（誠實記錄）

`DEFECT_AND_REPAIR_RECORD.md`（`454abb3d…`）：308-transient、silent-empty-month、empty-frame-persist、duckdb BIGINT 推斷、SKIP O(n²)、universe 硬編碼、TPEx 官方不可達（→TWSE 唯一來源）。修補工具全置 `HG-KSEOS/var/pciv/`（gitignored）；產品碼僅 Codex tracked writes。

## 6. 證據索引（SHA-256）

| EV ID | 工件 | SHA-256 |
|---|---|---|
| EV-DAILY-001 | USER_DECISION_DAILY_OHLCV_2026-08-13.md | 878a706f0f3999bf914ac3511425c130936626265ac3de4ea24580fb5e592f07 |
| EV-DAILY-002 | UNIVERSE_REMOVALS_2026-08-13.md | 807cee9c0f8785fa… |
| EV-DAILY-003 | DEFECT_AND_REPAIR_RECORD.md | 454abb3d81e0f5d1… |
| EV-DAILY-004 | CHECK_DAILY_VERDICT.json | 31def72b7a20bb10… |
| EV-DAILY-005 | daily_dataset_manifest.json | 9b3421dc704f73cc… |
| EV-DAILY-006 | S2R_ROUTER_EVIDENCE_DAILY.json | 7222d1e8452ba63d… |
| EV-DAILY-007 | daily_universe_263.txt v3 | 25f10e9c7dc4c7ad… |

（完整 64-hex 見 Shared Spine evidence_refs；本 MD 不嵌入自身 hash——single-direction binding。）

## 7. Claim 邊界

```text
DAILY_OHLCV_LAYER = COMPLETE（258 symbols × 2023-01-03 → 2026-08-13，DSV-DAILY-2026-08-13-r1）
production autonomy = NOT_CLAIMED | SQS live trading = NOT_AUTHORIZED | remote deployment = NOT_CLAIMED
runtime qualification（broker/execution）= NOT_RUN（STATUS_VECTOR TT-TS014-001 BLOCKING 維持）
```

## 8. 終止

```text
WO-RP2-DAILY-001 VERIFIED（checker=swarm-lane-b ≠ writer=codex）
DAILY_OHLCV_LAYER_COMPLETE
STOP
```
