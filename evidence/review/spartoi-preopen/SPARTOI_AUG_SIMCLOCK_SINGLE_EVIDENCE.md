# Spartoi 8 月模擬時鐘日級補跑 — 單一證據

- **WO**: WO-RBWI-FULLRUN-001（SPINE, 既有, 續跑）
- **USER_DECISION**: `USER_DECISION_RBWI_Q234_0820_SIMCLOCK_2026-08-21-001.md`
- **日期**: 2026-08-21；**模擬交易日**: 全 2026-08 交易日（08-03..08-20, 14 日）
- **資料集**: `DSV-DAILY-2026-08-21-r1`
- **Claim ceiling**: SIM-only 已成日期補跑；NO live/production/live-broker/fill 宣稱；live XQ+PAPER 維持 PENDING

## 1. 範圍與方法

- 權威：Spartoi RUNBOOK&WI v2.0.0 → P1 執行手冊 v2.1.0（SF-00~SF-31 主鍵）。
- 本輪跑「收盤後、開盤前」日級流程 **SF-02 / SF-03 / SF-13 / SF-14**，per-day 落盤。
- **fastest-acceleration**: 這些日期已發生 → 模擬直接跳到當日完整日線一次算完（無即時 tick），
  `sim_mode=SIM_FASTEST_ACCEL`（user requirement 2026-08-21）。
- 盤前 live 部分（平衡價/委比/量）→ **qualification-proxy**（`daily-close-proxy`），非實盤。
- 無 fill、無 broker write、無 live 宣稱；SF-13 KPI = N_A（無實盤執行）。

## 2. 產出（raw index）

Primary home: `SQS-THC/evidence/spartoi-preopen/` + `var/spartoi-preopen/dayflow/`

- **98 件 dayflow artifacts**（14 日 × 7 檔，每日）:
  `daily_pack.json` / `S1_final_list.json` / `xs_watchlist.xs` / `preopen_risk_report.json` /
  `daily_report.json` / `weekly_report.json` / `feedback_to_method.json`
- **14 份 dayflow 目錄**: `var/spartoi-preopen/dayflow/2026-08-{03..20}/`
- **14 份 version_manifest**: `var/spartoi-preopen/archive/version_manifest_2026-08-*.json`
- **覆蓋證明**: `evidence/spartoi-preopen/SPARTOI_AUG_BACKFILL_COVERAGE.json`
- **AO 判決**: `evidence/spartoi-preopen/AO_VERDICT_AUG_BACKFILL.json`

## 3. Functional / target 檢測

- `check_spartoi_aug_corpus.py` → **129/129 PASS**（14 日期、98 artifacts、S1_final 6–10 契約、
  誠實不變量、sim_mode、consistency）。

## 4. 獨立 AO（VERIFY_ONLY, fresh context）

- **Verdict**: `PASS-with-observation`（13/13 passed, blocking=[]）。
- 非宣稱：98 artifacts 無成交欄位、broker_write!=true、SIM_FASTEST_ACCEL、
  preopen=daily-close-proxy、所有「live」字樣皆 PENDING-live-XQ 覆核。
- Observation（非阻斷）：`daily_pack.json` 以缺欄代替 `filled==0`（與 A 組顯式規格略異）；SF-13 為結構性 N_A。
- Recorded: `AO_VERDICT_AUG_BACKFILL.json`

## 5. Non-claims

- 無實盤成交、無 broker write、無 live/production 宣稱。
- live Q2–Q4 + Spartoi 盤中/真實 preopen 需下交易日 live window + FDA + HITL（COV-11-06）。

## 6. STOP / 接續

- 本輪 Spartoi 日級模擬補跑完成並驗收。不停 production/live。
- Resume: `RESUME:SPARTOI_AUG_SIMCLOCK_FROZEN`（live 段需 HITL + live window）。
