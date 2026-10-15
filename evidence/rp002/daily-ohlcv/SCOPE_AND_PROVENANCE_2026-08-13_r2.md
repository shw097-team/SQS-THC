# 市場範圍與 Provenance 證據 r2（supersedes SCOPE_AND_UNIVERSE_IDENTITY_2026-08-13.md）｜WO-RP2-DAILY-003

```yaml
artifact_id: SCOPE_AND_PROVENANCE_DAILY_R2_2026-08-13
workorder: WO-RP2-DAILY-003
binding_findings: DA-EXT-006（REOPENED）, DA-EXT-009（REOPENED_BY_DEPENDENCY）
supersedes: SCOPE_AND_UNIVERSE_IDENTITY_2026-08-13.md（EV-DAILY-008, sha 1d467ac3…；其「38 檔 6xxx 上櫃」宣稱經本 r2 以 authoritative master 勘誤）
generated_at: 2026-08-13
```

## 1. 勘誤聲明（prefix-inference error → master-corrected）

先前 SCOPE 文件宣稱「venue = TWSE + TPEx、含 38 檔 6xxx 上櫃」，係以**代碼前綴推論**（6xxx ⇒ 上櫃）。本 r2 以 **TWSE 官方 ISIN instrument master**（`isin.twse.com.tw/isin/C_public.jsp`, strMode=2 上市 / strMode=4 上櫃）逐檔解析後勘誤：

- 本 universe 之 6xxx 代碼（6005 群益證、6024 群益期、6128 上福…）**皆為 TWSE 上市普通股**（ISIN 頁「市場別=上市」）。
- 已知上櫃代碼 6182 合晶（ISIN「市場別=上櫃」）**不在 universe**（此前已確立）。
- **Universe 實際 listing 分布 = TWSE 258 / TPEx 0**（Branch A）。

## 2. MVPMarketDataScope（修正後，凍結）

```yaml
MVPMarketDataScope:
  venue: TWSE（上市普通股 only; TPEx = 0 symbols, master-proven）
  instrument_type: listed_common_stock
  frequency: DAILY_EOD
  source: TWSE_STOCK_DAY 官方（Yahoo .TWO 明示 fallback, 0 次使用）
  start: 2023-01-03
  end: 2026-08-13
  listing_venue_identity: TWSE_ISIN_C_PUBLIC（258/258 resolved, identity_asof 2026-08-13）
```

> 此 scope 與上游 DOC-06 第一版 MVP（TWSE 上市普通股 + official EOD）**一致**；TPEx 擴張不在本 DSV（無需 MVPMarketDataScope semantic-version bump——本 DSV 從未含 TPEx 掛牌股，先前宣稱係勘誤前之誤判）。`DA-EXT-009`（TPEx 官方不可達）在 TWSE-only scope 下為 **NON_BLOCKING**（truthful disposition, master-proven）。

## 3. 三欄分離（listing_venue / provider / source_endpoint）

| 概念 | 值 | 依據 |
|---|---|---|
| **listing_venue** | TWSE（258/258） | TWSE ISIN C_public master（每檔 `market_cell=上市`; crosswalk 證據） |
| **provider** | TWSE_OFFICIAL（221,349 rows, 100%） | acquisition receipts `provider=TWSE_OFFICIAL` |
| **source_endpoint / source_identity** | `TWSE_STOCK_DAY:<YYYY-MM>`（全 rows） | receipts `source_identity` 逐窗標記; endpoint = `https://www.twse.com.tw/exchangeReport/STOCK_DAY` |

三欄不再混用：`listing_venue` 為掛牌市場身分（master），`provider` 為資料提供者，`source_endpoint` 為實際取得端點。universe 之 Stock List 來源（`知識庫\…\Taiwan STOCK\Stock List(單行).txt`, 263 codes）經 master 驗證為 **TWSE 上市清單**。

## 4. ResearchUniversePolicy（不變, A0 closed）

263（TWSE 上市清單）→ 移除 A0 指定 5 檔（1225/1236/9918/9931/5906, TWSE 官方驗證停牌/未交易）→ **258**；四處一致（universe v3 `25f10e9c…` / check_daily C1 / catalog / duckdb）。

## 5. Crosswalk 證據

`LISTING_VENUE_CROSSWALK_2026-08-13.json`：258 rows（symbol / name / listing_venue / market_cell / isin / identity_source / identity_asof）+ `listing_venue_count = {TWSE: 258}` + `unresolved = []` + master 頁面 row 數（上市 1,097 / 上櫃 890）。負例：master 確實能分辨上櫃（6182 合晶 → TPEx），故 258 全 TWSE 為 universe 真實屬性，非 parser artifact。

## 6. 終止

```text
SCOPE = TWSE-only（master-proven）
PROVENANCE = listing_venue TWSE / provider TWSE_OFFICIAL / endpoint TWSE_STOCK_DAY 三欄分離
TPEx = 0 symbols（Branch A: 修正 scope/catalog/evidence, 不需重抓 OHLCV）
STOP
```
