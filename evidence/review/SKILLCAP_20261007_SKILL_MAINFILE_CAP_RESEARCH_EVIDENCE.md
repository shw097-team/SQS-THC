# 建議方案：hgk-governed-execution 主檔容量治理（candidate，待你確認）

- 研究對象：`skills/software-development/hgk-governed-execution/SKILL.md`
- 研究主體 digest：`174df0185026de09c673b92d1df5b8f01dcb35cf0cf7facbbdf095b368fdf9e4`
- 量測時點：2026-10-07T02:35:34Z（subject digest 於 02:30:42Z 與 02:35:34Z 兩次讀取相同）
- Verification round 1：**FAIL**（`09_verification_round1.json`；獨立機器副本見 `transcripts/`）
- Verification round 2：**FAIL**（`11_verification_round2.json`）→ 本版為歷輪 findings 就地折入後的**現行 revision**（權威值見 `07_manifest.json` 的 `revision` 欄位；本檔此後不複述任何版本號或「最新輪次」，以免再次過期）。已執行的獨立驗證輪次見 `08_freeze_receipt.json` 的 `verification_history`
- WorkOrder：`WO-SKILLCAP-20261007-001`（writer=`hermes-native-delegated-subagents`，DEGRADED：本機無 codex CLI）

---

## 0. 先講結論（三個必要修正）

1. **「已達 100k 上限」成立，但精確講法是「餘裕 4 字元」。** 受治理口徑是 LF 正規化後的 `len()` = **99,996 / 100,000**（來源：`tools/skill_manager_tool.py:111` 的 `MAX_SKILL_CONTENT_CHARS`、`:192` 的 `len(content) > 100000`、`:488` 的 `read_text(encoding='utf-8')`）。同一檔案另有兩個會誤導人的數字：raw CRLF 字元 **101,219**、磁碟 bytes **105,116**。用後兩者量會誤判「已超限」。
2. **「無法在其中加指標」成立，但有一個零成本的繞道。** 主檔第 67、1221 行都指向 `references/support-files-index.md`；把條目加進**索引檔**不花主檔任何字元。這是止血，不是治本——因為 agent 第一個讀到的是主檔的 routing map，索引是第二跳。
3. **真正的病根不是「檔案太大」，是「沒有指定的落點」。** 2026-08-15 已做過一次機械拆分（主檔降到 36,802 chars、反向重建 byte-identical 通過），之後又長回 99,996。成長集中在**同一個節**：`## Execution-method invariants` 佔 **60,503 字元＝60.5%**，其中 **56,152 字元是上面 202 行之後逐輪疊上去的字母塊「wave lessons」**，而該節內 `###` 子標題 **0 個**、粗體獨立標題 **0 個**。也就是說：每一輪治理都把新教訓 append 進同一個扁平段落，沒有任何規則說它該落地在哪。

> 因此「另開一輪瘦身」這個方向本身是**錯的**：權威路由 `references/oversized-skill-handling-route.md` 明文把「拆分＋路由」列為首選，並**禁止直接瘦身**；2026-08-14 的手動瘦身事故造成 2 處結構破壞（`**` 殘留、換行被吃）與 4 次 skill_manage 100k-limit 失敗。

---

## 1. 可直接執行的三段式方案

### Tier 0｜零成本止血（可今天做，不動主檔一個字元）

- 在 `references/support-files-index.md` 加一條：`adversarial-verification-rounds` → 觸發條件「對凍結交付物做獨立對抗驗證輪次」→ 目標檔。
- 主檔「缺少直接指標」**登記為 carry_forward**，不假裝已解決。
- 成本：主檔 +0 字元。風險：低。可逆：只回退一個條目。
- **限制（必須揭露）**：這是第二跳可發現性。若 agent 沒讀索引，仍找不到。**不能以此宣稱容量治理完成。**

### Tier 1｜治本：把「教訓」從「不變式」裡機械分離出去（主方案）

已實測的結構軸線（唯讀，byte 級）：

| 區段 | 行號 | 字元數 | 處置 |
|---|---|---|---|
| 不變式正題（trigger 宣告 + 編號規則 1..12） | 138–201 | **4,350** | **留 inline**（這是被保護的 "Execution invariants" 本體） |
| 逐輪 wave lessons（25 個外層塊；另含未列為獨立塊的行 202–240 前置區 2,839 字元） | 202–790 | **55,387**（精確，經 round-1 查核複驗） | **byte-exact 搬入 `references/lessons-execution-waves-*.md`** |
| Routing decision matrix | 791–802 | **763**（精確） | **留 inline**（被保護元素，且它落在最後一塊 v@758 內部，必須先切邊界再搬） |

搬移後主檔預估 **約 44,000–46,000 字元**（餘裕約 54k），指標成本另計。**注意**：行 202–803 合計 56,152 字元**含**受保護的 matrix，不能當成可搬容量；排除 matrix 後的可搬容量為 **55,387**。

**機械規則（不得靠手感）**：
- 切點一律用 **`(起始行, 字元跨度)`** 從凍結副本取得，**不得**用字母標籤當鍵——實測標籤會重複（loose 規則下 a/b/c/g/i/z 各出現多次，另有 aa/bb/zb 等複合標籤），用標籤當鍵一定碰撞。
- 分段規則必須先宣告並凍結。實測同一節在不同規則下的塊數是 **42（寬鬆）/ 39（要求粗體）/ 28（三空白+粗體）/ 25（再排除巢狀子標記）**，差 17 塊。重複標籤**依規則而異，必須逐規則陳述**：A 寬鬆 a×2/b×3/c×3/g×2/i×3/z×2/aa×3；B 要求粗體 a×2/b×2/c×2/g×2/i×2/z×2/aa×3；C 三空白+粗體 a×2/b×2/c×2/g×2/z×2/aa×3；D 排除巢狀後僅 g×2/z×2/aa×3。**y 在任一規則下都只出現 1 次**。**規則不寫死，這一步就無法被獨立複驗。**
- 每塊搬走後留 **3 行指標**（section 名 / 觸發條件 / 檔路徑），並在 routing map 加一列。
- 原文 **bytes 不改寫**；losslessness 用「把 slice 塞回指標位置 → 與凍結副本 byte-identical」證明（沿用 2026-08-15 已驗證做法）。

**為什麼這是「低壓平」**：搬移是 byte-exact relocation，不摘要、不合併、不重排；正題與 matrix 這種有規範作用的層次留在原位，只有累積式證據離場。壓平風險來自「摘要/合併條款」，這個方案一次都不做。
**為什麼這是「低回歸」**：被保護的 5 個元素（When to use / Architecture+Execution invariants / Routing decision matrix / Step 9-0 與 9-0a 全文 / RP-002 status）全部留 inline；既有 36 個出站指標目標不動檔名與位置。

### Tier 2｜讓它不再長回來（沒有這層，Tier 1 做完還會回到原點）

1. **建立 lesson-landing 規則**：新增的 wave lesson 一律寫進 `references/lessons-execution-waves-<wave>.md`，不變式節只留一行指標。在 routing map 增加一列「新的治理 wave 教訓 → 載入 `references/lessons-...`」。
2. **容量預算閘**：宣告主檔天花板（建議 60,000），並提供可重跑探針；超過就 FAIL，強迫先搬移再 append。探針要用受治理口徑（LF 正規化 `len()`），並同時印出 bytes/raw 供對照。
3. **重複權威裁定**：同一組規則目前存在多處。獨立 lane 逐條比對 14 條 Rules 的結果是 **9 條至少 2 份、1 條（R4 損失分級）3 份、5 條僅 1 份**；另有 7 條 Procedure 只有獨立 skill 完整具備。**不要**按字面相似度直接刪——要用「逐條 provenance 對照 → 指定唯一權威 → 其餘降為指標」。

---

## 2. 選項矩陣（風險評分，附權威依據）

| 選項 | 壓平風險 | 回歸風險 | 可逆 | 建議 |
|---|---|---|---|---|
| A 直接手動瘦身 | **高** | **高** | 低 | **禁止**（權威路由已列為反模式；歷史事故：2 處結構破壞） |
| B 純 GUARDED SLIM（只刪冗餘） | 中 | 中 | 中 | 僅在「證明不適合拆分」後可用；需 pre/post guard + 關鍵元素 grep 不減 |
| **C 機械拆分＋routing map（Tier 1）** | **低** | **低** | **高** | **主方案** |
| D 只在既有索引＋獨立 skill 補落點（Tier 0） | 低 | 低 | 高 | **備援／立即止血**，非容量治理完成 |
| E 全面拆成多個獨立 skill | 中 | **高** | 中 | 不建議（改變載入邊界，跨 skill 具名引用風險） |
| F 針對重複規則做 SSOT 去重 | **高** | 中 | 中 | 只可作為 Tier 2 的**逐條證明後**子任務 |

---

## 3. 前置條件與驗收（可被獨立 lane 重跑）

- **G0** 本輪僅分析、唯讀；執行前另取批准（原路由前置即「Gate 2 確認方案」）。
- **G1** 凍結原始 bytes + SHA-256 + 三種量測口徑（LF 字元 / raw CRLF 字元 / bytes）+ 行數 + 標題清單 + 既存孤兒 baseline。
- **G2** 實讀 `scripts/skill_guard.py`；確認拆分器存在或建置；新檔名一律小寫+連字號（ref regex 只吃 `[a-z0-9-]+\.md`）。
- **G3** 凍結 manifest：每段起訖、原始 slice digest、目的路徑、指標文字、routing map delta、受保護段落。斷言 ranges 不重疊且 slice 完整。
- **G4** staging copy dry-run → `skill_guard pre/post`；T1–T6 全 PASS 才進真目錄。
- **G5** 反向重建 byte-identical（losslessness 的決定性證明）。
- **G6** 0 新增孤兒（不是「0 孤兒」）、routing map 與 support-files-index 一致、方向性引用逐一歸類。
- **G7** 關鍵操作元素 grep 數不減（不算入新指標）。
- **G8** fresh-context 冷啟動 canary：只給主檔，要求經 routing map 走到正確 references 檔。
- **G9** live 套用前取 spine lease 寫鎖、比對來源 digest 未漂移、原子替換後 readback。
- **G10** 容量預算閘上線（Tier 2）。
- **G11** 獨立 lane 重跑（checker ≠ maker），FAIL 原文保留。

## 4. 已知斷鏈風險（實證，非推測）

- **Step 9-0 與 Step 9-0a 有 8+ 個 references 以名稱引用**（`step-9-fda-cua-operations.md`、`support-files-index.md`、`fda-upgrade-research-2026-08-14.md`、`fda-authorization-guardrail-design.md`、`cross-session-integrity.md`、`oversized-skill-handling-route.md`、`oversized-skill-split-notes.md` 等）→ **header 不得消失**，全文本輪留 inline。
- **主檔的外部入站引用**：`HG-KSEOS/scripts/docs_gap_audit.py:60`、`Fabric/stage/RP002-STAGE-FABRIC/SELF_EVOLUTION_UPGRADE_RECEIPT.yaml:12`、`FAR canary ResearchSourceDenominator.tsv:3`、三根 review 的 `SKILL_SPLIT_FINAL_ACCEPTANCE_EVIDENCE_2026-08-15.md:51`。主檔本身不得改名。
- **最後一塊 v@758 內含 Routing decision matrix（791–802）** → 直接「搬前 N 大塊」會誤搬受保護元素，必須先切邊界重算。
- **一項待核對**：舊 split notes 稱有另一個 skill 以「Step 9-0a」名稱引用主檔；本輪在現行 skills 目錄掃描 **0 命中**，該引用現況**未經證實**，僅列為歷史記錄。

## 5. Claim ceiling（誠實邊界）

- 本輪 **未修改任何 skill 檔**；所有數字為唯讀量測。
- **LF 口徑的效力範圍**：只證明「既有檔案經 `read_text(encoding='utf-8')` 讀入 patch 時」會被正規化；`_validate_content_size` 本身只做 `len()`，**不會**對新輸入的 CRLF 自行正規化。帶 CRLF 的 payload 可能 LF 看似未超、實際仍被拒。
- 「低壓平／低回歸」是**設計評分**，不是已執行遷移的驗收結果。Tier 1 未執行。
- 已發生的控制平面副作用（經 round-1 查核修正後，全部揭露）：
- Shared Spine **6 列**：requirements 1、acceptances 1、taskspecs 1、**leases 1**、workorders 1、canonical_events 1（前版漏列 lease）。
- Kanban board `skillcap-20261007`：**凍結前（as-of 2026-10-07T02:30:42Z）= 5 卡 / 26 events / 4 comments / 3 runs / 4 links**；**查核時（as-of 2026-10-07T02:35:34Z）= 5 卡 / 35 events / 4 comments / 4 runs / 4 links**。
  - 凍結前 event kind：created 5、claimed 3、heartbeat 6、commented 4、linked 4、dependency_wait 2、claim_rejected 2。
  - 查核時**新增**事件種類：completed 3、completion_blocked_empty_result 3、promoted 1；claimed 增至 4、claim_rejected 增至 3。
  - 此處的 `promoted` 是 **Kanban 工作流**把卡片由 todo 轉 ready，**不是產品 promotion**；不可由事件名稱推論已發生 Tier 1 遷移或 release。
  - 凍結後另有事件，**不回灌**成凍結前數字。（`hermes kanban list` 的 handler 會呼叫 recompute_ready 造成寫入，查核改用唯讀 DB 查詢。）
- OpenSpec：1 change / 4 個新檔（untracked，已實測）。
- <!-- SKILLCAP-COUNTS-START (auto-managed by build_manifest.py) -->
本 run dir（as-of = manifest revision 7）**根目錄 34 檔**、`superseded/` 14 檔、`transcripts/` 9 檔 → **遞迴總數 57 檔**；bound 31、excluded_by_construction 1、post_build 2。（本區塊由 build_manifest.py 自動改寫，結構上不可能與 07_manifest.json counts 不一致；引用時仍須連 as-of revision 一起引用。）
<!-- SKILLCAP-COUNTS-END -->
- 導入 1 個 curator 建立的獨立 skill。
- 三根 `evidence/review` mirror。
- 未執行、未宣稱：canonical skill 變更、promotion、release、production、remote。
