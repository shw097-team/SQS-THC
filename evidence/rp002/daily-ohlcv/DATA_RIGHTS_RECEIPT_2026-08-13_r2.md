# Data Rights 收據 r2（supersedes DATA_RIGHTS_RECEIPT_2026-08-13.md）｜WO-RP2-DAILY-003

```yaml
artifact_id: DATA_RIGHTS_RECEIPT_DAILY_R2_2026-08-13
rights_id: RIGHTS-DAILY-2026-08-13-002
workorder: WO-RP2-DAILY-003
binding_finding: DA-EXT-005（PARTIAL / affected reopen → CLOSED）
supersedes: RIGHTS-DAILY-2026-08-13-001（EV-DAILY-009, sha 4bb381c4…）
owner: SQS-THC / TW-ICT FSDT-Stack owner
checker: independent acceptance officer
generated_at: 2026-08-13
```

## 1. Provider 覆蓋（master-proven, TPEx 為 0）

依 `LISTING_VENUE_CROSSWALK_2026-08-13.json`（TWSE ISIN C_public master）＋ acquisition receipts：

```text
active venues  = {TWSE} only（258/258 symbols, TPEx = 0）
provider       = TWSE（台灣證券交易所）官方 STOCK_DAY 公開行情端點 — 100% rows（221,349）
source endpoint= https://www.twse.com.tw/exchangeReport/STOCK_DAY
rights 覆蓋    = 本收據綁定 provider=TWSE 之**全部** rows；無任何 TPEx 掛牌股 rows（無未證明之 provider）
```

> DA-EXT-005 之「REOPEN for any claimed TPEx data」條件**不成立**——master 證明 universe 無 TPEx 掛牌股，故 rights 收據僅需覆蓋 TWSE provider，即為完整覆蓋。

## 2. 權利綁定（沿用 RIGHTS-DAILY-2026-08-13-001 之全部條款）

| 欄位 | 值 |
|---|---|
| source / provider | TWSE 官方 STOCK_DAY 公開行情端點（Yahoo fallback 0 次使用） |
| purpose | INTERNAL_RESEARCH / BACKTEST（本機、非商業） |
| consumer | SQS-THC data_plane 本機 backtest/analytical 工作負載 |
| retention | DSV 範圍 2023-01-03 → 2026-08-13（A0 收斂 3~4y）; review 2026-11-13 |
| redistribution | NONE |
| model-use / egress | 僅內部研究模型; 無第三方 egress |
| effective_at | 2026-08-13 |
| review_at | 2026-11-13（90 日檢視） |
| revocation path | 依序刪除 derived → core parquet → raw → receipts 對應列（不靜默跳過, 對應 privacy-rights-erasure） |
| evidence locator | 本檔 + privacy/register.yaml + data_policy.yaml（rights_receipt）+ G02 + LISTING_VENUE_CROSSWALK_2026-08-13.json |

## 3. 限制（誠實宣告, 沿用）

official source ≠ 任意再利用許可；新 purpose 需重新 rights review（G02 hard gate）。資料僅供本機研究回測；不構成投資建議、不構成 live trading 授權。

## 4. 驗證

- 檢查：provider 覆蓋 = 實際 active venues 之 exact set（{TWSE}）、欄位齊全、revocation path 明確 ＝ PASS。
- 負例：任何未經 rights review 之 redistribution / 商用 / egress；任何 TPEx rows 未證明 provider → FAIL_CLOSED。
