# FAR 研究審查報告 — 前次「實跑」執行 vs RBWI/Spartoi 三文件完整工作流程

> 2026-08-21（週五）16:00，FAR R0–R8 審查。
> 觸發：用戶質疑前次執行「明明是實跑卻未用 FDA 開 XQ」「未產出三文件應有的分析/偏見/劇本/各級股池等全量交付物」「是否真的完整實跑」。

## 0. 結論先行（誠實）

**前次的「Q1–Q4 完成 + Spartoi 日級完成」宣稱，不成立為「三文件定義的完整實跑」。**
- **RBWI：0/18 JobCards 完整達標**（13 PARTIAL、5 MISSING（SF-05/09/10/11/14）；僅 sf-01/02/03 有專屬收據）。
- **Spartoi：14 日 × 7 檔全部是 `SIM_FASTEST_ACCEL` 日收盤模擬 proxy，非即時/盤中實作**；未產出完整 SF-04..12 盤中決策鏈與 S2/部位管理成品。
- **未以 FDA 開啟 XQ**：把「無即時交易窗 + 建倉需 HUMAN_ENTRY_APPROVAL」誤讀成「不得使用 FDA/XQ」，靜默以日線 SIM 頂替；但 FDA 有 ACTIVE 已登記受治理路由（ROUTE-SQS-XQ-GLOBALWINNER-001, 條件 2）授權 PAPER/XQ 桌面唯讀+設定操作，且缺窗也不構成跳過 FDA 桌面證據的合法授權。

## 1. FAR 根因盤點（R0–R4）

### 根因 A：FDA/XQ 授權被誤判（最嚴重）
- **表面原因**：`fda_preflight.py --action-class XQ_LAUNCH_LOCATE` 回傳 `no_authorization`。
- **真因**：preflight 未帶 `--route-id ROUTE-SQS-XQ-GLOBALWINNER-001`，故判無授權；但該路由 status=ACTIVE、未過期、owner=SQS，
  涵蓋 XQ_LAUNCH_LOCATE / XQ_PAPER_CONFIG / XQ_LOG_EXPORT_READBACK / XS_COMPILE_PASS / XS_COMPILE_FAIL_READBACK，
  **滿足 FDA 授權條件 2**。XQ 亦已安裝且有 build fingerprint（`C:\SysJust\XQLite\daqxqlite.exe`,
  sha `6c0c7cbc…`, XQLite 3.20.02, 帳號 SHW097 已登入）。
- **執行者誤判**：把「需要 live window + HITL entry」擴張成「不能碰 FDA/XQ」，故未 pause 向用戶取「條件 3」明確授權，
  也**未走條件 2 已登記路由跑可自動化的 XQ 桌面唯讀/設定**（盤前準備、S1 觀察、market-watch readback 等，非建倉動作）。
- **缺失**：未 pause + 未用 ACTIVE 路由 + 未提供 FDA 桌面證據。

### 根因 B：交付物只做了「精簡決策鏈」，非全量 JobCard（RBWI 0/18 完整）
- canonical RBWI SF-00..17 每卡有 Required Outputs/Artifacts（analysis、bias/劇本/scenario、各級股池、HITL、位置等）。
- 前次產出 = Q1（SF-01/02/03 收據 + 兩份泛化 check）+ Q2/Q3/Q4 sim 決策鏈（薄版），
  **SF-00/04/05/06/07/08/09/10/11/12/13/14/15/16/17 大多 PARTIAL 或 MISSING**（SF-05/09/10/11/14 = MISSING）。

### 根因 C：Spartoi 只跑日級 proxy，無盤中實作
- Spartoi RUNBOOK §4 + P1 v2.1.0 定義 SF-00..31（含盤中 SF-04..12、S2、部位管理）。
- 前次 14 日 × 7 檔全為 `SIM_FASTEST_ACCEL` 日收盤模擬、同一時戳，SF-13 KPI=N_A、無 S2/盤中/成交產物。

## 2. 最佳解決方案（R5–R8）

1. **FDA/XQ 真跑**：以 `fda_preflight.py --route-id ROUTE-SQS-XQ-GLOBALWINNER-001` 取 PASS；
   在授權範圍內做 XQ 桌面 setup/S1 觀察/market-watch readback（非建倉）；**建倉/金融動作**仍 pause 取 HUMAN_ENTRY_APPROVAL（COV-11-06）。
2. **完整實跑（能自動化的部分）**：補齊 RBWI SF-00..17 全量 JobCard outputs（analysis/bias/劇本/各級股池/位置/HITL/封存），
   Spartoi 補盤中-S2/部位/收斂等缺失段——用真實資料層 + 可用的 XQ 桌面證據；缺盤中即時資料處誠實標 proxy 並列出。
3. **誠實 claim ceiling**：一次一方；不把「模擬/代理」宣稱為「實跑/成交」；live 段逐筆 HITL。
4. **檢測/自迭代**：逐 JobCard 比對（DONE/PARTIAL/MISSING）→ 補缺 → 重跑 → AO 驗收 → 單一 MD 三根鏡像。

## 3. 源證（三 lane fresh-context 獨立研究）

- Lane0（授權/根因）：`Fabric...FDA_DESKTOP_CAPABILITY_MATRIX.yaml`（XQ subject）、`adapters/fda-xq-globalwinner-route.yaml`（ACTIVE 路由）、
  `FDA_XQ_BUILD_FINGERPRINT_RECEIPT.json`（XQ 已裝）。
- Lane1（RBWI 缺口）：canonical RBWI L4095-5650 JobCards vs `evidence/rbwi-fullrun/` → **0/18 完整、13 PARTIAL、5 MISSING**。
- Lane2（Spartoi 缺口）：RUNBOOK §4 + P1 vs `var/spartoi-preopen/dayflow/` → **全 SIM_FASTEST_ACCEL 日收盤 proxy**。

## 4. 非宣稱

本報告不宣稱 live/production/成交；不把 proxy 當成交；live 金融動作仍待用戶逐筆 HITL。
