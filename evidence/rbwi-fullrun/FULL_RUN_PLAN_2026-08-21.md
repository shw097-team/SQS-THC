# 完整實跑方案規劃（RBWI v3.0.0 r2 上位 + Spartoi RUNBOOK&WI v2.0.0 + Spartoi P1 v2.1.0）

> 2026-08-21（週五）16:05 呈報，供用戶確認後執行（HITL）。
> 前置：FAR_REVIEW_PREVIOUS_EXECUTION_2026-08-21.md（前次非完整實跑，根因已證實）。
> 本方案把「完整實跑」定義為：三文件定義的 **RBWI SF-00..17（18 JobCards）全量** 與
> **Spartoi SF-00..31** 各級股池/分析/劇本/bias/位置/HITL/封存 成品，且**盤中段以 FDA 開啟真實 XQ**。

## 0. 誠實界線（claim ceiling）

- 一次一方；**不把「模擬/代理」宣稱為「實跑/成交」**。
- 盤中/建倉/金融動作 → 逐筆 **HITL**（COV-11-06，不可自批）。
- FDA 授權：**條件 2**（ACTIVE 路由 ROUTE-SQS-XQ-GLOBALWINNER-001：XQ setup/觀察/readback 非建倉，
  含 XQ_LAUNCH_LOCATE/XQ_PAPER_CONFIG/XQ_LOG_EXPORT_READBACK/XS_COMPILE_PASS/XS_COMPILE_FAIL_READBACK）
  + **條件 3**（建倉/進場需用戶逐筆 HUMAN_ENTRY_APPROVAL）。
- live/production 不宣稱。

## 1. 時程（台股交易日時窗）

| 段 | 時窗 | 可執行狀態 | 說明 |
|---|---|---|---|
| SF-00 控制面 | 每日開盤前 | ✅ | 獨立於交易時窗，任何資料層可做 |
| SF-01/02/03 週級/盤前 | 盤前 | ✅（資料層真算） | 需真實日線資料，可在非盤中完成 |
| SF-04..12 盤中（S1/S2/部位/收斂） | 09:00–13:10 | ⚠️ 需 live+FDA 或 SIM | 真實盤中 → **下交易日**；模擬 → 立即（代理標註） |
| SF-13 盤後復盤 | 13:30 後 | ✅ | 資料層、SF-14 封存同 |

**關鍵**：今天是週五 15:47 已收盤 → **真實盤中 XQ 段今天無法跑**；可立即做的 = 全量 JobCard 中
「資料可算」的部分（SF-00/01/02/03/13/14 等）＋ FDA/XQ 盤前設定（下交易日開盤前）。真實 S1/S2 需下交易日開盤段。

## 2. 授權路徑（依序）

1. **FDA 條件 2**：`fda_preflight.py --route-id ROUTE-SQS-XQ-GLOBALWINNER-001 --action-class <CLASS>`
   → PASS 後做 XQ 桌面 非建倉 操作（setup / 觀察 / readback / 編譯）。
2. **FDA 條件 3（建倉）**：先用 FDA 開啟 XQ → 對每個擬進場標的 pause → 用戶逐筆 HUMAN_ENTRY_APPROVAL
   （含 symbol/side/qty/risk ceiling/場景 ref）。
3. 若用戶授權 **模擬模式** → SIM_FASTEST_ACCEL，全量交付物照樣產出，但徹底標 `SIM/proxy`、不宣稱成交。

## 3. 交付物清單（R5–R8 補齊對照）

### RBWI SF-00..17（canonical JobCards，18 卡全量）
| SF | 名稱 | 交付物 | 狀態路徑 |
|---|---|---|---|
| SF-00 | Runtime Bootstrap | RuntimeContext/RoleBinding/ToolAllowlist/RunReceipt | 全量產出（補 ToolAllowlist） |
| SF-01 | Weekly Context | WeeklyContextPackage（regime/bias/事件） | ✅已有，補 bias 全字段 |
| SF-02 | Daily Freeze | DailyRunExecutionPackage | ✅已有 |
| SF-03 | Pre-open Candidate | SessionCandidatePool-S1 / 各 tier | ✅已有，補全字段 |
| SF-04 | Opening Scenario Calibration | ScenarioTree/劇本（5 分支） | 補齊（含 live 或 sim） |
| SF-05 | S1 Setup Observation | S1 技術觀察（ICT/MTF） | **補 M**（前次 MISSING） |
| SF-06 | S1 Qualification→Risk→HITL | SetupQualification/Risk/HITL/OrderIntent | 補齊 |
| SF-07 | Midday Reassessment | 午盤重估 | 補齊 |
| SF-08 | S2 Candidate Refresh | SessionCandidatePool-S2 | 補齊 |
| SF-09 | S2 Setup Observation | S2 技術觀察 | **補 M** |
| SF-10 | S2 Qualification→Risk→HITL | 第二段決策鏈 | **補 M** |
| SF-11 | Position Management | 部位/收斂/停損 | **補 M** |
| SF-12 | Close/Reconcile/Overnight | 對帳/OvernightDecision | 補齊 |
| SF-13 | Replay/Learning | ReplayReceipt/LearningCandidate | 補齊 |
| SF-14 | Daily Archive | version_host/封存/證據縮減 | **補 M** |
| SF-15 | Independent Risk Service | 獨立風險/否決 | 補齊 |
| SF-16 | Agent/Tool Capability Admission | 能力准入 | 已有 PREOPEN 佔位→補成品 |
| SF-17 | Operator Cockpit/HITL | HITL/覆寫/ACK | 已有佔位→補成品 |

### Spartoi RUNBOOK&P1（SF-00..31）
| 組 | 交付物 | 狀態 |
|---|---|---|
| 週級/盤前（SF-01/02/03） | weekly_pack / daily_pack / S1_final / xs / preopen_risk | ✅ 已有（14日 sim） |
| **盤中（SF-04..12）** | S1/S2 觀察、S2 refresh、部位管理、收斂 | ⚠️ **前次僅日線 proxy**，需補（真實=FDA+下交易日）|
| 盤後（SF-13/14） | daily_report/annual/feedback / version_manifest | ✅ 已有 |
| 貫穿（SF-00/15/16/17） | RTContext/風險/HITL/能力 | 補齊 |

## 4. 執行/驗收/自迭代

1. 逐 JobCard 比對 → 補缺（獨立 lane 載入 canonical 每卡 outputs）。
2. 資料層真算 + FDA/XQ 桌面（授權內）＋ 模擬代理（標註）。
3. 自動檢測（DONE/PARTIAL/MISSING 逐卡）→ 自迭代 → 重跑。
4. fresh 獨立 AO VERIFY_ONLY → 單一 Evidence MD → 三根 byte-identical 鏡像。
5. 不達到「全量一致」不宣告完整實跑完成。

## 5. 需要用戶授權的決策

- **A**：FDA 條件 2 授權用 ACTIVE 路由做 XQ 桌面操作（下交易日，盤前 setup + 盤中 readback）？ 是/否
- **B**：盤中建倉採**逐筆 HUMAN_ENTRY_APPROVAL**（真實）或**模擬 SIM**（代理）？ 
- **C**：今天（已收盤）是否先做「資料可算全量交付物」補齊（SF-00/01/02/03/13/14 等），盤中段等下交易日？ 是/否