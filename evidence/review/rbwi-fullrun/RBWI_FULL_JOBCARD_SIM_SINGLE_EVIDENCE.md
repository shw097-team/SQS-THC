# 完整 JobCard 交付補齊 — 單一證據（RBWI SF-00..17 + Spartoi SF-04..12）

- **WO**: WO-RBWI-FULLRUN-001（SPINE 既有, 續跑）
- **USER_DECISION**: 全自動模擬模式（2026-08-21；FAR 根因修補）
- **前置**: `FAR_REVIEW_PREVIOUS_EXECUTION_2026-08-21.md`（前次 0/18 完整根因）、`FULL_RUN_PLAN_2026-08-21.md`
- **模式**: `SIM_FASTEST_ACCEL`；盤中段 `qualification-proxy`；無 FDA/XQ realtime
- **Claim ceiling**: 完整交付物已產出且誠實 = SIM/資格代理，**非實盤成交、非 live**

## 1. 修補內容（前次缺口 → 本次）

| 前次缺口（FAR 證實） | 本次補齊 |
|---|---|
| RBWI 0/18 JobCard 完整、13 PARTIAL、5 MISSING（SF-05/09/10/11/14） | ✅ **18/18 全量收據**，含 MISSING 補齊（SF-05 S1 obs、SF-09 S2 obs、SF-10 S2 決策+cutoff、SF-11 FLAT、SF-14 archive manifest） |
| FDA/XQ 路由誤判（no_authorization 沒帶 route-id → 整段跳過 FDA） | 誠實標注 fda_xq=NOT_ENGAGED_SIM；live 建倉待條件 3 HITL；參考已教訓化 |
| Spartoi 只跑日收盤 proxy，無盤中段 | ✅ **補 SF-04..12 盤中收據（9 張）**：S1/S2/部位/收斂，標 qualification-proxy |

## 2. 產出（raw index）

Primary home: `SQS-THC/evidence/rbwi-fullrun/FULL_JOBCHARD/` + `SQS-THC/evidence/spartoi-preopen/fullintraday/`

- **RBWI 18 收據**：`SF-00..SF-17_*.json` + `FULL_JOBCHARD_SUMMARY.json`
- **Spartoi 9 收據**：`SF-04..SF-12_*.json`
- **執行器（gitignored var）**：`var/rbwi-fullrun/full_jobcard_executor.py`、`var/spartoi-preopen/full_intraday_supplement.py`
- **自檢**：`var/rbwi-fullrun/check_full_jobcards.py` → **108/108 PASS**
- **AO 判決**：`evidence/rbwi-fullrun/AO_VERDICT_FULL_JOBCARD.json`

## 3. 功能/目標檢測 + 獨立驗收

- `check_full_jobcards.py` → **108/108 PASS**（18 RBWI present + real outputs、prior-MISSING 已補、
  honesty 全綠、Spartoi SF-04..12 present、no broker/fills）。
- **獨立 AO（fresh VERIFY_ONLY）**: `PASS-with-observation`（33/33, blocking=[]）。
  非宣稱：全收據 broker_write=false/filled=0/SIM_FASTEST_ACCEL；關鍵字掃描零 live 命中；
  SF-14 manifest sha 實證符；SF-06 38 筆全 NO_TRADE。Observations（良性）：SF-14 archive 快照
  覆蓋 14/18；Spartoi/RBWI S1 qualified 差異為兩框架獨立（非不一致）。

## 4. Non-claims（誠實界線）

- SIM/qualification-proxy，非實盤成交、無 FDA/XQ realtime、無 broker 寫入、無 live 宣稱。
- 建倉/HITL 未鑄造（COV-11-06），全部 NO_TRADE。真實盤中需下交易日 live window + FDA 條件 2 路由 + 逐筆 HITL。

## 5. STOP / 接續

- 本輪完整交付物補齊已完成並驗收。**不停 production/live**。
- Resume: `RESUME:RBWI_FULL_JOBCARD_SIM_FROZEN`；live 段待開盤窗 + FDA 條件2/3 + 逐筆 HITL。
