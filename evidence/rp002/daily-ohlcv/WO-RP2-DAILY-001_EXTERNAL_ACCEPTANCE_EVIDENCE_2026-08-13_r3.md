# WO-RP2-DAILY-001/002｜台股 Daily OHLCV 歷史回測資料層｜彙整驗收證據（r3, EVIDENCE_ONLY CLOSURE）

```yaml
artifact_id: WO_RP2_DAILY_001_EXTERNAL_ACCEPTANCE_EVIDENCE_2026_08_13_R3
formal_name: "WO-RP2-DAILY-001/002｜外部驗收彙整證據（internal ALL PASS）"
subject_workorder: WO-RP2-DAILY-001（原建置, VERIFIED）＋ WO-RP2-DAILY-002（閉環/修補, VERIFIED）
subject_dataset: DSV-DAILY-2026-08-13-r2（supersedes r1；r1 已封存）
external_report_basis: WO-RP2-DAILY-001_EXTERNAL_ACCEPTANCE_REPORT_2026-08-13_r2.md（PARTIAL / NOT_GRANTED）
closure_mode: EVIDENCE_ONLY + NARROW_REPAIR（PIT clock, evidence-confirmed defect）
generated_at: 2026-08-13
timezone: Asia/Taipei
language: zh-TW
internal_verdict: ALL PASS（check_daily 10/10、PIT canary PASS、suite 231 OK、SWARM 16/16、WO VERIFIED）
external_final_acceptance: PENDING（由外部驗收官依本彙整證據裁決）
```

> 本檔為外部驗收官所需之**單一彙整驗收證據**：12 類 proof（E1–E12）全部以 exact bytes / SHA-256 / raw log 關閉，對應外部報告 DA-EXT-001..008 blockers。所有工件 hash 皆可由本檔指向之 exact 路徑重新計算。本檔**不嵌入自身 hash**（single-direction binding）；三根 mirror byte-identical 後由外部驗收官自行重算。

---

## E1 — Candidate identity（DA-EXT-001 / DA-EXT-008）

```yaml
workorder: WO-RP2-DAILY-002
requirement: REQ-DAILY-002（FROZEN v1, EVT-32788c58）
taskspec: TS-DAILY-002（ADMITTED）
maker: codex（Shared Spine workorders writer=codex；state=VERIFIED）
checker: swarm-lane-b-ao（SWARM 雙 lane, deleg_e0815dfa, VERIFY_ONLY, mutation=0）
repo_head: HGK 22e21f03 / SQS 9a70501a / Fabric 493f00d
dataset_version: DSV-DAILY-2026-08-13-r2
provider_receipts: ocx-msr458y0-5z / ocx-msra2quu-7a/7b/7c（opencode-go/deepseek-v4-flash/status 200）
evidence_md: 本檔（三根 mirror, SHA-256 等值, 見 §E13）
```

- External r2 的 blocking finding `DA-EXT-001`（canonical MD 未上傳、SHA 無法重算）→ 本檔即該 canonical evidence，SHA-256 由外部自行重算（三根 byte-identical mirror）；r1 review MD 亦已存在於三根（`RP002_DAILY_OHLCV_LAYER_EVIDENCE_FOR_REVIEW.md`）。
- `DA-EXT-008`（checker≠maker exact binding）→ `INDEPENDENT_ACCEPTANCE_RECEIPT_2026-08-13.md`（EV-DAILY-018, sha `7be6777c08e45da9e2b384657f5e653f23330f6aba323f1f05dec2f1c74c1c06`）+ Shared Spine `record_workorder_result`（checker=swarm-lane-b-ao ≠ codex, state=VERIFIED）。

## E2 — Scope identity（DA-EXT-002 / DA-EXT-006）

`SCOPE_AND_UNIVERSE_IDENTITY_2026-08-13.md`（EV-DAILY-008, sha `1d467ac324aaebae56ebae3161944b9342b0ce6338ab883efdfe25680581f2c6`）：

```yaml
MVPMarketDataScope:
  venue: TWSE + TPEx（A0 決策 UD-DAILY-OHLCV-2026-08-13-001 授權 scope 擴張, 含 38 檔 6xxx 上櫃）
  instrument_type: listed_common_stock
  frequency: DAILY_EOD
  source: TWSE_STOCK_DAY 官方（Yahoo .TWO 明示 fallback, 0 次使用; TPEx 官方不可達 = truthful disposition, non-blocking）
  start: 2023-01-03
  end: 2026-08-13
ResearchUniversePolicy:
  as_of: 2026-08-13
  candidate_count: 263
  active_count: 258
  exclusions: 1225 福懋油(2025-04-03→06-20) / 1236 宏亞(2023-09-27→10-09) / 9918 欣天然(2023-01-18→19) /
             9931 欣高(2023-01-18→19) / 5906 台南-KY(2025-02-25→03-10) —— TWSE 官方逐窗口驗證, A0 決策 UD-UNIVERSE-REMOVAL-2026-08-13-001
  venue_semantics: venue = 資料路由端點（全部 TWSE 官方）; 掛牌交易所由代碼前綴判定（已於 scope 檔凍結）
```

263→移除指定 5 檔→258 **四處一致**：universe v3（`25f10e9c…`, 258 行, 無 1225/1236/9918/9931/5906/2330）＝ check_daily C1 258 ＝ catalog symbol_count 258（r1 與 r2）＝ duckdb DISTINCT symbol 258。A0 決策 exact execution 證明（non-blocking TT 閉合）。

## E3 — Raw manifest（DA-EXT-001 佐證）

| 邊 | 值 |
|---|---|
| raw_artifact_count | **11,352** parquet（`data_plane/data/raw/daily_twse/symbol=*/start=…_end=….parquet`, zstd） |
| raw_bytes_total | 63,255,939 |
| receipts journal | `daily_acquisition_receipts.jsonl` **13,332 行**, sha256 `d591cf8d9594c47ce4748c49184718e6118b8fceff10198b2d65fcb8ce087ae9`（逐窗: symbol/source/start/end/rows/bytes/sha256/status/at_utc） |
| aggregate manifest | 每窗 sha256 即 content-addressed manifest; 隨機不可操控抽驗 30/30（seed 20260813, 本輪）+ 20/20（AO Lane-A）+ 50/50（check_daily C6）全部命中 |
| idempotency | SKIP_EXISTS 以 latest-per-(symbol,source) 計; re-fetch 等值（receipts 與 artifacts 1:1, 11,352 keys） |
| source identity | `TWSE_STOCK_DAY:<YYYY-MM>`（全 221,349 列 TWSE_OFFICIAL; YAHOO 0 列） |
| 除名股歸檔 | `raw/daily_twse_removed_archive/`（1225/1236/9918/9931/5906 + ARCHIVE_MANIFEST.json, 歷史紀錄） |

## E4 — Schema / typed boundary（DA-EXT-007）

`daily_bars`（backtest.duckdb）14 欄全 typed：`symbol VARCHAR`（CAST 顯式, 防 read_parquet BIGINT 推斷 quirk）、`date DATE`、`open/high/low/close/amount DOUBLE`、`volume BIGINT`、`provider/venue/source_identity VARCHAR`、`retrieved_at TIMESTAMP WITH TIME ZONE`、`asof/known_at DATE`。

- 無文字型金融欄位（AO A2/P4 驗證：text-typed financial columns = 0）。
- PK = (symbol, date)：C4 重複 = 0。
- Coercion error path：parser 對無效/缺欄列 **reject（continue）**，不靜默寫 NULL/0（backfill_daily.py fetch_twse_month 之 TypeError/ValueError → skip）；無成交日（close='--'）明示排除（ZERO-TRADE-ROW-DROP 為正確行為）。
- timezone/trading_date 政策：date = TWSE 交易日曆日；retrieved_at = UTC 實際抓取時點。
- schema migration：r1→r2 為 derived 層重建（同 schema, known_at 值修正）+ catalog version 記錄 + manifest lineage。

## E5 — Coverage / completeness（DA-EXT-006 佐證）

`RAW_ARTIFACT_SUMMARY_2026-08-13.json`（EV-DAILY-012, sha `30969d545ae69631b18a5f5c75d520797c9df63228fdb3a3ce22da97afee0c92`）：

- **真實市場日曆 871 個交易日**（2023-01-03..2026-08-13, 判準：當日 ≥100 檔有交易）。
- 258 symbols × per-symbol rows/min_date/max_date（檔內完整列表）。
- 全庫 3,369 個「對日曆缺失日」**逐一以 TWSE 官方 raw payload 驗證分類**：
  - PRE_LISTING 3,027（上市前, 合法；raw 層對應合法空月紀錄）
  - NO_TRADE_DAY('--') 252（官方有列但無成交, parser 正確丟棄）
  - SUSPENSION_WINDOW 90（官方完全省略；抽驗 9945 2023-09-14..22 為減資/除權停牌窗口, 09/25 復牌帶 X0.00）
  - **FETCH_DEFECT = 0**
- C5：max_gap 14 曆日, >14 檔數 = 0；silent-empty-window 偵測：空月分類（pre-listing 合法空月 vs 瞬時空月）已於 r5/r6 修補鏈閉合。

## E6 — PIT / Five Clocks（DA-EXT-004）

clock 映射（canonical equivalent, 已於 rebuild 修正並凍結）：

| Five-Clocks | 本 DSV 欄位 | 值/derivation |
|---|---|---|
| valid/effective time | `asof` | 交易日（bar 之有效日） |
| authorized_available_at | `known_at` | **asof + 1 曆日**（保守 EOD 可用性: D 日收盤自 D+1 00:00 起可用） |
| technical_ready_at | `retrieved_at` | 實際抓取 UTC 時點（fetch 當時） |
| source_observed | `source_identity`/`provider`/`venue` | TWSE_STOCK_DAY:<month>（官方端點） |
| revision/transaction | raw immutable（無修訂）| raw 逐窗 sha256 綁定; DSV 改版 = 新 snapshot（r1→r2 lineage）, 絕不原地改寫 |

- 正確性（非僅 non-null）：C10 `wrong_clock = 0`（221,349 列全數 known_at == asof+1d）。
- decision-time predicate：**bar 可見 iff `known_at <= decision_time`**。
- 負例（PIT canary, `pit_canary_r2_2026-08-13.log` sha `0e80dd11d792eeab597a47c295412f80baf407da561b73fc5a702af53d7af44a`）：
  - P2：2026-08-12 10:00 決策 → 當日（08-12）收盤列 **0 可見**（same_day=0）。
  - P3：**2026-08-13 收盤列存在於 DB（257 列），08-13 09:30 決策 → 0 可見（reject/abstain）**；08-14 09:00 → 257 全可見。
  - P5：deterministic replay gated hash 重跑等值、gated ≠ ungated（gate 確實改變決策）。
- 代表性列（1101）：
  - `2023-01-03, open 25.10, close 25.15, volume 12298521, asof 2023-01-03, known_at 2023-01-04, retrieved_at 2026-08-13T06:…Z, provider TWSE_OFFICIAL, venue TWSE`
  - `2026-08-12, … , asof 2026-08-12, known_at 2026-08-13`
- 本缺陷（r1 版 known_at==asof）已記錄 `D-2026-08-13-001 PIT-KNOWN_AT-SAME-DAY-001` 並以 DSV r2 重建修復（見 E12 之 rebuild drill）。

## E7 — Rights（DA-EXT-005）

`DATA_RIGHTS_RECEIPT_2026-08-13.md`（EV-DAILY-009, sha `4bb381c4fa9fd37962cdb60c27a2a3e82fb9979104ceffce357fecfc06ee82af`）：source=TWSE 官方、purpose=**INTERNAL_RESEARCH/BACKTEST**、consumer=本機 data_plane 研究工作負載、retention=DSV 範圍（A0 收斂 3~4y, review 2026-11-13）、redistribution=**NONE**、model-use/egress=僅內部、effective=2026-08-13、revocation path=依序刪除 derived→core→raw→receipts（不靜默跳過）、evidence locator 綁定 privacy/register.yaml（privacy-research-corpus）+ data_policy.yaml publish_requirements（rights_receipt）+ G02。官方來源 ≠ 任意再利用許可之限制已誠實宣告。

## E8 — Corporate actions（DA-EXT-003）

`CORPORATE_ACTION_POLICY_2026-08-13.md`（EV-DAILY-010, sha `534181b43f94842e289cf28f5bb6148a270140f41391e4604ab51a145c227263`）：**state = RAW_UNADJUSTED_ONLY**（無調整因子/無 CA 事件流/無 AdjustmentMethodProfile）＋ **typed BLOCK**：任何相依 total-return 或除權息/分割調整連續性之回測，未經治理路徑（CorporateActionEvent + AdjustmentMethodProfile + 獨立 checker）前**不得消費本 DSV**，違者 FAIL_CLOSED。raw 不可變保留 → 未來 adjusted 層可由 raw 重建（不需重下載）；改版以新 semantic version 發布。

## E9 — check_daily raw receipt（DA-EXT-001 佐證）

`rawlogs/check_daily_r2_2026-08-13.log`（sha `545e65e85f691667693d1e2ddcb67209895d112708159fc34fcb4877f2e5f837`）＝ verdict **PASS 10/10**（`CHECK_DAILY_VERDICT_R2.json`, EV-DAILY-013, sha `a6973e95a7b3d3245fe56185d38bc7830b23e2ba2014353d68fd6ac9aaea55b5`）：

| check | predicate（實際驗什麼） | observed |
|---|---|---|
| C1 | core 目錄數 == 258 且 duckdb distinct symbol == 258 | 258/258 |
| C2 | min ≤ 2023-01-04 且 max ≥ 2026-08-12 | 2023-01-03..2026-08-13 |
| C3 | OHLC invariants（high≥max(o,c), low≤min(o,c), o/c>0, v≥0）違規 == 0 | 0 |
| C4 | (symbol,date) 重複 == 0 | 0 |
| C5 | gap>14d 之 symbol 數 == 0 | max_gap=14, 0 檔 |
| C6 | receipts JSONL 合法 + 抽 50 檔 sha256 命中 receipts | 13,332 lines, 50/50 |
| C7 | latest-per-key receipts rows == core rows == bars rows | 221,349×3 |
| C8 | catalog DSV 註冊 rows == bars | 221,349 |
| C9 | legacy CSV（Taiwan STOCK oracle）交叉 ≥99% | 11,630/11,630 = 1.0000（20 symbols） |
| C10 | PIT 6 欄 non-null **且 known_at == asof+1d（wrong_clock == 0）** | nulls=0, wrong_clock=0 |

## E10 — Backtest canary / deterministic replay（DA-EXT-004/006 佐證）

`rawlogs/pit_canary_r2_2026-08-13.log`（sha `0e80dd11…`）：P1 clock 0 違規、P2 決策時點 gate（same-day 0 可見）、P3 負例（存在但不可見→reject）、P4 typed boundary、P5 **frozen DSV deterministic replay**（1101 gated buy-and-hold 序列 hash，重跑 byte-identical；gated ≠ ungated 證明 gate 有效）、P6 raw immutability 30/30。

- canonical suite：`rawlogs/canonical_suite_r2_2026-08-13.log`（sha `8135274d16332e1bcd3def390a83ede11ed5ebc288518cf9f00f330bb008af53`）= **231 tests OK**（0.630s）。
- IS/OOS、TCA、策略績效為上層 consumer 責任，本 data-only WO 明確 route-out（不假裝已驗）；data-gap/parity 由 C5 + E5 閉合；rights/CA gate 由 E7/E8 typed BLOCK 閉合。

## E11 — Independent acceptance（DA-EXT-008）

`INDEPENDENT_ACCEPTANCE_RECEIPT_2026-08-13.md`（EV-DAILY-018, sha `7be6777c…`）：maker=codex、checker=SWARM 雙 lane（deleg_e0815dfa, fresh context, VERIFY_ONLY, read-only, **mutation_by_checker=0**）、subject digest = 上表 6 項 exact bytes 重算一致、verdict **PASS 16/16**（Lane-A 10/10 + Lane-B 10/10）。Shared Spine：`WO-RP2-DAILY-002 state=VERIFIED, result_json.checker=swarm-lane-b-ao`。

## E12 — Rollback / rebuild / security（DA-EXT-001 佐證）

- **Rebuild drill（已實作）**：`rawlogs/rebuild_r2_2026-08-13.log`（sha `663b768d4a19dc307b9a23f20b69fd5440953e7f63099ceff772f3366717d864`）：由 immutable raw + receipts 決定性重建 core → duckdb → manifest → catalog（258 sym / 221,349 rows / 11,352 artifacts）；**raw 未動**（30/30 + AO 20/20 sha 命中 receipts）。
- Rollback pointer：git heads（HGK `22e21f03`/SQS `9a70501a`/Fabric `493f00d`）＋ r1 DSV 封存（catalog r1 列 + `legacy/daily_dataset_manifest_r1.json` = `9b3421dc…`）＋ receipts journal 備份（`.bak-20260813`）。
- Secret/PII scan：evidence + metadata + config 目錄 regex scan（sk-/AKIA/private key/password/api_key）＝ **0 發現**。
- Unauthorized writes：porcelain 依 mtime 歸因，本 WO 窗口僅 evidence + 2 product src（codex）+ universe 檔；無 live broker adapter 寫入（canonical suite + provider_profile live=BLOCKED 維持）。

## E13 — 三根 Mirror 與 SHA-256 等值

本檔與全部 evidence 工件 mirror 至 `HG-KSEOS/evidence/review/`、`SQS-THC/evidence/review/`、`Fabric/evidence/review/`（byte-identical `cp`），SHA-256 三根等值（外部可自行重算）。

## TT / CR register（外部報告 §4.2 全數閉合）

| ID | 狀態 | 閉合證據 |
|---|---|---|
| TT-DAILY-EXT-001 | **CLOSED** | 本檔 E1/E13（canonical MD bytes + SHA 可重算 + 三根 mirror） |
| TT-DAILY-PIT-001 | **CLOSED** | E6（clock 映射 + C10 wrong_clock=0 + 負例 P2/P3 + canary） |
| TT-DAILY-RIGHTS-001 | **CLOSED** | E7（RIGHTS-DAILY-2026-08-13-001） |
| TT-DAILY-CA-001 | **CLOSED** | E8（RAW_UNADJUSTED_ONLY + typed BLOCK） |
| TT-DAILY-UNIVERSE-EVIDENCE-001 | **CLOSED** | E2（263→5→258 四處一致, A0 exact execution） |
| TT-DAILY-SCHEMA-001 | **CLOSED** | E4（typed daily_bars, 0 text financial cols, coercion reject path） |
| TT-DAILY-IND-001 | **CLOSED** | E11（AO receipt 綁 exact digests, mutation=0） |

## DA-EXT findings closure

| ID | 外部裁決 | 本輪閉合 |
|---|---|---|
| DA-EXT-001 CRITICAL | canonical MD 未上傳 | **CLOSED**（本檔三根 mirror + 全部 raw logs/receipts） |
| DA-EXT-002 | authority-closed / execution evidence | **CLOSED**（E2 四處一致） |
| DA-EXT-003 HIGH | CA policy 未證明 | **CLOSED**（E8 RAW_UNADJUSTED_ONLY + BLOCK） |
| DA-EXT-004 CRITICAL | Five-Clocks 無 semantic proof | **CLOSED**（E6 + 修補 D-2026-08-13-001 + 負例） |
| DA-EXT-005 CRITICAL | rights binding 未提交 | **CLOSED**（E7） |
| DA-EXT-006 HIGH | scope 三邊 binding 未提交 | **CLOSED**（E2/E5） |
| DA-EXT-007 MEDIUM/HIGH | VARCHAR→typed boundary | **CLOSED**（E4；無修補需求——financial 欄位已 typed） |
| DA-EXT-008 CRITICAL | independent receipt 缺 exact binding | **CLOSED**（E11） |
| DA-EXT-009 | TPEx non-defect | 維持 NON_BLOCKING（TWSE+TPEx scope 已由 A0 授權） |

## Claim 邊界（honest）

```text
DAILY_OHLCV_LOCAL_BACKTEST_DATA_LAYER_PASS（frozen DSV r2: local research/backtest usability, PIT/rights/quality/lineage/replay qualified）
production autonomy = NOT_CLAIMED ｜ SQS live trading = NOT_AUTHORIZED ｜ remote deployment = NOT_CLAIMED
runtime/broker qualification = NOT_RUN（STATUS_VECTOR TT-TS014-001 BLOCKING 維持）
策略獲利能力 = NOT_CLAIMED ｜ IS/OOS/TCA = 上層 consumer 責任（route-out）
```

## 終止

```text
INTERNAL VERDICT = ALL PASS
WO-RP2-DAILY-002 VERIFIED（maker=codex, checker=swarm-lane-b-ao, mutation=0）
DSV-DAILY-2026-08-13-r2 = LOCAL BACKTEST DATA LAYER PASS（258 symbols, 221,349 rows, 871 trading days, 0 fetch defects）
EXTERNAL FINAL ACCEPTANCE = PENDING（由外部驗收官依本彙整證據裁決）
STOP
```
