# RBWI Q2/Q3/Q4 8/20 模擬時鐘補跑 — 單一外部審查證據

- **WO**: WO-RBWI-FULLRUN-001（SPINE, writer=codex, 既有, 續跑）
- **Board**: `rbwi-fullrun-2026-08-14`（K0–K6b done；Q2 gate K7b 待 live/HITL）
- **USER_DECISION**: `USER_DECISION_RBWI_Q234_0820_SIMCLOCK_2026-08-21-001.md`
- **日期**: 2026-08-21（週五）；**模擬交易日**: 2026-08-20（及 8 月全月）
- **資料集**: `DSV-DAILY-2026-08-21-r1`（08-13→08-20 增量, 163 symbols on 8/20; 258 total）
- **Claim ceiling**: `LOCAL_PAPER_SIMULATION_ONLY`；NO live / production / live-broker claim；live XQ+PAPER 維持 PENDING

---

## 1. Claim ceiling / 邊界

- 本輪是 **8/20（及整個 8 月）模擬時鐘補跑**，受 `LOCAL_PAPER_SIMULATION_ONLY` 約束。
- **fastest-acceleration**：這些日期已發生，模擬直接跳到當日完整資料一次算完（無即時 tick），換取模擬效率（user requirement 2026-08-21）。
- `filled==0`、`broker_write==False`、HUMAN_ENTRY_APPROVAL 未 mint → 全部交易意向 = `NO_TRADE` / `PENDING_HITL`。
- 盤中 / XQ market-watch / 真實 PAPER 成交 = **qualification-proxy**，非真實成交。

## 2. 執行方法還原

| Item | 值 |
|---|---|
| Executor | `var/rbwi-fullrun/q234_engine.py`（date-parameterized, fastest-accel, 支援任意 8 月日期）+ `q234_executor.py`（8/20 單日版） |
| 執行方式 | `python q234_engine.py 2026-08-20` + `python q234_engine.py all`（14 個交易日） |
| 決策鏈 | Q2 SF-04→05→06→SF-15→SF-17；Q3 SF-07..10 全新 S2；Q4 SF-12→13→14+replay |
| 資料源 | `backtest.duckdb` `daily_bars`（8/20: 163 rows; 8/11,8/13: 162 rows == 真實資料） |
| 誠實檢查 | `check_q234_sim.py`（8/20）+ `check_q234_corpus.py`（全月） → **52/52 PASS** |

## 3. 產出（raw index）

Primary home: `SQS-THC/evidence/rbwi-fullrun/`

- **42 份 sim receipts**（14 日期 × Q2/Q3/Q4）: `{Q2_OPENING_S1|Q3_MIDDAY_S2|Q4_CLOSE_POSTMARKET}_sim_2026-08-*.json`
- **9 份 checkpoints**（Q1 + Q2/Q3/Q4 × 8/20）：`RBWI_CHECKPOINTS/*`（Q2/Q3/Q4 = `SEGMENT_PASS_AND_FROZEN_SIM`）
- **denominators**: `var/rbwi-fullrun/SEGMENT_DENOMINATOR_Q{2,3,4}*.tsv`（TERMINAL_SIM）
- **AO verdict**: `AO_VERDICT_Q234_SIM_820.json`
- **USER_DECISION**: `USER_DECISION_RBWI_Q234_0820_SIMCLOCK_2026-08-21-001.md`
- **RUN_LEDGER**: `RBWI_RUN_LEDGER.jsonl`（8/20 sim + full-Aug backfill events）

## 4. Functional / target 檢測結果

- `check_q234_corpus.py` → **52/52 PASS**；`verdict=PASS`。
- 涵蓋：corpus 42 收據完整、all filled=0、all no broker write、all boundary PAPER、
  Q2 全 NO_TRADE、Q3 fresh S2 + cutoff enforced、Q4 BREAK=0 + replay hash、fastest-accel marker。

## 5. 獨立 AO（VERIFY_ONLY, fresh context）

- **Verdict**: `PASS-with-observation`（7/7 passed, blocking=[]）。
- 非宣稱驗證：42 收據零越界宣稱字樣；filled==0 / broker_write==False / SIM_FASTEST_ACCEL 全一致；
  Q2 NO_TRADE、Q4 BREAK=0、USER_DECISION claim ceiling 相符。
- Observation（良性，資料層對帳解釋）：8/11,8/13 replay_rows=162 因 duckdb 該日亦 162；
  replay_hash 為 32-bit 資料相依值（以 163==163 列數對帳為準）。
- Recorded: `AO_VERDICT_Q234_SIM_820.json`

## 6. Non-claims（honest 界線）

- 無 live / production / live-broker / real-fill 宣稱。
- 無自動憑證、無 broker write、無 XQ 桌面寫入。
- live XQ/PAPER 執行權限 **維持 PENDING**；Q2–Q4 live 段仍待下交易日開盤窗 + 逐筆 HUMAN_ENTRY_APPROVAL（COV-11-06 人類閘，不可自批）。

## 7. STOP / 接續

- 本輪模擬時鐘補跑完成並 freeze（SIM）。**不停聲 production/live**。
- Resume token: `RESUME:RBWI_Q234_820_SIMCLOCK_FROZEN`（live Q2 續跑需 live window + FDA 授權 + HITL）。
