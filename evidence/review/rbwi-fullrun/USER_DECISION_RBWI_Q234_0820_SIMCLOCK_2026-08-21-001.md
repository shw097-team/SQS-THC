---
decision_id: USER_DECISION_RBWI_Q234_0820_SIMCLOCK_2026-08-21-001
authority: USER
decided_at: 2026-08-21T11:02+08:00
status: ACTIVE
supersedes: N/A
supersession_basis: N/A
bound_into: WO-RBWI-FULLRUN-001 / board rbwi-fullrun-2026-08-14
context: RBWI 4+1 PACK v2026.08.14-r2 Q2-Q4 financial segments normally require live XQ/PAPER
  session + FDA authorization + per-action HITL-APPROVAL/1 (entry needs HUMAN_ENTRY_APPROVAL).
  On 2026-08-21 (Fri) at ~10:52 the Q2 opening window (09:00-09:30) had already closed and no
  FDA HITL token was minted for the session.
---

# USER DECISION — RBWI Q2–Q4 以 8/20 模擬時鐘補跑

使用者明確裁決（2026-08-21 上午）在 Q2–Q4 無法於當日 live 時窗執行時，改採**「昨日 8/20 模擬時鐘」**
方式補跑，以 8/20 資料為背景執行 Q2–Q4 完整實跑；並同時進行 FDA evidence manifest defect 的
FAR 必要性研究與派修方案。

## 1. 兩條工作軌

1. **FAR 研究軌**：Fabric FDA evidence manifest 對 `FDA_USER_GUIDE.md` 的 hash mismatch——
   以 FAR 自研究框架判定派修必要性與具體派修方案（Gate 1 後呈報）。
2. **RBWI Q2–Q4 模擬時鐘補跑軌**：以 8/20 為模擬交易日，使用 8/20 當日資料（daily/minute 皆須取得）
   在**模擬時鐘（SIM）模式**下執行 Q2（Opening/S1）、Q3（Midday/S2）、Q4（Close/Post-market）
   的完整決策鏈、資格判定、風險、與（如觸發）模擬 PAPER 動作，並做 readback 與 checkpoint freeze。

## 2. 誠實 claim ceiling（不得越界）

- 本補跑是 **SIM 模擬**，受 `LOCAL_PAPER_SIMULATION_ONLY` 邊界約束，**非 live 執行**。
- 不宣稱 live/PAPER-XQ 真實成交、不宣稱 production、不進行任何 broker/live write。
- 模擬時鐘補跑若因資料可取得性無法完整重現 live 市場（例如 minute 覆蓋不足），
  須以 `qualification-proxy` 明確標註，**不得把 proxy 當成真實成交**（沿用 Spartoi 誠實界線）。
- Q2–Q4 的 live XQ/PAPER 執行權限仍維持 PENDING（非本補跑可授予）；本補跑不取代 live HITL。

## 3. 資料前置

- daily 層目前 max=2026-08-13（258 symbols）；minute 層 max=2026-08-10（50 symbols）。
- 執行前須先取得 8/20 資料；若 minute 8/20 無法取得（覆蓋不足），填補方案以 daily 近端 + 明確 proxy 標註。

## 4. 產物要求

- 每 segment 產出 `SEGMENT_DENOMINATOR_<Qx>.tsv`（8/20 版本）+ checkpoint freeze（SIM 標記）。
- 單一 evidence MD（primary home `SQS-THC\evidence\rbwi-fullrun\`）+ 三 root byte-identical 鏡像。
- fresh-context AO VERIFY_ONLY lane 驗收後始可 promotion。

decider: CURRENT_USER (via Hermes clarify)
recorded_by: Hermes Agent
