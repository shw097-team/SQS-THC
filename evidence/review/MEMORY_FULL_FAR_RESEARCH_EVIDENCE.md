# Hermes Memory Full — FAR Research + Engineering Plan — Evidence (single MD, fully embedded)

**WO:** WO-HGK-MEM-RESEARCH-001 · **Board:** hermes-memory-far · **Generated:** 2026-08-14T04:16:22Z
**Gate 1 (FAR research):** PASS — challenge lane verdict PASS (A1..A10), DOC-11 compliance: 合理落地 (3 hard conditions)
**Gate 2 (user HITL):** PENDING — this MD is the submission; no self-approval.

## 0. Claim ceiling
- This round produced a RESEARCH + PLAN only. NO memory mutation was performed (MEMORY.md/USER.md untouched, byte-identical to session start).
- NO product code changed in HG-KSEOS / SQS-THC / Fabric (porcelain deltas: +1 evidence file per repo only, task tooling under gitignored var/).
- NO external provider enabled, NO vector DB, NO new tool install.
- HERMES_DIRECT_TRACKED_PRODUCT_WRITE = 0 (no tracked-tree product writes by Hermes; Codex write confined to gitignored var/hermes-memory-research/codex_output/).

## 1. WorkOrder / governance binding
- REQ-HGK-MEM-RESEARCH-001 FROZEN (canonical event EVT-456ae7308609fcde, version 1)
- TS-HGK-MEM-RESEARCH-001 (taskspec, writer=codex, writable_root var/a2/wt-mem-research)
- WO-HGK-MEM-RESEARCH-001 (workorder, writer=codex, base_head 22e21f0, rollback_pointer RB-WO-…)
- Router: route('memory_far_research') → NATIVE (unregistered-flow fallback); lane ≠ execution surface; Kanban+Swarm+Codex all default-on.

## 2. Artifacts (raw index, sha256 from final bytes)
| artifact | bytes | sha256 |
|---|---|---|
| M4_cross_analysis.md | 5807 | `efb78c90a4646d60680b851f2b413be94fb893bbf533d71fbe9a38bd25af9a1a` |
| M5_plan_hitl_draft.md | 5160 | `354d82e10ab1b82af9d550a712cc129b8f5a6830fcf78cbf5f852ac617686bea` |
| M8_fabric_retrieval_analysis.md | 5723 | `1721a6ceb2bfb8c540667df6304392db0586c9e81f702524c3b33a0caa2c1035` |
| codex_output/memory_research_analysis.md | 9772 | `84078a9efe42747bc41ccb12a3f7578c72f595499fe551584624bf157c8c8e31` |
| route_check.json | 1080 | `a64e46b914d418826901571e992063ad8dccca2ef932106e35082f5a5c91761c` |
| raw_notes.md | 5619 | `1fd4e5221e038df5090be9d1cfdc866624218c8e7eb4754f4fdb2da26e997648` |

## 3. KANBAN trace
```
M1 KB survey: done (25 findings + 14 principles from 8 DOC)
M2 Web survey: done (20 sources; file-as-memory consensus)
M3 Local mechanism: done (memory_char_limit 2200 config-tunable; 8 providers; CLI surfaces)
M4 Cross-analysis: done (TRI_SOURCE table; P0/P1/P2 + non-goals)
M5 Plan MD + Gate2 HITL: done (challenge findings integrated)
M6 Evidence freeze: in progress
M7 Codex primary execution: done (spawn WO writer=codex; 9772 B artifact; provider receipt)
```

## 4. SWARM trace
- Research lanes: deleg_02653a95 (3 parallel leaves: KB survey / local mechanism / web survey), started 11:32-11:38 UTC, overlap interval 11:32..11:38.
- Acceptance lanes: deleg_ebfeb0ea (2 parallel leaves: fact challenge / DOC-11 compliance), started 11:44-11:46 UTC.

## 5. CODEX trace (writer=codex, M7)
- Spawn: codex-cli 0.147.0-alpha.6.5 (sealed lane %LOCALAPPDATA%\HG-KSEOS\runtime\), isolated CODEX_HOME/OPENCODEX_HOME, credential from canonical hermes .env.
- Command: --model deepseek-v4-flash --cd C:\Projects\Agent_Workspace exec --skip-git-repo-check --ephemeral --sandbox danger-full-access -c approval_policy=never --json <prompt>
- Provider receipt (usage.jsonl): input_tokens=32720, cached_input_tokens=31488, output_tokens=10884, reasoning_output_tokens=8175; WS 426 → HTTP fallback (recorded defect-class note OPENCODEX-WS-426-001).
- Output: var/hermes-memory-research/codex_output/memory_research_analysis.md (9,772 B, sha in §2).

## 6. Challenge lane (fresh context, independent) — full verdict
### Lane A (fact verification) — CHALLENGE_VERDICT=PASS
```
All verification complete. The KB governance layer (知識庫\HG-KSEOS_SSOT) exists with the six-class/four-gates concepts the research cites — traceable foundation confirmed. Every Hermes mechanism fact checked out. Final report:

---

## CHALLENGE_VERDICT=PASS

### A1..A10 驗證表

| # | 檢查項 | 判定 | 依據 |
|---|--------|------|------|
| A1 | config.yaml memory 段：`memory_char_limit=2200`、`user_char_limit=1375`、`memory_enabled=true` | **PASS** | config.yaml L114-119 逐字確認：`memory_enabled: true`、`memory_char_limit: 2200`、`user_char_limit: 1375`、`flush_min_turns: 6`、`nudge_interval: 10` |
| A2 | `flush_min_turns` 原始碼零引用（dead config 宣稱） | **PASS** | 全樹 grep `flush_min_turns` 僅 1 命中：`cli-config.yaml.example:734`（註解範例檔）。**零 .py 引用**，dead key 宣稱屬實 |
| A3 | memory_tool.py docstring：§ 分隔、frozen snapshot、無自動壓縮 | **PASS** | L16「Entry delimiter: §」；L11-14「frozen snapshot at session start…preserves prefix cache」；L26-34 docs 明示「does **not** auto-compact」；add 溢出路徑（L428-440）只回錯誤+要求同回合 consolidate，無靜默壓縮 |
| A4 | `apply_batch` 存在 + 單回合 3 次 consolidation 保險絲 | **PASS** | `apply_batch` @ L562（all-or-nothing、final-budget 驗證、idempotent add）；`_MAX_CONSOLIDATION_FAILURES_PER_TURN = 3` @ L163，註解引 issue #42405；`reset_consolidation_failures()` @ L176 |
| A5 | 官方文件確認「memory 不自動壓縮」 | **PASS** | 雙重驗證：(1) 倉內 docs 源 `website/docs/user-guide/features/memory.md` L27「Memory does **not** auto-compact: …returns an error instead of silently dropping entries」+「What Happens When Memory is Full」章節 (L134-153)；(2) 線上頁 curl 200 OK 且含 "auto-compact" 字樣 |
| A6 | MEMORY.md/USER.md 用量數字（2101/2200=95%、340/1375=24%） | **PASS** | 實際讀檔計算：MEMORY.md **恰 2101 chars**、USER.md **恰 340 chars**（含換行，與工具計法一致）；16 個條目（15 個 `§` 分隔行，與研究「16 entries」相符） |
| A7 | 研究文件 (a) 無根據宣稱檢查 | **PASS** | 逐項核對：fuse #42405 ✓（源碼註解）、drift guard #26045 ✓（`_drift_error` L110 引 issue）、`hermes memory setup/status` CLI ✓（`hermes_cli/memory_setup.py`）、session_search FTS5 免費無限 ✓（docs L204-206）、8 個 provider 存在 ✓（docs L350）。唯一瑕疵見 FINDING-01/02 |
| A8 | 研究文件 (b) 結論與事實一致性 | **PASS** | P0「就地整理+修剪、不啟用 provider、不裝向量庫、不改產品碼、上限僅微調」與全部已驗證機制一致；「>80% 先 consolidate」為 docs 明示最佳實踐（L153）；`memory_char_limit` 確實 config 可調（`agent_init.py:1717` 讀取） |
| A9 | 研究文件 (c) 過度工程化檢查 | **PASS** | 無向量庫/新工具建議；P2 provider 啟用明確標為「NOT now」；非目標段明列「NO vector DB, NO new tool install, NO product code change」。社群檔案記憶論點（Anthropic/OpenAI/AGENTS.md）與 docs 設計相符 |
| A10 | P0 修剪建議 vs Hermes 記憶體機制相容性 | **PASS** | substring replace 語義 ✓（唯一 substring 匹配、多重匹配報錯——apply_batch 為官方全量路徑）；drift guard ✓（`\n§\n` 分隔、`ENTRY_DELIMITER` @L67；手動編輯後 replace/remove/apply_batch 會拒寫並存 `.bak`，drift 錯誤訊息本身即指示「rewrite as clean §-delimited list then retry」→ 手動修剪只要維持乾淨 § 格式即相容）；刪除 dead `flush_min_turns` ✓ 無副作用。見 FINDING-03 操作注意 |

### Findings

- **FINDING-01（低）** provider 數量少報：研究宣稱「7 external providers」，實際 repo/docs 為 **8**（漏列 supermemory；`website/docs/.../memory.md` L350、`CONTRIBUTING.md` L72 皆列 8）。不影響任何結論。
- **FINDING-02（低）** 「prefer session_search / skill / external provider over raising the limit」被表述為官方指引；docs 逐字僅支持「Character limits keep memory focused」+「>80% consolidate」，該優先排序是研究者綜合（精神一致但歸因略強於來源）。
- **FINDING-03（低）** P0 執行操作細節未明示：手動編輯 MEMORY.md 後 (a) 須維持乾淨 `\n§\n` 分隔格式（條目內含「§」可容忍——parser 以 L67 的 `\n§\n` 切分，非裸 `§`）；(b) frozen snapshot 使編輯要到**下一 session** 才生效——計畫應註明「編輯→新 session 才驗收效果」。非違規，僅操作性備註。

### 總結
- **做了什麼**：獨立查證 config.yaml、memory_tool.py 源碼（docstring/apply_batch/fuse/drift guard/parser）、官方 docs（倉內源+線上 curl）、MEMORY.md/USER.md 實際字數與條目數、`hermes memory` CLI 與 provider 清單、KB DOC-11 存在性。
- **結論**：研究者所有關鍵事實宣稱（95% 用量、無自動壓縮、3 次保險絲 #42405、drift guard #26045、apply_batch、dead `flush_min_turns`、config 可調上限、docs 指引）**全部屬實**；P0 就地修剪方案與機制相容、無過度工程化。3 個低嚴重度瑕疵均不影響結論 → **PASS**。
- **檔案**：未建立/修改任何檔案（唯讀驗證）；下載暫存 `C:/Users/user/AppData/Local/Temp/hermes_mem_docs.html`（可刪）。
- **問題**：無阻礙性問題；KB DOC-11 內部 taxonomy（四閘門/六類）僅做到「文件存在且概念可追溯」，未深度審計其內部內容（超出本任務核心範圍）。
```

### Lane B (DOC-11 governance compliance) — overall: 合理落地
```
驗證完成。所有關鍵概念均在 DOC-11 原文中找到明確依據。以下是合規報告。

## 合規檢查結論摘要

**驗證結果：研究者引用的 7 項治理原則全部真實存在於 DOC-11**（promotion / supersession / retention finite / withdrawal / context budget / memory 非 truth / state 屬 WorkOrder），均有原文段落支持，無虛構引用。**P0 修剪計畫整體符合 DOC-11 治理精神**，但必須以 WithdrawalEvent + readback 流程執行、保留 provenance、並將狀態落地至 WorkOrder 等 canonical artifact，才能完全合規。

```json
{
  "doc11_quotes": [
    {
      "concept": "memory 不是 truth（核心命題）",
      "line": 26,
      "quote": "r1 已成立的核心命題——Memory 是 scoped、temporal、revocable、evidence-bearing candidate state，而不是 canonical truth——完整保留"
    },
    {
      "concept": "retention 必須 finite",
      "line": 348,
      "quote": "基本規則：第一，scope 採最小可用範圍；第二，tenant 隔離預設 deny；第三，sensitivity 提升會提高 permission tier；第四，retention 必須 finite 或有合法 hold；第五，consent 必須可撤回；第六，revocation 必須觸發 propagation；第七，break-glass 不能擴張成永久權限。"
    },
    {
      "concept": "state 屬於 WorkOrder（canonical boundary）",
      "line": 152,
      "quote": "Canonical truth 只能存在於 Authority、SourceCapsule、ArtifactContract、CanonicalEvent、WorkOrder、approved documentation、verified tests 與 ReleaseEnvelope 等受治理 artifact 中。Memory 可以記錄「曾發生」「曾偏好」「曾成功」「曾失敗」「可能可重用」，但不能宣稱「這就是系統規範」。"
    },
    {
      "concept": "暫態工作狀態（working memory）不持久化",
      "line": 177,
      "quote": "|Working Memory|單次任務或短 session 內的暫態工作狀態。|task/session|短；預設不持久化|任務結束後清除或轉 candidate|不可跨 workspace 自動共享；不可被引用為 truth。|"
    },
    {
      "concept": "working memory 任務結束不得自動持久化",
      "line": 185,
      "quote": "Working memory 預設只在單次任務內存在。它可協助 decomposing、temporary planning、tool result holding，但任務結束後不得自動持久化。"
    },
    {
      "concept": "procedural memory → skill candidate 需 owner gate",
      "line": 154,
      "quote": "Procedural memory 可提出 skill candidate，但 Skill 的 schema、測試、MCP/tool 安全、version lifecycle 必須由 DOC-13/F07/F12 控制。"
    },
    {
      "concept": "promotion 是高風險路徑、需指定 target owner",
      "line": 425,
      "quote": "Promotion 是 memory governance 的高風險路徑。Memory 經常被召回或多次出現，不代表它真實、穩定、可共享或可執行。Promotion 必須指定 target：SourceCapsule、ArtifactContract、SkillMemoryManifest、KnowledgeObject、KG edge candidate 或 Controlled Evolution candidate；每種 target 都有不同 owner 和 admission criteria。"
    },
    {
      "concept": "context budget（recall gate 最後一關）",
      "line": 400,
      "quote": "Recall 不是「找最像的記憶」。它是一個 gated decision：先過 permission/scope，再過 taint/security，再檢查 freshness/retention，再處理 conflict/supersession，再計算 relevance，最後才交給 DOC-10 context budget。若任一必要條件不明，正確行為是 abstain 或返回 TT，而不是把記憶塞進 prompt。"
    },
    {
      "concept": "withdrawal 必須 propagated readback",
      "line": 274,
      "quote": "Withdraw/delete 階段必須 propagated readback；只刪 markdown 而未重建 vector index 不合格。"
    },
    {
      "concept": "supersession（conflict/supersession review）",
      "line": 165,
      "quote": "當 memory 與 canonical artifact 衝突時，canonical artifact 優先；memory 進入 conflict/supersession review。"
    },
    {
      "concept": "finite lifecycle：deletion 是正常終態",
      "line": 4877,
      "quote": "The lifecycle is a finite state machine with stop conditions: ... Deletion, demotion and abstention are normal terminal or transitional outcomes. ... Without explicit stale, conflict, withdrawal and compensation paths, every interaction increases hidden state and incident cost. A finite lifecycle converts \"learning\" into reversible operations."
    }
  ],
  "p0_compliance": [
    {
      "action": "狀態快照（hash/cron id/進行中專案）移出記憶體",
      "verdict": "符合",
      "reason": "DOC-11 明確定義 Working Memory 為「單次任務或短 session 內的暫態工作狀態」，scope 為 task/session、預設不持久化、任務結束後清除或轉 candidate（L177/L185）；且 canonical truth/authoritative state 的歸屬是 WorkOrder 等受治理 artifact（L152），memory 不得宣稱「這就是系統規範」。把 cron id、hash、進行中專案等暫態執行狀態從長期記憶移出，正是將 state 歸位到 WorkOrder 的正確動作，符合 memory-not-truth 與 finite lifecycle 精神。前提條件：移出必須以 WithdrawalEvent 執行並完成 index rebuild 與 readback 驗證（L274/L379），且狀態須落地至 WorkOrder/canonical artifact 而非無痕消失。"
    },
    {
      "action": "程序性內容已入 skill，故從記憶體移除（去重）",
      "verdict": "符合",
      "reason": "DOC-11 的 promotion gate 管轄的是「procedural memory → skill candidate」的升格路徑（L154/L425/L431），其 owner gate（F07/F12）僅在『建立/安裝新 skill』時觸發。skill 早已建置完成時，記憶體中殘留的只是重複 pointer/hint，移除重複項屬 retention 清理而非 promotion，無需重新走 promotion gate；研究者的論點成立。條件：① 僅刪除與既有 skill 完全重疊的內容，並保留指向 SkillMemoryManifest 的 provenance ref（L180「可 route 到 SkillMemoryManifest 或 skill candidate」）；② 不得觸碰 skill 本體——DOC-11 明載「不安裝 skill、不改 MCP tool schema」（L520）；③ 若記憶內容超出既有 skill 涵蓋範圍，應保留或提出新 skill candidate 而非刪除；④ 仍須走 withdrawal/readback 流程。"
    },
    {
      "action": "以記憶體 95% 滿為由的整體 P0 修剪",
      "verdict": "部分符合",
      "reason": "方向正確：DOC-11 明定「retention 必須 finite 或有合法 hold」（L348）、finite lifecycle 以 deletion/demotion/abstention 為正常終態（L4877），並警告「只優化累積的 memory 系統會增加 hidden state 與 incident cost」（L4879），容量壓力下的修剪正是治理預期的操作。但僅以容量為觸發理由不足——DOC-11 要求修剪依據是 retention policy、expiry、supersession/conflict 與 withdrawal（L139/L400），且刪除須留 tombstone、走 audit trail、propagated readback（L274/L373）。若計畫只是『容量到了就刪』而不對照 retention/expiry 政策、不驗證 readback，則降為不符合；若按 policy + 證據流程執行則符合。另注意：DOC-11 禁止的是「頻率→自動 promotion」（L522），不禁止「policy→deletion」，低頻或重複正是合法刪除理由。"
    }
  ],
  "overall": "該 P0 記憶體修剪計畫是 DOC-11 治理精神的合理落地，非越權行為。驗證結論：(1) 研究者引用的七項治理原則——promotion（L61/L425）、supersession（L139/L165）、retention 必須 finite（L348）、withdrawal（L274/L461）、context budget（L61/L400/L417）、memory 不是 truth（L26/L59/L97/L152）、state 屬於 WorkOrder（L152）——全部真實存在於 DOC-11 原文，無捏造；(2) P0 兩大核心動作（暫態狀態移出記憶體、既有 skill 的重複程序記憶去重）在概念上與 DOC-11 的 working-memory 不持久化、memory-as-candidate-state、promotion gate 只管升格不管去重等原則一致；(3) 合規落地的三個硬條件：a) 所有移除動作須以 MemoryWithdrawalEvent 執行並完成 index rebuild + readback 驗證（L274/L379），禁止裸刪 markdown；b) 被移出的狀態必須落地到 WorkOrder 等 canonical artifact，程序記憶去重須保留 SkillMemoryManifest provenance ref；c) 修剪須以 retention/expiry/supersession policy 為裁決依據，並全程保留 audit trail 與 tombstone。滿足以上條件即為 DOC-11 精神的忠實實作；若跳過 withdrawal/readback 或無痕刪除，則違反 DOC-11 的 delete-propagation 契約，需修正後方可執行。"
}
```

---

**交付摘要：**
- **做了什麼**：在知識庫定位 DOC-11（`Hermes_Agent_OS_專業技術文檔_DOC-11_2026-07-16_r2.md`，5340 行），以 13 次搜尋 + 5 段精讀，逐項驗證研究者引用的 7 項治理原則，並對 P0 兩大修剪動作 + 整體修剪流程做合規判定。
- **發現**：7 項原則全部在 DOC-11 有原文依據（11 條引文含行號）；P0 動作 1（狀態快照移出）與動作 2（skill 去重）均判「符合」，整體修剪判「部分符合」（方向對、須補 retention-policy 依據與 withdrawal/readback 流程）；整體結論：合理落地，但有 3 個硬性合規條件。
- **未建立/修改任何檔案**；未遭遇阻礙。
```

## 7. Key research conclusions (condensed)
1. 95% full is a designed-for state (no auto-compact; error + same-turn consolidate, fuse 3/turn #42405).
2. Limit config-tunable (memory_char_limit 2200) but official guidance: keep focused; >80% consolidate first.
3. DOC-11 governance: memory ≠ truth; finite retention; state → WorkOrder; procedures → skills (owner gate at install only, dedup ≠ promotion).
4. Community 2026-05..08: file-as-memory is standard; 2200-char + §-delim = manual context compaction per Anthropic; vector DBs over-engineered here; 8 external providers available as future one-command option.
5. P0: classify → prune state snapshots + skill dupes + compact env facts (target ~1100-1300, <80%) with backup + withdrawal/readback + next-session verification.
6. Non-goals: no vector DB, no provider enable, no product code, no auto-compaction implementation.
7. **M8 (user-challenge response): FABRIC ALREADY has a cross-session memory retrieval layer** — spine knowledge_fts (354 docs, FTS5, HGK-PROVIDER-FTS5 ENABLED/PREFERRED_DEFAULT), KnowledgeFactory API (search/remember/revoke/verify_citation), FAR tri-source retrieval (far_retrieval.py: KB scan + spine MATCH + memory rows), 知識庫 9,706 md, session_search 138 MB. User claim CONFIRMED → "need retrieval" is NOT a provider-trigger anymore; the ONLY unmet gap is embedding concept-similarity (semantic) retrieval, unproven needed. Strengthens the no-provider conclusion: FABRIC built its own local/auditable/governed retrieval layer; external providers' only edge (embedding) is out-of-scope and governance-negative (DOC-12 black-box similarity).

## 8. Gate 2 — user decisions requested
1. Approve P0 memory consolidation+prune execution (entry-by-entry removal list will be presented)?
2. Approve P1 removal of dead config key flush_min_turns (evidence-only)?
3. Keep memory_char_limit at 2200 (recommended)?
4. (M8) Acknowledge FABRIC-infra retrieval finding: P2 provider-trigger reworded to embedding-semantic-only; no provider enablement this round.

## 9. Non-claims / STOP
- STOP: awaiting user HITL on §8. Do NOT self-approve Gate 2.
- External meta acceptance: not claimed. Production/live: not claimed.
