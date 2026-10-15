# 用戶決策｜台股歷史資料庫 Daily OHLCV 層規格變更

```yaml
decision_id: UD-DAILY-OHLCV-2026-08-13-001
authority: USER (human decision authority)
decided_at: 2026-08-13
session: Hermes desktop / HG-KSEOS governed execution
status: EFFECTIVE
supersedes: 原規劃「Daily OHLCV 5 年、全 eligible TWSE/TPEx」
supersession_basis: 上游藍圖 data_policy.yaml retention.daily.authority = PATCH_DEFAULT（用戶對 daily retention 參數具 patch 權限）
bound_into: REQ-DAILY-001 (Shared Spine)
```

## 決策內容

1) Daily OHLCV 資料層範圍由「5 年」改為「**3 年~4 年**」：

   - 起訖：**2023-01-03 → 2026-08-13**（約 3.6 年，符合 3~4 年區間）
   - 市場：**全 eligible TWSE/TPEx**
   - 台股個股目標：**263 檔**（universe = `知識庫\SQS-THC資料庫\台股價格歷史資料\Taiwan STOCK\Stock List(單行).txt`，263 codes）

2) 本決策**必須被確實記錄並輸出為證據**（本檔即證據載體；其 SHA-256 綁定至 REQ-DAILY-001 之 source_locator，並鏡像至三根 evidence/review）。

## 背景引用

- 最終交叉確認報告（閉環版）2026-08-13：`CROSS_CONFIRM_VERDICT = PARTIAL_PASS`；gap 清單第 1 項 = Daily OHLCV 5y all-eligible 層未閉合
- 上游藍圖：`Shioaji-first TWSE-TPEx Official Reference + FinMind Conditional Accelerator 藍圖 r1`（daily tier 2-5 年、TWSE/TPEx = official reference authority）+ `data_plane/config/data_policy.yaml`（retention.daily.initial_years=5, authority PATCH_DEFAULT）
- 現有本地資料：`Taiwan STOCK/` 263 檔 `*_history.csv`（2023-01-03→2025-06-26）為 legacy 未註冊資料，可作為交叉驗證 oracle

## 交付要求（本決策定義之升級任務範圍）

- 於 SQS-THC `data_plane` 建立 Daily OHLCV 層：raw immutable parquet + core daily parquet + `backtest.duckdb` daily_bars + `catalog.sqlite` DSV 註冊 + acquisition receipts（逐窗 sha256）
- 範圍：263 symbols × 2023-01-03 → 2026-08-13
- 來源：TWSE 官方 OpenAPI 為主；TPEx 官方不可達時，記錄缺陷（TPEX_OFFICIAL_API_UNREACHABLE）並以明示 fallback（Yahoo Finance `.TWO` chart API）補足，source_identity 逐列標記
- 品質：OHLC invariants、覆蓋率、無隨機缺口、PIT 欄位、與 legacy CSV 交叉驗證

## 終止條件

```text
DAILY_OHLCV_LAYER = COMPLETE (263 symbols × 2023-01-03 → 2026-08-13, DSV registered)
或 PARTIAL + 明示缺口清單（fail-closed，交由用戶決策）
production / live trading / remote deployment 一律 NOT claimed
```
