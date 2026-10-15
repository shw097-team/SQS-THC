# Data Rights 收據｜TWSE 台股日線（DSV-DAILY-2026-08-13-r2）

```yaml
artifact_id: DATA_RIGHTS_RECEIPT_DAILY_2026-08-13
rights_id: RIGHTS-DAILY-2026-08-13-001
workorder: WO-RP2-DAILY-002
binding_finding: DA-EXT-005
owner: SQS-THC / TW-ICT FSDT-Stack owner
checker: independent acceptance officer
generated_at: 2026-08-13
```

## 1. 權利綁定（purpose binding）

| 欄位 | 值 |
|---|---|
| source / provider | **TWSE（台灣證券交易所）官方 STOCK_DAY 公開行情端點**；Yahoo Finance chart 明示 fallback（本 DSV 0 次使用） |
| purpose | **INTERNAL_RESEARCH / BACKTEST**（本機、非商業研究回測用途） |
| consumer | SQS-THC `data_plane` 本機 backtest/analytical 工作負載（DuckDB/Parquet 層），HG-KSEOS 治理之研究流程 |
| retention | 有界：DSV 範圍 2023-01-03 → 2026-08-13；`data_policy.yaml` daily retention authority=PATCH_DEFAULT（藍圖預設 5y）已由 A0 決策（UD-DAILY-OHLCV-2026-08-13-001）收斂為本 DSV 3~4 年 |
| redistribution | **NONE**（無任何外部轉發/公開重製） |
| model-use / egress | 僅限內部研究模型與回測；**無第三方 egress** |
| effective_at | 2026-08-13 |
| review_at / expires_at | **2026-11-13**（90 日檢視）；檢視後若無異動自動續期至下一檢視點 |
| revocation path | 權利撤銷時依序刪除：derived 層（duckdb/catalog 對應 DSV 列）→ core parquet → raw artifacts → receipts journal 對應列；刪除動作記錄於證據（deletion log），不得靜默跳過（對應 `privacy/register.yaml` privacy-rights-erasure 範圍） |
| evidence locator | 本文檔 + `privacy/register.yaml`（privacy-research-corpus）+ `data_policy.yaml` publish_requirements（rights_receipt）+ G02（台灣資料權 hard gate） |

## 2. 重要限制（誠實宣告）

- **official source ≠ 任意保存/再利用皆許可**：本收據為上述 purpose/retention/redistribution 之操作約束；任何新 purpose（商用、公開、第三方模型訓練）必須重新進行 rights review（G02 hard gate），不得沿用本收據。
- 資料僅供本機研究回測；不構成投資建議、不構成 live trading 授權（SQS live trading = NOT_AUTHORIZED）。
- 上游 DOC-06 要求 rights 為 hard gate：`data_policy.yaml` publish_requirements 已含 `rights_receipt`；本收據即該 gate 於此 DSV 的閉合工件。

## 3. 驗證

- 檢查：收據欄位齊全（source/purpose/consumer/retention/redistribution/model-use/effective/expiry/revocation/evidence locator 全數具值）＝ PASS。
- 負例：任何未經 rights review 的 redistribution / 商用 / egress 意圖 → FAIL_CLOSED（由 acceptance officer 依 G02 判定）。
