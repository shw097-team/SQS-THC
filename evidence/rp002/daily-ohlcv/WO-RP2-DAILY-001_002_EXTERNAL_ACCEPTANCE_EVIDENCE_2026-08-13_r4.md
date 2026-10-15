# WO-RP2-DAILY-001/002/003｜台股 Daily OHLCV 歷史回測資料層｜彙整驗收證據 r4（FOCUSED CLOSURE）

```yaml
artifact_id: WO_RP2_DAILY_001_002_EXTERNAL_ACCEPTANCE_EVIDENCE_2026_08_13_R4
formal_name: "WO-RP2-DAILY-001/002/003｜外部驗收彙整證據 r4（scope+clock focused closure）"
subject_workorders: WO-RP2-DAILY-001（VERIFIED）＋ WO-RP2-DAILY-002（VERIFIED）＋ WO-RP2-DAILY-003（VERIFIED, 本輪）
subject_dataset: DSV-DAILY-2026-08-13-r2（data 零變動；本輪為 scope/clock 語義閉環）
external_report_basis: WO-RP2-DAILY-001_002_EXTERNAL_ACCEPTANCE_REPORT_2026-08-13_r3.md（PARTIAL; 2 affected edges）
supersedes: WO-RP2-DAILY-001_EXTERNAL_ACCEPTANCE_EVIDENCE_2026-08-13_r3.md（sha 76610a65…, 保持不變為歷史）
closure_mode: FOCUSED_EVIDENCE_AND_SCOPE_SEMANTIC_CLOSURE_ONLY
generated_at: 2026-08-13
timezone: Asia/Taipei
language: zh-TW
internal_verdict: ALL PASS（check_daily 11/11、PIT canary PASS、SWARM 17/17、WO-RP2-DAILY-003 VERIFIED）
external_final_acceptance: PENDING（由外部驗收官依 §5.4 promotion conditions 裁決）
```

> 本檔回應 r3 之 2 條 affected edges：**FOCUSED-01（scope/listing venue/provider provenance）** 與 **FOCUSED-02（Five-Clocks semantic）**。所有工件 hash 皆可由本檔指向之 exact 路徑重新計算；本檔不嵌入自身 hash；三根 mirror byte-identical 後由外部重算。

---

## FOCUSED-01｜Scope / listing venue / provider provenance（DA-EXT-006 / DA-EXT-009 / DA-EXT-005-TPEx）

### 1.1 Authoritative instrument master（FOCUSED-01-A/B）

以 **TWSE 官方 ISIN instrument master**（`isin.twse.com.tw/isin/C_public.jsp`；strMode=2 上市 1,097 rows / strMode=4 上櫃 890 rows；Big5；`市場別` 欄）逐檔解析 258 symbols：

| 邊 | 值 |
|---|---|
| resolved | **258/258**（unresolved = []） |
| **listing_venue_count** | **{TWSE: 258, TPEx: 0}** |
| identity_source / as_of | TWSE_ISIN_C_PUBLIC / 2026-08-13 |
| 負例（master 可分辨上櫃） | 6182 合晶 = 上櫃（master 判 TPEx），**不在 universe**（Lane-A A4 確認） |

**Branch A 成立**：實際 TPEx symbol count = **0** → 依 r3 §3.1 修正 scope/catalog/evidence，**不重抓 OHLCV**（raw 11,352 artifacts 零變動）。

### 1.2 勘誤聲明（prefix-inference error, master-corrected）

先前 r3 E2 宣稱「TWSE + TPEx、含 38 檔 6xxx 上櫃」係**代碼前綴推論錯誤**：本 universe 之 6xxx 代碼（6005 群益證、6024 群益期、6128 上福…）經 ISIN master 判定**皆為 TWSE 上市**（市場別=上市）。已由 `SCOPE_AND_PROVENANCE_2026-08-13_r2.md`（EV-DAILY-022, sha `9f29f03c…`）正式勘誤；原 SCOPE 文件保留為歷史（EV-DAILY-008 不變）。

### 1.3 三欄分離（FOCUSED-01-C/D）

| 概念 | 值 | 依據 |
|---|---|---|
| **listing_venue** | TWSE（258/258） | ISIN master（`LISTING_VENUE_CROSSWALK_2026-08-13.json`, EV-DAILY-020, sha `c14b699b…`） |
| **provider** | TWSE_OFFICIAL（221,349 rows, 100%） | receipts（0 YAHOO; Lane-A A8） |
| **source_endpoint / source_identity** | `TWSE_STOCK_DAY:<YYYY-MM>`（全 rows） | receipts source_identity 逐窗標記; endpoint = `https://www.twse.com.tw/exchangeReport/STOCK_DAY` |

### 1.4 Scope 修正（凍結）

```yaml
MVPMarketDataScope: venue=TWSE（上市普通股 only; TPEx=0, master-proven）
  instrument_type: listed_common_stock | frequency: DAILY_EOD
  source: TWSE_STOCK_DAY 官方（Yahoo fallback 0 使用）
  start: 2023-01-03 | end: 2026-08-13
```

與上游 DOC-06 第一版 MVP（TWSE 上市普通股 + official EOD）**一致**。`DA-EXT-009`（TPEx 官方不可達）在 TWSE-only scope 下為 **NON_BLOCKING**（truthful disposition, master-proven——非 r2 之假設，係 r4 之證明）。A0 決策之 universe（Stock List 263 = TWSE 上市清單）忠實執行：263 → 5 除名 → 258。

### 1.5 Rights（DA-EXT-005 閉合）

`DATA_RIGHTS_RECEIPT_2026-08-13_r2.md`（EV-DAILY-023, sha `703c6a7e…`）：active venues = {TWSE} only；provider=TWSE 覆蓋 **100% rows**（221,349）；**無任何未證明 provider 之 TPEx rows**（r3「REOPEN for claimed TPEx data」條件不成立）。RIGHTS-DAILY-2026-08-13-002 保留全部條款（purpose/retention/redistribution/revocation/effective/review）。

### 1.6 驗證（SWARM）

- Lane-A 8/8（A1-A8）：crosswalk 一致性、universe↔crosswalk、**獨立重抓 ISIN 雙頁抽樣 25/25 match**、6182 負例、DB 不變量、負例前瞻、raw sha 15/15、provider/source 分離。
- Lane-B B3/B4/B5/B9：scope 修正內容、rights 覆蓋、4 穩定 hash 重算 MATCH（universe `25f10e9c…` / receipts `d591cf8d…` / manifest `8dca5dae…` / r3 master `76610a65…`）、資料層零 mutation。

## FOCUSED-02｜Five-Clocks semantic closure（DA-EXT-004）

### 2.1 Clock contract（owner/source-backed）

`FIVE_CLOCKS_CONTRACT_2026-08-13.md`（EV-DAILY-021, sha `9af604c5…`）materialize 五時鐘（不新增實體欄位）：

```text
event_time        = asof（交易日, EOD 日粒度）
publication_time  := availability_time := known_at := asof + 1 曆日（保守 EOD 發佈模型）
ingest_time       = retrieved_at（TIMESTAMPTZ UTC, 實際抓取）
decision_time     = consumer 決策時間戳（predicate 輸入）
```

- **Owner-backed equivalence**：`publication_time := availability_time := known_at`（owner: SQS-THC / TW-ICT FSDT-Stack；basis: TWSE 官方 EOD 發佈模型 + DOC-06 五時鐘契約 + 保守回測慣例）。
- **Conservative consequence（明示）**：D 日任何決策不得使用 D 日收盤（`known_at(D+1) > decision_time(D)` → reject）；刻意保守 trade-off。
- **Causal predicates**：P1 `known_at > asof`；P2 `retrieved_at >= asof`；P3 publication==availability（結構性 single field）；P4 `availability_time <= decision_time`（gate）。

### 2.2 Checker（Codex C11, writer=codex）

`check_daily.py` 新增 C11（causal ordering）：`publication_not_after_event=0`、`ingest_before_event=0`（0 容忍）。check_daily **11/11 PASS**（`CHECK_DAILY_VERDICT_R4.json`, EV-DAILY-024, sha `0fe4934d…`；raw log sha `458131ed…`）。

### 2.3 Negative canary（維持 PASS）

`pit_canary_r4_2026-08-13.log`（sha `0e80dd11…`）VERDICT=PASS：2026-08-13 EOD rows 存在（257），decision 08-13 09:30 → **0 visible**；decision 08-14 09:00 → **257 visible**；gated deterministic replay hash 重跑等值、gated ≠ ungated。

### 2.4 一致性

DSV manifest（`8dca5dae…`, dataset_version r2 / rows 221,349 / symbol_count 258）＝ schema metadata ＝ 本契約 subject；evidence 三邊一致。

## r3 blocker closure matrix（本輪）

| r3 Finding | r4 external-relevant state | Closure |
|---|---|---|
| DA-EXT-004 Five-Clocks | clock contract + C11 + negative canary | **CLOSED**（FOCUSED-02） |
| DA-EXT-005 rights | {TWSE} only provider coverage, master-proven | **CLOSED**（FOCUSED-01.5） |
| DA-EXT-006 scope binding | TWSE-only master-proven + 三欄分離 + 勘誤 | **CLOSED**（FOCUSED-01.1–1.3） |
| DA-EXT-009 TPEx | TPEx=0（Branch A）→ TWSE-only 下 NON_BLOCKING | **CLOSED**（FOCUSED-01.4） |
| （r2 已閉合）DA-EXT-001/002/003/007/008 | 不變, 三根證據持續有效 | CLOSED |

## TT register（r3 §4.2 新增, 全數閉合）

| TT | 狀態 | 閉合證據 |
|---|---|---|
| TT-DAILY-EXT-R3-SCOPE-001（CRITICAL） | **CLOSED** | ISIN master crosswalk 258/258 TWSE + 三欄分離（EV-DAILY-020/022） |
| TT-DAILY-EXT-R3-TPEX-001（CRITICAL conditional） | **CLOSED（conditional 不成立）** | TPEx=0（Branch A; master + Lane-A A4 負例）→ 無需 TPEx acquisition |
| TT-DAILY-EXT-R3-RIGHTS-001（HIGH conditional） | **CLOSED** | rights r2 覆蓋 {TWSE}（EV-DAILY-023） |
| TT-DAILY-EXT-R3-CLOCK-001（HIGH） | **CLOSED** | FIVE_CLOCKS_CONTRACT + C11 + canary（EV-DAILY-021/024） |

## E1–E12（r3 已閉合項目, 本輪複述摘要）

E1 candidate identity（WO-001/002/003 VERIFIED, maker=codex, checker=swarm lanes）｜E3 raw manifest（11,352 artifacts / receipts `d591cf8d…` 13,332 lines）｜E4 typed schema（daily_bars 全 typed, 0 text financial）｜E5 coverage（871 trading days, 3,369 missing = 全數合法, **0 fetch defects**）｜E7 rights（r2 版）｜E8 RAW_UNADJUSTED_ONLY + typed BLOCK｜E9 check_daily 11/11 raw log｜E10 deterministic replay + negative fixtures｜E11 AO receipts r3（`7be6777c…`）+ r4（`118c2cd6…`）｜E12 rebuild drill（r2 執行）+ raw immutability + secret scan 0 + porcelain 歸因。

## Claim 邊界（honest）

```text
DAILY_OHLCV_LOCAL_BACKTEST_DATA_LAYER_PASS（candidate for EXTERNAL FINAL ACCEPTED, 依 r3 §5.4 條件全數成立）
production autonomy = NOT_CLAIMED ｜ SQS live trading = NOT_AUTHORIZED ｜ remote deployment = NOT_CLAIMED
策略獲利能力 / IS-OOS / TCA = NOT_CLAIMED（上層 consumer 責任）｜ broker/runtime qualification = NOT_RUN
TPEx 擴張 = 未納入本 DSV（master-proven 無 TPEx 掛牌股）; 未來若需 TPEx → 新 scope semantic version + owner approval + authorized acquisition
```

## 終止

```text
INTERNAL VERDICT = ALL PASS
WO-RP2-DAILY-003 VERIFIED（maker=codex, checker=swarm-lane-b-ao, mutation=0）
FOCUSED-01 = CLOSED（listing_venue 258/258 TWSE, provider/source 三欄分離, TPEx=0, rights 覆蓋）
FOCUSED-02 = CLOSED（five-clocks contract + C11 + negative canary PASS）
EXTERNAL FINAL ACCEPTANCE = PENDING —— 依 r3 §5.4 之 7 項 promotion conditions 全數成立, 由外部驗收官裁決
STOP
```
