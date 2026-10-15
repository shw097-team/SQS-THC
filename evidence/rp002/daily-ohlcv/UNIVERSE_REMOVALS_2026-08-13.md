# 用戶決策｜停牌個股自 Universe 刪除紀錄與證據

```yaml
decision_id: UD-UNIVERSE-REMOVAL-2026-08-13-001
authority: USER (human decision authority)
decided_at: 2026-08-13
session: Hermes desktop / HG-KSEOS governed execution
directive: 「若有停牌的個股,就直接從清單刪掉,並留下紀錄和證據」
status: EFFECTIVE
bound_into: REQ-DAILY-001 (Shared Spine, WO-RP2-DAILY-001)
supersedes: daily_universe_263.txt v1（263 codes）
result: daily_universe_263.txt v2（259 codes）
```

## 判定基準

check_daily C5（>14 曆日缺口）觸發 5 檔 → 逐檔以 **TWSE 官方 STOCK_DAY 現況**核對缺口窗口：
- TWSE 官方**無**該窗口交易日 → 真實停牌/未交易 → **刪除**
- TWSE 官方**有**該窗口交易日 → 抓取缺陷 → 修補保留

## 刪除清單（5 檔，263 → 258）

| 符號 | 名稱（TWSE title） | 驗證窗口 | TWSE 官方實測 | 分類 |
|---|---|---|---|---|
| 1225 | 福懋油 | 2025-04-03 → 2025-06-20 | 2025-04 僅 4/1、4/2 兩列；2025-05 全空 | 真實停牌 |
| 1236 | 宏亞 | 2023-09-27 → 2023-10-09 | 2023-09 止於 9/26（18 列）；2023-10 始於 10/11（15 列） | 真實停牌 |
| 9918 | 欣天然 | 2023-01-18 → 2023-01-19 | 2023-01 止於 1/17（13 列），無 1/18–19 | 真實停牌 |
| 9931 | 欣高 | 2023-01-18 → 2023-01-19 | 2023-01 止於 1/17（13 列），無 1/18–19 | 真實停牌 |
| 5906 | 台南-KY | 2025-02-25 → 2025-03-10 | 2025-02 有 6 個 '--' 無成交日（2/7、2/10、2/18、2/25–27）；2025-03 有 8 個 '--'（3/3–3/7、3/10、3/13、3/27）→ 2/24→3/11 連續 15 曆日無交易 | 真實未交易 |

驗證方法：`urllib` 直連 `https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=YYYYMM01&stockNo=XXXX`，逐月比對交易日集合；以上窗口 TWSE 官方回應無對應日期。

## 修補保留（無）

全部 C5 觸發檔均經 TWSE 官方核對：1225/1236/9918/9931/5906 為真實停牌/未交易（刪除）；其餘 18 檔審計缺損經順序雙取樣驗證為無成交日（'--'）正確排除，artifact 與 TWSE 真實成交日完全一致。

## 污染清除（1 檔）

| 符號 | 原因 | 處置 |
|---|---|---|
| 2330 | 不屬於 Stock List 263 codes（清單 2329 → 2337）；raw artifacts + receipts 為任務工具 debug 測試產物 | 刪除 raw/symbol=2330 + 對應 receipts（journal 先備份） |

## 最終 Universe

`data_plane/config/daily_universe_263.txt` v3 = **258 codes**（v1 移除 1225/1236/9918/9931/5906）。
除名股票 raw artifacts 歸檔於 `data_plane/data/raw/daily_twse_removed_archive/`（歷史紀錄，含 ARCHIVE_MANIFEST.json）。
證據：本檔 SHA-256 綁定至最終 review MD。
