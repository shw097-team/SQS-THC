# hgk-governed-execution SKILL 拆分 — 最終驗收證據（WO-HGK-SKILL-SPLIT-001）

> 日期: 2026-08-15 · Gate 2 用戶授權（UD:2026-08-15:Gate2:PlanA）· 前置: SKILL_SPLIT_RESEARCH_REPORT_v1（EVD-SKILL-SPLIT-RESEARCH-001）+ v2（challenge 7 條件閉合）
> Claim ceiling: 本 WO 僅機械拆分 hgk-governed-execution SKILL.md 與新增 7 個 references/step-*.md；未修改其他 skill/既有 references 檔/config；未執行任何 FDA 桌面操作。

## §1 變更摘要

| 項目 | 拆分前 | 拆分後 |
|---|---|---|
| SKILL.md | 103,481 chars / 107,604 B（skill_guard BLOCKED） | 36,802 B / 567 行（guard PASS） |
| Sections | 25 H2 | 26 H2（+Routing map） |
| references/*.md | 44（含並行 session 新增） | 51（+7 新檔，0 刪除/更名） |

## §2 搬移 7 段（byte-exact，機械搬移器 var/a2/skill_split_exec.py）

| 新檔（references/） | 來源行 | bytes | sha256 |
|---|---|---|---|
| step-pitfalls-checklist.md | L670-931 | 24,026 | 71f0d7456846 |
| step-9-fda-cua-operations.md | L993-1147 | 12,036 | 3aa4a31924af |
| support-files-index.md | L1176-1327 | 15,232 | 77b6d2ec90e6 |
| step-6d-evidence-closure-pipeline.md | L507-597 | 6,233 | 43041294c347 |
| step-evidence-only-contract-a.md | L179-255 | 5,441 | a3133c854125 |
| step-10-external-provider-tool-enablement.md | L1164-1175 | 4,270 | 371f763bba82 |
| step-verify-only-lane.md | L256-308 | 3,974 | 219e7f123646 |

主檔保留：When to use / invariants / Routing decision matrix / Step 0-8 / **Step 9-0 + 9-0a 全文 inline** / 新增 `## Routing map`（When to use 之後）+ 每段 3 行指標（header 保留）。

## §3 驗證結果（T1-T6' + Canary C1-C4）

| # | 測試 | 結果 |
|---|---|---|
| T1 | skill_guard post | **PASS**（36,802 B / refs=16 / sections=26 / dangling=0） |
| T2 | 關鍵操作元素 grep 不減（跨主檔+references 全集合，含大小寫不敏感） | **PASS**（21 token 全數存在） |
| T3 | 位元組重建 diff（pointer 塞回 vs 拆分前） | **PASS（byte-identical，107,604 B == 107,604 B）** |
| T4 | references 覆蓋（delta 基準） | **PASS（0 新增孤兒；10 個既存孤兒 baseline 豁免）** |
| T5 | 外部 hooks 路徑存在（fda_guard_mint/hook、fda_preflight、fda_script_guard、screen_state_check） | **PASS** |
| T6' | guard dangling=0 且 union 提及 ≥ 23（33−10） | **PASS（40 ≥ 23，dangling=0）** |
| C1 | fresh agent: FDA 操作細節 → step-9-fda-cua-operations.md | **PASS**（經 Routing map，含 Step 9-0/9-0a inline 判定） |
| C2 | fresh agent: EVIDENCE_ONLY 閉環 → step-evidence-only-contract-a.md | **PASS** |
| C3 | fresh agent: 異常排查 → step-pitfalls-checklist.md | **PASS** |
| C4 | fresh agent: 索引查找 → support-files-index.md → taiwan-isin-venue-master.md | **PASS**（三層鏈） |

## §4 風險防護落實（拆分倒退/拆分孤兒）

- 倒退：機械搬移（零手動改寫）＋ sha256 逐檔 ＋ T3 byte-identical 重建 ＋ T2 grep 不減 ＋ guard pre/post
- 孤兒：Routing map ＋ header 保留（外部名稱引用錨點存活，含 fda-desktop-automation「Step 9-0a」、force-pause「§11」、xq-xs「Step 9/§11-15/Step 6B」）＋ T4 覆蓋 ＋ T5 hooks 絕對路徑
- 並行寫鎖：執行窗口同 session 完成；套用前 references/ 快照比對（本 WO 0 第三方衝突）

## §5 交付路徑與 hash

- 拆分後 SKILL.md: `C:\Users\user\AppData\Local\hermes\skills\software-development\hgk-governed-execution\SKILL.md`（sha 見 mirror）
- 7 個新 references 檔（同上目錄 references/，sha 見 §2）
- 拆分器: `HG-KSEOS\var\a2\skill_split_exec.py`
- 研究報告 v1/v2: `HG-KSEOS\var\a2\SKILL_SPLIT_RESEARCH_REPORT_v1.md` / `_v2.md`
- 本證據 MD 3-root mirror byte-identical

## §6 非主張

- references/ 中 10 個既存孤兒檔（含並行 session 產物）未納入索引——屬 baseline 既有狀態，非本 WO 範圍
- 拆分僅及 hgk-governed-execution skill；fda-desktop-automation 等其他 skill 未動
- FDA 防護層功能不受影響（hooks 檔案未改名/移動，T5 驗證）
