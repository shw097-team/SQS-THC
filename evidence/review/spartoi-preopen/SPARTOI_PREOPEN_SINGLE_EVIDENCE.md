# Spartoi 台股當沖/隔日沖 — 收盤後+開盤前 執行單一 Evidence（single MD）

**artifact_id:** `SPARTOI_PREOPEN_SINGLE_EVIDENCE`
**runbook:** Spartoi｜台股當沖隔日沖_RUNBOOK&WI_v2.0.0 · **manual:** Spartoi｜P1_執行手冊_v2.1.0
**governance:** TW-ICT_FSDT-Stack（參照 TW-ICT_v3.0_專業技術文檔 DOC-05 / 市場資訊&台股趨勢 v2.0 等）
**candidate:** CAND-SPARTOI-W34-20260820 · **week:** 2026-W34 · **date:** 2026-08-20
**generated:** 2026-08-20T21:50+08:00 · **financial_boundary:** LOCAL/PAPER qualification · **live_broker:** NOT_AUTHORIZED

---

## 0. Claim Ceiling (verbatim)

```
SPARTOI_PREOPEN_WORKFLOW_STRUCTURAL_EXECUTION_COMPLETE
Runtime = 收盤後/開盤前 SF-01..03,13,14 deliverables produced (LOCAL/PAPER, data-derived)
Independent = PASS-with-observation (fresh-context VERIFY_ONLY lane; no blockers)
Production = NOT_CLAIMED · Live trading = NOT_AUTHORIZED · Broker write = NOT_AUTHORIZED
SF-03 live preopen (平衡價/委比/量) = PENDING_Q2/XQ_live_window
SF-13 KPI = N/A (qualification run, no live execution)
```

**Non-claims (explicit):**
- SF-03 的 preopen 資訊（平衡價/委比/量）以 **daily-close proxy** 暫代，真實 preopen 需
  Q2/XQ live window — **不成立為成交或趨勢**。
- SF-13 復盤 KPI（勝率/R-multiple/MAE-MFE…）因本窗**無實盤執行**皆為 `N_A`，只做結構性復盤。
- weekly_pack 週偏見是資格/研究脈絡，**非交易訊號**；`broker_write=false` 全場。
- 未把任何 qualification proxy 假裝成真實成交/即時行情。

---

## 1. 執行範圍與交付物（User 指定：收盤後+開盤前+補做上周~本週周級分析）

| SF | 名稱 | 時相 | 交付物 | 狀態 |
|---|---|---|---|---|
| SF-01 | 週級分析（補做上周收盤後~本週開盤前） | 收盤後→週末 | `weekly_pack.json` | DONE |
| SF-02 | 盤前分析 | 開盤前 | `daily_pack.json` | DONE |
| SF-03 | 盤前選股 | 開盤前 | `S1_final_list.json` + `xs_watchlist.xs` + `preopen_risk_report.json` | DONE(proxy) |
| SF-13 | 盤後復盤 | 收盤後 | `daily_report.json` + `weekly_report.json` + `feedback_to_method.json` | DONE(structural) |
| SF-14 | 資料管理 | 收盤後 | `version_manifest.json` | DONE |

**SF-01 週級分析產出要點（真實 daily OHLCV 計算）：**
- `bias_w`: **direction=BULL, confidence=MEDIUM**, advance_ratio=0.61 (up 155 / down 99),
  mean_ret≈+1.54%, PWH/PWL/week-open/close targets+invalidations, five-clock known_at==asof+1d.
- `W-DR/EQ50`: eq50/high/low + pd_arrays（近窗 2026-08-05..08-13）.
- `W-LQ`: old_weekly_h/l; double-top/bottom 標記待位移棒收盤確認.
- `weekly_list`: **30 檔**（流動性前 30，15-35 範圍內）含 script_score-W/risk_tags.
- `four_cards`: 敘事(正/反)×進場(正/反) 4 張完整.  `event_flags`: event/holiday/week_open_close.

**SF-02 盤前分析產出：** bias_d_draft/final（BEAR_MILD 三情境）、D-DR/EQ50、IL/EL、
**A_list=12（≤16）**、**S1_candidates=10（6-10 內）**、story_card_final；4 mutation flags false.

**SF-03 盤前選股產出：** **S1_final=8（6-10 內）**、xs_watchlist.xs、preopen_risk_report（vi/處置 ±10%）。

**SF-13 復盤：** daily_report（structural, KPI N/A）+ weekly_report + feedback_to_method；誠實標
deviation_reason=[no_execution_today, data_window_asof_2026-08-13 no_new_bars].

**SF-14：** version_manifest.json 8 runtime artifacts + 索引/可回放性。

---

## 2. 資料 / 權威基底

- 資料層：DSV-DAILY-2026-08-13-r2（258 TWSE daily OHLCV, 221,349 rows, PIT T+1）。
- 增量更新回報 `NO_CHANGE`（資料停在 8/13；今天 8/20 無新 bar）— 誠實接受，分析基準以資料內最後完整週為準。
- 權威參照：TW-ICT_v3.0 DOC-05（Universe/Candidate/MTF Bias/Scenario）、ICT&SMC、
  台股當沖 v3.0、市場資訊&台股趨勢 v2.0（five-clock/regime）。Spartoi SF 主鍵沿用 RUNBOOK/手冊。

## 3. 治理 / 方法

- HGK control plane（WO/evidence/mirror）+ Hermes orchestration + SQS-THC domain stack；
  XQ 非唯一執行端（本資格 run 未動 XQ）；`broker_write=false`。
- Kanban: board `rbwi-fullrun-2026-08-14`（Spartoi 執行卡 t_2664f7d5 completed）。
- fresh-context 獨立 Acceptance Officer lane（deleg_1a001679）→ **PASS-with-observation**。
- 非主張掃描：所有 live/broker/order/trade 命中皆是反義/排除上下文（broker_write=false、
  "NOT a trade signal"、"no live order"）。

## 4. Raw Evidence（PRIMARY home + 3 mirror roots byte-identical）

- PRIMARY: `SQS-THC/evidence/spartoi-preopen/`（artifacts/ 含 11 個產生檔 + coverage + AO verdict）
- MIRROR: `HG-KSEOS/evidence/review/spartoi-preopen/` · `SQS-THC/evidence/review/spartoi-preopen/` · `Fabric/evidence/review/spartoi-preopen/`
- 主要檔 sha256 前綴：weekly_pack=6fc44a22 / daily_pack=34579ff3 / S1_final=fbac54bc /
  xs_watchlist=1dea0d1e / preopen_risk=12a65d28 / daily_report=e3159bdb / weekly_report=8551b3b6 /
  feedback=077ef71f / version_manifest=a1ad5b8d / coverage=3936ddbc(更新後另計) / AO=9d0efca3.

## 5. Stop / Hold

```text
STOP: 本資格 run 到此閉合「收盤後+開盤前」工作流程。以下 pending：
  (a) SF-03 真實 preopen（平衡價/委比/量）+ XQ/XS 操作 → 需 Q2/XQ live 市場 window + HITL；
  (b) SF-13 KPI 復盤 + 方法回饋 → 需實際 live 執行資料；
  (c) 資料層 8/14 起至今日的新 bar（TWSE）→ 待 daily cron 依 data owner 機制推進。
未自我主張：production / live trading / remote deployment / external final meta acceptance。
```

## 6. Mirror & Readback

所有 Spartoi 產物 + 單一 MD + verdict，已 byte-identical 鏡像 primary + 三 root；
SHA-256 逐檔比對全 OK。
