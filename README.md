# SQS-THC & TW-ICT FSDT-Stack

> Cold-start landing page（新 Hermes / GPT / operator session 起點）。本頁是 landing page，
> 不是 normative source；完整使用說明見 `docs/SQS-THC_TW-ICT_FSDT-Stack使用說明文檔.md`（§3）。

## 1. 這是什麼（What this is）

SQS-THC & TW-ICT FSDT-Stack 是一個 **Financial Product / Domain Stack** 的本地實作 repo：
`src/kernel/fsdt` 是 **Financial Contract Kernel**（金融契約核心，source-resolved），提供
契約驗證、正規化、PIT 驗證與價值計算；其上為 temporal / knowledge / harness / capability
等 kernel，以及研究、風險、治理相關模組。它是 **product / domain stack**，不是系統控制平面。

## 2. 治理關係（Governance）

- SQS 在 **HG-KSEOS 治理之下**（HGK root：`C:\Projects\Agent_Workspace\HG-KSEOS`）。
- SQS **不是第二個 control plane**；HG-KSEOS 是 **sole governance / normative / WorkOrder /
  evidence / release plane**。
- **Hermes** = 受治理的 runtime / orchestration plane。
- **Codex** = primary bounded executor（在 HGK WorkOrder 授權下執行 bounded 變更）。
- SQS 的 WorkOrder、證據、里程碑均由 HGK 治理記錄收斂；本 repo 是 HGK 治理之下的 product root。

## 3. Canonical root 與東西在哪（Where things live）

- Canonical root：`C:\Projects\Agent_Workspace\SQS-THC`
- User Guide（完整使用說明）：`docs/SQS-THC_TW-ICT_FSDT-Stack使用說明文檔.md`
- SSOT 控制包（RBWI_WP_CONTROL_PACK G01..G07）目前位於 `C:\Projects\Agent_Workspace\知識庫\HG-KSEOS_SSOT\RBWI_WP_CONTROL_PACK`（source-resolved；以 fresh-read 為準）。
- 狀態向量：`STATUS_VECTOR.json`（package_status / runtime_status / production_pass）
- Stage-3 (RP-002 v2.0) evidence root：`evidence/rp002/stage3/`（gates / knowledge / s1 / wp30 / closures；final review MD `RP002_R1_EVIDENCE_FOR_EXTERNAL_REVIEW.md`，sha256 ba287aee…）
- Stage-3 PCIV-F01 closure receipts：`evidence/rp002/stage3/closures/`（CLOSURE_EXT-F01..F07 + ACCEPTANCE_OFFICER_RECEIPT + CANARY_RECEIPT）
- RP-001 里程碑關閉記錄：`evidence/review/SQS_RP001_MILESTONE_CLOSURE_RECORD.md`

## 4. Financial truth 邊界（Where financial truth lives）

- 金融契約真理 = 目前 **source-resolved Financial Contract Kernel**（`src/kernel/fsdt`）；
  source wins over doc。
- memory / retrieval 產出（knowledge/RAG 結果）**不能自我升級為 financial truth**：只能引用
  與佐證 kernel 產出，不能覆寫契約判定。

## 5. 預設模式（Default mode）

- **LOCAL / PAPER / NO-LIVE-WRITE**：無 live broker write 配置。
- Order path 一律 **HITL_ONLY**；`adapters/xq-read-watch.yaml` 為 read-only watch
  （`watch_only: true` / `write: false`）。
- Live trading 未授權；Production 未宣稱（見 §8）。

## 6. 普通 SQS 任務路由（Normal task route，RP-002 Stage-3 current）

1. 任務經 HGK 普通 admission（SharedSpine）受理；
2. Hermes runtime 承接執行（orchestration plane）；
3. router 依任務性質自動選 **DIRECT / MULTI_PROFILE_DAG / SWARM**（SQS_STACK_MANIFEST execution_modes）；
4. tracked（受追蹤）實作變更走 **Codex** bounded executor；
5. 執行 worker 來自 3 個 persistent profiles：`sqs-orchestrator`（協調）、`sqs-data-analysis`（源基分析候選）、`sqs-risk`（fail-closed 風險/裁量），Profile 不擁有 Financial Truth。

## 7. Canonical suite

```bash
PYTHONPATH=src python -m unittest discover -s tests -t .
```

- 純 stdlib + 本地 kernel imports；任何 Python 3.11 皆可（2026-08-13 實測 231 tests OK，以當次執行輸出為準）。
- 若 repo `.venv-data` venv 的 base interpreter path 失效（已知 broken），改用
  `C:\Users\user\AppData\Local\Programs\Python\Python311\python.exe`（system Python 3.11 fallback）。

## 7.5 Daily OHLCV 資料層（ACTIVE, 2026-08-13 EXTERNAL FINAL ACCEPTED）

- **資料集**：`DSV-DAILY-2026-08-13-r2`（258 檔 TWSE 上市普通股、221,349 rows、2023-01-03 → 2026-08-13、TWSE 官方 STOCK_DAY；RAW_UNADJUSTED_ONLY + 調整相依 typed BLOCK）。
- **啟用**：`data_plane/config/STATUS_VECTOR_DAILY.json`（daily layer **ACTIVE**）+ `provider_profile.yaml` `daily_layer`；外部驗收 r4 **GRANTED**（`DAILY_OHLCV_LOCAL_BACKTEST_DATA_LAYER_PASS`, 7/7 promotion）。
- **回測入口**：`data_plane/data/backtest.duckdb` → `daily_bars`（決策 predicate：`known_at <= decision_time`；同日收盤 BLOCKED）。
- **每日自動更新**：Hermes cron `d0d31ffedd07` 每日 20:00 Asia/Taipei（`backfill_daily.update_incremental()`；新列 → 新日期戳 DSV 版本 + lineage；無新列 → NO_CHANGE；更新後自動 check_daily 11 項）。
- **證據**：`evidence/rp002/daily-ohlcv/`（EV-DAILY-001..028；WO-RP2-DAILY-001..004 VERIFIED）。
- 詳細：User Guide §16。

## 8. 邊界（Boundaries）

- **Production NOT_CLAIMED**；`LOCAL_PACKAGE_PASS` ≠ production。
- **Live trading NOT_AUTHORIZED**。
- RP-001 為 **MILESTONE_CLOSED** 歷史里程碑（identity/lessons/references frozen；不重開施工）。
- Knowledge 治理（K1/KG1）：**ACTIVE**（RP-002 Stage-2 KG1/F1/CF1 PASS；SQLite/FTS5 P0 REUSE；ContextForge 1.0.7 promoted）；Qdrant `ADMITTED_DISABLED`、Neo4j `INSTALL_PROFILE_READY`，皆 default OFF。
- RP-002 v2.0 Stage-3：SQP1/S1/E1/E2/E3/R1 完成（child reducer `STAGE3_SQS_PASS_ELIGIBLE_FOR_MASTER_R1_REDUCTION`，master reducer `RP002_LOCAL_ACCEPTANCE_PASS`）；E1/E2 演進 lineage 已收斂；PCIV-F01 以 superseding receipts 閉合（accepted 歷史原封）。
- 3 persistent profiles：`sqs-orchestrator`、`sqs-data-analysis`、`sqs-risk`（`agents/profiles/`）；TW-ICT Financial Runtime Pack：`SQS/TWICT_RUNTIME_PACK_MANIFEST.yaml`（TWICT-FINANCIAL-RUNTIME-PACK/1）；Stack manifest：`SQS_STACK_MANIFEST.yaml`（RP002-STACK-MANIFEST/2）。外部最終 meta acceptance：PENDING_FOCUSED_REVIEW（production/live/remote 未宣稱）。
