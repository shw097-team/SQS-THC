# 缺陷與修補紀錄｜WO-RP2-DAILY-002 閉環（r2，supersedes r1 版）

```yaml
artifact_id: DEFECT_AND_REPAIR_RECORD_DAILY_R2_2026-08-13
workorder: WO-RP2-DAILY-002
supersedes: DEFECT_AND_REPAIR_RECORD.md (EV-DAILY-003, sha 454abb3d…)
scope: r1 完整缺陷鏈 + 本輪新增缺陷（PIT clock、audit blind-spot、operational）
generated_at: 2026-08-13
```

## 1. r1 缺陷鏈（沿用，未重開）

`TPEX_OFFICIAL_API_UNREACHABLE`、`BACKFILL-CONCURRENCY-FIX-001`、`BACKFILL-308-TRANSIENT-001`、`BACKFILL-SILENT-EMPTY-MONTH-001`、`BACKFILL-EMPTY-FRAME-PERSIST-001`、`BACKFILL-SYMBOL-DTYPE-DUCKDB-001`、`PARTIAL-MONTH-PERSIST`、`ZERO-TRADE-ROW-DROP`（澄清為正確行為）——完整內容見 r1 版 `DEFECT_AND_REPAIR_RECORD.md`。

## 2. 本輪新增缺陷

### D-2026-08-13-001｜PIT-KNOWN_AT-SAME-DAY-001（CRITICAL，已修）

- **現象**：raw 與 core 的 `known_at == asof == bar_date`（Date 粒度）。
- **後果**：依上游決策時點 predicate `known_at <= decision_time`，同一交易日盤中決策（如 09:30）會「看到」當日收盤——**lookahead hazard**。外部 DA-EXT-004 要求 clock 正確性證明（非僅 non-null）。
- **判定**：實質 PIT 語義缺陷（evidence 證實 → 依外部報告 3.2 觸發 NARROW_REPAIR）。
- **修補**（Codex WO-RP2-DAILY-002, EXIT=0）：canonical core 材料化時 `known_at := asof + 1 曆日`（保守 EOD 可用性：D 日收盤自 D+1 00:00 起可用）；raw 保持 as-received（不可變，hash 綁定）。clock 映射：`asof`=valid/effective、`known_at`=authorized_available、`retrieved_at`=technical_ready、raw immutable=revision N/A（無修訂）、`source_identity`=provenance。
- **驗證**：DSV r2 重建後 C10 `wrong_clock=0`（221,349 列全數 known_at==asof+1d）；PIT canary 負例 PASS（2026-08-13 收盤列於 08-13 09:30 決策不可見、08-14 09:00 全可見）。
- **DSV 治理**：r1 為已封存 snapshot（catalog r1 列 + manifest r1 bytes `9b3421dc…` 保留），r2 為 superseding 新 snapshot（lineage: parent_version r1 + parent_manifest_sha256）。

### D-2026-08-13-002｜REFERENCE-CALENDAR-BLINDSPOT-001（AUDIT，已閉合，0 缺陷）

- **現象**：以 1101 為基準日曆的舊審計，漏看 1101 自身缺 2025-08-13（該日為 1101 除權息日，官方 `volume=0, close='--'`，parser 正確丟棄；其餘 257 檔皆有成交）——**自我參照盲點**。
- **閉合**：改以**真實市場日曆**（當日 ≥100 檔有交易 = 871 個交易日）重審；全部 3,369 個缺失日逐一對 TWSE 官方 **raw payload** 驗證分類：
  - PRE_LISTING 3,027（上市前，合法；raw 層對應合法空月紀錄）
  - NO_TRADE_DAY('--') 252（官方有列但無成交，parser 正確丟棄）
  - SUSPENSION_WINDOW 90（官方完全省略；抽驗 9945 2023-09-14..22 為減資/除權停牌窗口，09/25 復牌帶 X0.00 旗標）
  - **FETCH_DEFECT 0**
- **結果**：完整性 100% 合法；無需任何重抓。

### D-2026-08-13-003｜OPENCODEX-DAEMON-RESTART-001（OPERATIONAL，已處理）

- **現象**：Codex 執行中途 opencodex daemon（:10101）掉線（connection refused ×5），首次 run EXIT=1。
- **根因**：daemon 進程消失；`ocx stop` 的 pid 追蹤失效（healthz 仍 up）；以 `ocx start` 重啟後缺 provider credential（openai-chat authMode: key 需 OPENCODE_GO_API_KEY）。
- **處理**：netstat 找 listener pid → PowerShell `Stop-Process` 強制清掉 → 帶 `OPENCODE_GO_API_KEY`（hermes .env）重啟 → healthz OK → 重跑 Codex EXIT=0。
- **教訓**（已併入 skill reference）：daemon 重啟必須帶 credential env；`ocx stop` 失效時用 netstat+Stop-Process。

## 3. 誠實註記

- 無任何製造者自我驗收：checker = 獨立 lane（Lane-A/Lane-B, deleg_e0815dfa），maker = Codex（WO-RP2-DAILY-002 writer=codex）。
- 本輪無 re-download、無 raw mutation（raw 11,352 artifacts hash 與 receipts 一致，抽驗 30/30 + AO A9 20/20）。
