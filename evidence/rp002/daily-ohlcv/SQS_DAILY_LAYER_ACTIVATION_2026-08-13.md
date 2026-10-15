# SQS 台股 Daily OHLCV 資料庫｜啟用與每日自動更新證據｜WO-RP2-DAILY-004

```yaml
artifact_id: SQS_DAILY_LAYER_ACTIVATION_2026-08-13
workorder: WO-RP2-DAILY-004
basis: WO-RP2-DAILY-001_002_003_EXTERNAL_FINAL_ACCEPTANCE_REPORT_2026-08-13_r4.md（EXTERNAL FINAL ACCEPTANCE = GRANTED）
subject_dataset: DSV-DAILY-2026-08-13-r2
generated_at: 2026-08-13
```

## 1. 外部最終驗收（binding）

r4 報告裁決 **PASS / GRANTED**，接受 claim `DAILY_OHLCV_LOCAL_BACKTEST_DATA_LAYER_PASS`（7/7 promotion conditions、0 blocking findings、0 blocking TT）。彙整證據 r4（sha `33c12726…`）與 AO receipt r4（sha `118c2cd6…`）已三根 byte-identical。

## 2. 啟用狀態（SQS ACTIVE）

| 工件 | 值 | SHA-256 |
|---|---|---|
| `data_plane/config/STATUS_VECTOR_DAILY.json` | daily layer **ACTIVE**; current DSV r2; external GRANTED; cadence DAILY; claim ceiling（production NOT_CLAIMED / live NOT_AUTHORIZED / remote NOT_CLAIMED） | `97e4018ea7a3f67200a2d6632ffae10018ccebd5c3fe211aad04203abfcdf960` |
| `data_plane/config/provider_profile.yaml` | `daily_layer: state ACTIVE` + DSV r2 + TWSE-only + rights RIGHTS-DAILY-2026-08-13-002（中文註解完好, 無 mojibake） | `b68d3993241ce3bed37b538a6e4ce84548851c9057dcd0a680962d4be77ce2b6` |

TS-014 `STATUS_VECTOR.json`（package/runtime 域, TT-TS014-001 BLOCKING）**未動**——與 daily-layer 啟用正交，claim 紀律維持。

## 3. 每日自動更新機制

| 邊 | 值 |
|---|---|
| 產品能力 | `backfill_daily.update_incremental()`（codex-authored, WO-RP2-DAILY-004）: 抓取近 2 個月 × 258 symbols, idempotent skip（receipt+sha 比對, **不產生 SKIP journal 雜訊**）, 有新列才重建 core/duckdb + 註冊日期戳新 DSV（parent lineage 動態自 catalog）; 無新列 → NO_CHANGE 不動 DSV |
| 排程 | Hermes cron `d0d31ffedd07`「SQS Daily TWSE OHLCV Auto-Update」：**每日 20:00 Asia/Taipei**（`0 20 * * *`, forever, no_agent, deliver=local）; 下次 2026-08-14 20:00 |
| 執行鏈 | `daily_twse_update.py`（cron wrapper, sha `7819eaf5…`）→ `run_daily_update.py`（runner, sha `bb935f01…`）→ update_incremental → check_daily 11/11 → summary |
| 驗證 | 每次更新後跑 check_daily; FAIL → alert（runner exit≠0, cron 記錄錯誤） |
| 失敗語義 | TWSE 瞬時錯誤 → 記入 failures, 不落新 DSV; 隔日自動重試（idempotent） |

## 4. Dry-run 驗證（2026-08-13）

`rawlogs/daily_update_dry_run_2026-08-13.log`（sha `cd370075…`）：

```json
{"update":{"status":"NO_CHANGE","new_rows":0,"fetched_artifacts":0,"skipped":516,"failures":[],
            "dataset_version":"DSV-DAILY-2026-08-13-r2"},
 "check_daily":{"verdict":"PASS","checks":11,"failed":[]}}
```

- 516 次比對全數 SKIP（無網路抓取、無 journal 新增）；**DSV r2 原封不動**（catalog/manifest 驗證 hash 不變）。
- 後續交易日（如 2026-08-14）將有 new_rows > 0 → 自動註冊 `DSV-DAILY-2026-08-14-r1`（parent=r2, lineage 於 manifest）。

## 5. 獨立驗收（AO lane, deleg_66dab23a）

**PASS 9/9**（VERIFY_ONLY, read-only, mutation=0）：C1 啟用向量內容｜C2 provider_profile 中文完好 + daily_layer｜C3 codex functions 存在 + 動態 parent｜C4 dry-run log（NO_CHANGE/516/11）｜C5 catalog r2 原樣（`8dca5dae…`）+ 無新版本｜C6 manifest 不變｜C7 spine writer=codex（checker≠maker）｜C8 raw sha 10/10 命中 receipts｜C9 claim discipline。

## 6. Claim 邊界

```text
DAILY_OHLCV_LOCAL_BACKTEST_DATA_LAYER_PASS（EXTERNAL FINAL ACCEPTED）— SQS 回測資料源正式啟用
production autonomy = NOT_CLAIMED ｜ SQS live trading = NOT_AUTHORIZED ｜ remote deployment = NOT_CLAIMED
策略獲利能力 / IS-OOS / TCA / broker runtime = NOT_CLAIMED / NOT_RUN
每日更新僅擴充 frozen TWSE daily layer（新日期 → 新 DSV version, lineage 保留）
```

## 7. 終止

```text
SQS_DAILY_LAYER = ACTIVE（DSV-DAILY-2026-08-13-r2, EXTERNAL FINAL ACCEPTED）
DAILY_AUTO_UPDATE = CONFIGURED（cron d0d31ffedd07, 每日 20:00 +08, dry-run NO_CHANGE PASS）
WO-RP2-DAILY-004 VERIFIED（maker=codex, checker=AO lane, mutation=0）
STOP
```
