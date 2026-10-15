# 缺陷與修補紀錄｜WO-RP2-DAILY-001（Daily OHLCV 層）

本檔記錄建置過程中發現、根因定位與修補之全部缺陷（誠實記錄，非假 PASS）。

## 資料源判定
- `TPEX_OFFICIAL_API_UNREACHABLE`：TPEx 官方 st43 端點 404、openapi 302/HTML（2026-08-13 實測）→ 以 TWSE 官方 STOCK_DAY 為唯一來源（實測涵蓋 6xxx 上櫃代碼）；Yahoo `.TWO` 保留為明示 fallback（本輪 0 次使用）。

## 抓取層缺陷
| ID | 缺陷 | 根因 | 修補 |
|---|---|---|---|
| BACKFILL-308-TRANSIENT-001 | 20 檔部分月份 HTTP 308 Permanent Redirect | TWSE CDN（HiNetCDN）併發下瞬時重定向，urllib 判無限迴圈 | 308 感知重試 + 8s 起長 backoff（重試 6 次） |
| BACKFILL-SILENT-EMPTY-MONTH-001 | 靜默空月（stat OK 但 data 空）被當「無資料」 | fetch 回空未報錯，symbol 仍標 ok | 空 artifacts 全庫掃描清除 + 重抓 |
| BACKFILL-EMPTY-FRAME-PERSIST-001 | 空 frame 仍寫成 artifact（0-row parquet）→ 永久擋重抓 | persist_artifact 無空 frame 防護 | 刪除 + 重抓 + 分類上市前合法空月 |
| BACKFILL-SYMBOL-DTYPE-DUCKDB-001 | duckdb read_parquet 將 polars String symbol 推斷為 BIGINT | duckdb parquet 元資料 quirk | 建表時 `CAST(symbol AS VARCHAR)` + core 顯式 cast |
| BACKFILL-SKIP-O2-001 | SKIP 路徑 O(n²)（latest_receipt 逐 artifact 遍歷成長中 journal） | 無索引 | dict 索引化（修補工具）+ 產品碼待 Codex 正式修 |
| BACKFILL-UNIVERSE-HARDCODE-001 | load_universe 硬編碼 263 檔 | 數量耦合 | Codex patch：改為 ≥100 合理性下限 |
| BACKFILL-ZERO-TRADE-ROW-DROP-001 | TWSE 無成交日（close='--'）被 parser 排除 | 設計 B（回測標準：排除無成交日） | 確認非缺陷；驗證 artifact 與 TWSE 真實成交日一致 |

## 治理/流程紀錄
- `UD-UNIVERSE-REMOVAL-2026-08-13-001`（用戶決策）：停牌股除名——1225 福懋油、1236 宏亞、9918 欣天然、9931 欣高、5906 台南-KY（TWSE 官方逐窗口驗證），263→258；證據 `UNIVERSE_REMOVALS_2026-08-13.md`
- `CHECK_PREDICATE_UPDATE-001`：check_daily EXPECTED_SYMBOLS 263→259→258（隨 universe 決策，Codex patch ×2）
- `DEBUG_POLLUTION-001`：2330 非 universe 成員（2329→2337），debug 測試產物已清除（raw 刪除 + receipts 剝離，journal 備份 .bak/.bak2）
- 修補工具全部置於 `HG-KSEOS/var/pciv/`（gitignored task tooling）；產品碼僅經 Codex tracked writes 修改
