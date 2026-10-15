# 市場範圍與 Universe 身分證據｜WO-RP2-DAILY-002 閉環

```yaml
artifact_id: SCOPE_AND_UNIVERSE_IDENTITY_DAILY_2026-08-13
workorder: WO-RP2-DAILY-002
subject_dataset: DSV-DAILY-2026-08-13-r2 (supersedes r1)
binding_findings: DA-EXT-002, DA-EXT-006
generated_at: 2026-08-13
```

## 1. MVPMarketDataScope（DSV 凍結範圍）

| 欄位 | 值 | 依據 |
|---|---|---|
| venue | **TWSE + TPEx**（上市普通股 + 上櫃普通股，依 A0 決策含 6xxx 上櫃代碼） | UD-DAILY-OHLCV-2026-08-13-001（「全 eligible TWSE/TPEx、263 檔目標」）；DOC-06 第一版 MVP 為 TWSE-only，本次含 TPEx 為 **A0 使用者授權之 scope 擴張**（semantic-version bump 由 A0 決策支持） |
| instrument_type | listed_common_stock | 上游 DOC-06 Part 0.1/1.1 |
| frequency | DAILY_EOD | 上游 DOC-06 |
| source | **TWSE_STOCK_DAY 官方 API**（主要）；Yahoo Finance chart 為明示 fallback（**0 次使用**，實測 TWSE 端點本身回傳上櫃代碼） | `S2R`/acquisition receipts；`TPEX_OFFICIAL_API_UNREACHABLE` 缺陷已記錄（TPEx 官方 st43/openapi 不可達，truthful disposition：TWSE 官方端點涵蓋兩市場） |
| start | 2023-01-03 | UD-DAILY-OHLCV-2026-08-13-001 |
| end | 2026-08-13 | 同上（含今日行情） |

**venue 欄位語義（明確宣告，無 silent coercion）**：`venue` 記錄**資料路由端點市場**（本 DSV 全部 221,349 列皆經 TWSE 官方端點取得，故 venue='TWSE'）。個股**掛牌交易所**可由代碼前綴判定（6xxx = 上櫃 TPEx；其餘 = 上市 TWSE）；本 DSV 之 258 檔中有 38 檔 6xxx 上櫃代碼。此語義已於本文檔凍結，任何 consumer 不得將 venue 誤解為掛牌交易所。

## 2. ResearchUniversePolicy

```text
as_of:            2026-08-13
candidate_count:  263        (UD-DAILY-OHLCV-2026-08-13-001 之 Stock List 全 eligible)
active_count:     258        (263 - 5 停牌/未交易，A0 決策 UD-UNIVERSE-REMOVAL-2026-08-13-001)
```

### 2.1 A0 決策執行證明：263 → 移除指定 5 檔 → 258

| 符號 | 名稱（TWSE title） | 停牌/未交易窗口（TWSE 官方實測） | 原因 |
|---|---|---|---|
| 1225 | 福懋油 | 2025-04-03 → 2025-06-20 | 真實停牌 |
| 1236 | 宏亞 | 2023-09-27 → 2023-10-09 | 真實停牌 |
| 9918 | 欣天然 | 2023-01-18 → 2023-01-19 | 真實停牌 |
| 9931 | 欣高 | 2023-01-18 → 2023-01-19 | 真實停牌 |
| 5906 | 台南-KY | 2025-02-25 → 2025-03-10 | 真實未交易（連續 15 曆日） |

- 原始 denominator = 263（`daily_universe_263.txt` v1）；中間 v2=259 為歷史 intermediate 狀態（`UNIVERSE_REMOVALS_2026-08-13.md` front-matter 記錄）；**最終 governed universe = 258（v3）**。
- 2330 為 debug 污染（不在 263 清單，清單 2329→2337 跳號），已清除並留 journal 備份；**非** universe 成員、非 A0 決策對象。
- 除名股 raw artifacts 歸檔 `data_plane/data/raw/daily_twse_removed_archive/`（含 ARCHIVE_MANIFEST.json）＝歷史紀錄，不參與 DSV。

### 2.2 四處一致（exact execution 證明）

| 邊 | 值 | 證據 |
|---|---|---|
| universe 檔 v3 | 258 codes（無 1225/1236/9918/9931/5906/2330） | SHA-256 `25f10e9c7dc4c7ad0f027029542c97d8d034b36e9f9de4c1cc19ad57a23c6be0`（EV-DAILY-007） |
| check_daily | EXPECTED_SYMBOLS = 258（C1） | check_daily.py + raw log |
| catalog | symbol_count = 258（DSV r1 與 r2 皆然） | catalog.sqlite dataset_versions |
| duckdb | COUNT(DISTINCT symbol) = 258 | backtest.duckdb daily_bars |

A0 決策被忠實執行：**263 → 恰好移除指定 5 檔 → 258**，四處一致，無一處殘留被刪除標的（negative fixture：任何 governed 258 universe 內出現 1225/1236/9918/9931/5906 即 FAIL）。

## 3. Scope 綁定註記

- `data_policy.yaml` daily `initial_years: 5`（藍圖預設）**僅對本 DSV 由 A0 決策取代**（3~4 年）；policy 預設值未改寫，DSV 特定範圍凍結於本證據 + manifest。
- 上游 DOC-06 第一版 MVP（TWSE-only）已由 A0 授權擴張至 TWSE+TPEx；TPEx 官方端點不可達為 truthful disposition（缺陷 `TPEX_OFFICIAL_API_UNREACHABLE`，non-blocking under 本 scope，因 TWSE 端點涵蓋兩市場且 Yahoo fallback 備而 0 用）。
