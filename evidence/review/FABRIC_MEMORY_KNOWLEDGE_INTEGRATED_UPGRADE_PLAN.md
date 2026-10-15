# FABRIC MEMORY & KNOWLEDGE INFRASTRUCTURE — INTEGRATED UPGRADE PLAN
**External Review Package · Single Self-Contained Document · v1.0**

- **Generated:** 2026-08-14T05:32:20Z (UTC)
- **Governance:** HG-KSEOS as sole control plane; Hermes as governed Runtime/Orchestration Plane
- **WorkOrders:** WO-HGK-MEM-RESEARCH-001 (memory-full research) + WO-HGK-KBUPGRADE-RESEARCH-001 (KB/memory/KG shared-infrastructure upgrade research)
- **Boards:** hermes-memory-far + fabric-kb-upgrade-far (K1..K8, M1..M8 — all done)
- **Status:** Gate 1 (FAR research) = **PASS** (2 challenge lanes, both CHALLENGE_VERDICT=PASS); Gate 2 = **PENDING user HITL** (not self-approved)
- **Claim ceiling:** This document consolidates RESEARCH + PLAN only. NO migration, NO schema change, NO memory mutation, NO provider enablement was executed. Production/live/remote NOT claimed.

---

## 0. HOW TO READ THIS DOCUMENT
This single file is the complete external-review package. Every blocking claim is backed by
raw embedded bodies (§5-§10) rather than file paths — the reviewer environment cannot open
local paths or MEDIA attachments. Artifact digests are in §11 for byte-level verification.
All timestamps UTC. No claim in this document exceeds the evidence embedded herein.

---

## 1. EXECUTIVE SUMMARY

### 1.1 The problem (two linked findings)
1. **Hermes persistent memory is 95% full** (MEMORY.md 2,101/2,200 chars). Hermes memory
   does NOT auto-compact by design (official docs + source): an over-limit write errors, and
   the agent must free space in the same turn (max 3 consolidation failures/turn, issue #42405).
   The limit is config-tunable (`memory.memory_char_limit`), but official guidance is to keep
   memory focused and consolidate above 80% before adding.
2. **FABRIC knowledge infrastructure is fragmented**: HGK SharedSpine holds a complete but
   underused knowledge/memory/KG facility (KnowledgeFactory + 8 tables + FTS5, 354 docs,
   `HGK-PROVIDER-FTS5` ENABLED/PREFERRED_DEFAULT), while the FABRIC knowledge base holds
   9,698 md files that are NOT indexed into it; FAR re-implements retrieval against the same
   spine DB (duplicate code path); and the KG tables are empty (0 rows). Governance slots for
   a FABRIC-level shared knowledge service were PRE-RESERVED (KNOWLEDGE_POLICY `shared.*`
   namespace, KG1 gate, HGK_STACK_MANIFEST `knowledge_fts` service, `hgk-knowledge-factory`
   profile) — the missing piece is a runtime owner and a unified pipeline.

### 1.2 The user proposal (evaluated)
> Extract HGK's memory/knowledge/KG facilities, upgrade them into a FABRIC-level shared
> infrastructure (Shared Infrastructure Profile Team), integrate with FABRIC's existing KB,
> manage it under a PROFILE, governed by FABRIC, serving HGK/SQS/FAR/FDA cross-session sharing.

**Verdict: architecturally sound and consistent with FABRIC's original design intent —**
feasible ONLY as a *shared capability substrate* (SHARED_INFRASTRUCTURE_PROFILE_TEAM,
heavy_stack=false, `fabric.*` candidate-only namespace). NOT as a knowledge-truth transfer.
Extraction is a constitutional change requiring human two-key approval.

### 1.3 The plan at a glance
```
P0  (immediate, zero-infrastructure)  Hermes memory consolidation+prune 2,101 → ~1,100-1,300 chars
Stage 1 (immediate, zero-new-infra)   Repair stale FTS index (re-ingest from 知識庫 canonical roots);
                                      converge retrieval on KnowledgeFactory (retire FAR duplicate);
                                      keep hgk-knowledge-factory profile as operating identity
Stage 2 (governance formalization)    Land SHARED_INFRASTRUCTURE_PROFILE_TEAM per FDA/FAR precedent
                                      (WO→CAPC→canary→dual-lane acceptance→freeze; additive manifest)
Stage 3 (conditional, LAST)           KG/graph shared service ONLY after proven cross-member
                                      consistency need + DOC-12 edge admission + tenant isolation +
                                      audit; disambiguate kg_edges vs evidence_graph.py (EVO-005);
                                      Qdrant/Neo4j/pgvector stay default-off
```
**Non-goals (anti-over-engineering):** no second knowledge platform; no standalone memory
server; no vector DB; no KG enablement this round; no truth transfer out of domain owners;
no rewrite of the Hermes memory system (2200-char MEMORY.md stays the hot pointer cache).

---

## 2. GOVERNANCE & DECISION BOUNDARIES

### 2.1 Three bottom lines (violating any = DOC-01 hard invariants breach + AGENTS.md "no knowledge platform substitution")
| # | Invariant | Source |
|---|---|---|
| BL-1 | `domain_owner_retains_truth_authority: true` | Fabric\control\KNOWLEDGE_POLICY.yaml L27 |
| BL-2 | `cross_namespace_write_default: DENY` | KNOWLEDGE_POLICY.yaml L25 |
| BL-3 | `fabric_can_mutate_truth: false` | Fabric AUTHORITY_MATRIX (verified by governance lane) |

### 2.2 Governance principles applied (verified against Hermes_Agent_OS DOC-01/02/08/11/12/13/20)
- Canonical knowledge = source-backed approved artifact; Memory = scoped/temporal candidate state;
  RAG = retrieval; KG = rebuildable derived view — **none owns truth** (DOC-01 #4, DOC-02).
- Memory four gates: capture → object → recall → promotion; no self-promotion;
  cross-tenant memory injection = poisoning incident (DOC-11).
- Grounded retrieval = governed derived-view layer, 7-gate admission pipeline (DOC-12 §6);
  KG edge admission: schema-first, per-edge direct evidence locator + checker + effective
  interval, inferred vs source edges layered, high-risk edge needs 2 sources or human approval.
- CH-20 candidate-first invariant: candidates never direct-write, never self-approve,
  never become canonical truth without owner gate (DOC-20).
- taint-as-DATA: source text/memory/RAG/KG hits are DATA until sanitized+adopted (DOC-08).
- Published trust is time-bounded; descriptor/behavior change → re-certification (DOC-13).
- AssetHealthRecord multi-dimensional (freshness/correctness/safety/usage/dependency_impact),
  never collapsed to one score (DOC-20 ART-20-02).

### 2.3 SoD matrix
| Role | Responsibility | Boundary |
|---|---|---|
| HGK (governance plane) | WorkOrder existence/owner/acceptance; `hgk.approved.*` truth authority | truth authority not delegable; constitutional change = two-key human |
| FABRIC substrate (new profile team) | Shared infrastructure ops: index pipeline, retrieval API, admission gates, health records | `fabric.*` candidate-only; no self-accept/self-promote; no CREATE_WORKORDER; no second knowledge platform |
| Domain owners (SQS/FAR/FDA) | Own their knowledge content as products; consume shared substrate | writes confined to own namespace; SQS stays stage2-read-only |
| Hermes | Orchestration/kanban/dispatch; memory_records lifecycle; external provider adapter (one active) | derived memory only; cannot replace canonical knowledge |
| Oracle / AO | Independent acceptance (VERIFY_ONLY) + external review | MISSING_TOOL_ROW=FAIL_CLOSED; popularity cannot override gates |

---

## 3. CURRENT-STATE INVENTORY (verified, 2026-08-14)

| Asset | Location | Scale | Status |
|---|---|---|---|
| KnowledgeFactory API | HG-KSEOS\src\hg_kseos\knowledge.py | 10 public methods (ingest/promote/search/rebuild/add_kg_assertion/verify_citation/withdraw_source/remember/active_memory/revoke_memory) | Qualified: RAG_KB_RUNTIME_ACCEPTANCE 14/14 checks PASS (depth L3+L4, backend SQLite FTS5, p0=lexical/FTS-first, vector DEFERRED_SOURCE_BACKED) |
| Spine KB/Memory/KG tables | HG-KSEOS\var\shared-spine\hg-kseos.db (794 MB) | knowledge_docs 354 / knowledge_fts 354 (FTS5) / memory_records 1 / kg_edges 0 / kg_assertions 0 / sources 351 / candidates 376 | **DATA DEBT: sources 351/351 canonical_paths DEAD** (point to deleted SQS-THC\SSOT + 技術資料庫); FTS is a stale snapshot |
| FABRIC knowledge base | C:\Projects\Agent_Workspace\知識庫\ | 9,698 md (12 roots: 工程基座 5,916 / ASCE-WebX 1,328 / GENIE 808 / TCA-10X 449 / HG-KSEOS資料庫 323 / SQS-THC&TW-ICT_SSOT 192 / 專業技術文檔 169 / 實作相關DOC 157 / SQS-THC資料庫 139 / 教程字幕 128 / HG-KSEOS_SSOT 86 / Obsidian投影 3) | Live, growing; NOT indexed into spine FTS (coverage gap) |
| FAR tri-source retrieval | Fabric\fabric-autonomous-research\far_retrieval.py | 549 lines; KB scan + spine FTS MATCH + arXiv; qualified (103 tests) | **DUPLICATE**: retrieve_memory() re-implements spine FTS directly (bypasses KnowledgeFactory) |
| Governance slots | Fabric\control\KNOWLEDGE_POLICY.yaml; Fabric\stage\RP002-STAGE-FABRIC\A0_KNOWLEDGE_EXTENSION_EVIDENCE.yaml; Fabric\stage\RP002-STAGE-HGK\KG1\KG1_NAMESPACE_MODEL.json; Fabric\HGK_STACK_MANIFEST.yaml | shared.* namespace; KG1 gate; knowledge_fts service; 8 profiles incl. hgk-knowledge-factory | PRE-RESERVED — missing runtime owner + unified pipeline |
| Profile team precedents | Fabric\fabric-desktop-automation (FDA); fabric-autonomous-research (FAR) | TEAM.md + governance/ + evidence/ + receipts/ + capability matrix + execution binding | SHARED_INFRASTRUCTURE_PROFILE_TEAM pattern established; RP002_PROFILE_TEAM_MANIFEST additive |

---

## 4. THE INTEGRATED UPGRADE PLAN

### P0 — Hermes memory consolidation (immediate; zero infrastructure; needs user approval)
1. Backup MEMORY.md/USER.md raw bytes (rollback point).
2. Classify all 16 entries per DOC-11 six-class taxonomy + Operator five-questions.
3. Prune: state snapshots (hashes/cron ids/in-flight projects → belong to WorkOrder/evidence,
   not memory); skill duplicates (pointers to existing skills); compact env facts.
4. Execute via memory tool replace/remove/apply_batch (NOT manual edit, avoiding drift guard);
   record WithdrawalEvents; verify next-session effectiveness (frozen snapshot semantics).
5. Target: 2,101 → ~1,100-1,300 chars (<80%). Keep memory_char_limit at 2200 (recommended).

### Stage 1 — Shared data layer consolidation (immediate; zero new infrastructure)
1. Re-ingest 知識庫\HG-KSEOS_SSOT + 知識庫\SQS-THC & TW-ICT_FSDT-Stack_SSOT as canonical roots
   into spine FTS (repairs the 351/351 dead-source debt; ERR_SOURCE_DRIFT guard becomes operable).
2. Converge retrieval: FAR retrieve_memory() → call KnowledgeFactory.search (one API, one code path).
3. Keep `hgk-knowledge-factory` profile as the operating identity (role-level distillation executor).
4. NO new platform, NO new DB, NO KG enablement.
5. Acceptance: RAG_KB_RUNTIME_ACCEPTANCE re-run on re-ingested index (same 14 checks + fresh
   denominator); FAR test suite re-run.

### Stage 2 — Governance formalization (profile team)
1. Land `fabric-knowledge-infrastructure` (name TBD) as SHARED_INFRASTRUCTURE_PROFILE_TEAM:
   TEAM.md + governance/ + evidence/ + receipts/ + capability matrix + execution binding.
2. Pipeline per FDA/FAR precedent: WO admission → CAPC → canary → dual-lane acceptance
   (internal AO VERIFY_ONLY + external) → freeze; RP002_PROFILE_TEAM_MANIFEST additive, no fork.
3. Scope: shared capability substrate (index pipeline, retrieval API, admission gates,
   AssetHealthRecord); `fabric.*` candidate-only namespace.
4. KNOWLEDGE_POLICY updated additively (new namespace rows, no rewrites of accepted rows).
5. Constitutional two-key human approval required (owner gate: F01 + Human Policy Owner).

### Stage 3 — KG/graph (CONDITIONAL, LAST — NOT this round)
1. Trigger ONLY when: cross-member consistency retrieval need is PROVEN, AND DOC-12 edge
   admission (schema-first, per-edge evidence locator + checker + effective interval,
   high-risk dual-source) + tenant isolation + audit are all in place.
2. Disambiguate kg_edges/kg_assertions vs evidence_graph.py (EVO-005) — ONE graph facility.
3. Qdrant/Neo4j/pgvector stay default-off; any enablement = separate qualification event
   (MISSING_TOOL_ROW=FAIL_CLOSED).

---

## 5. EMBEDDED EVIDENCE — MEMORY-FULL RESEARCH (WO-HGK-MEM-RESEARCH-001)

### 5.1 Cross-analysis (M4) — verbatim
# M4 — Cross-Analysis: Hermes Memory Full (95%) — Engineering Assessment

Generated: 2026-08-14 (UTC). WO-HGK-MEM-RESEARCH-001. Board hermes-memory-far.

## 1. Situation
- MEMORY.md = 2,101/2,200 chars (95%). USER.md = 340/1,375 (24%).
- Memory does NOT auto-compact (official docs + source): overflow → tool error → model
  must consolidate same-turn (max 3 failures/turn fuse, issue #42405).
- This is a *known, designed-for* state: docs explicitly cover "What Happens When Memory is Full".

## 2. What the three research lanes established (TRI_SOURCE)

### Lane A — KB (Hermes_Agent_OS 專業技術文檔, DOC-11 core)
- Memory is NOT truth; four gates (capture/object/recall/promotion); six-class taxonomy;
  retention must be finite; supersession preserves lineage; withdrawal is multi-layer
  propagation; compaction must be readable-back/rollback-able (DOC-10 §9);
  promotion to Skill/KB requires owner gate, no self-promotion, anti-loop.

### Lane B — Local Hermes mechanism (source code + official docs)
- Native capabilities: dual-file (MEMORY.md/USER.md), §-delimited, frozen snapshot,
  drift guard, injection scan, write-approval gate, nudge + background review loop,
  session_search (FTS5, unlimited, free), `hermes memory` CLI, `hermes journey`,
  7 external providers (mem0/honcho/openviking/hindsight/holographic/retaindb/byterover).
- Limit IS config-tunable: `memory.memory_char_limit` (config.yaml, default 2200).
- Official full-load path = in-turn consolidation via replace/remove/apply_batch;
  `apply_batch` is the preferred atomic path (remove/make-room + add in ONE call).
- Official docs: "Character limits keep memory focused"; >80% → consolidate first;
  prefer session_search / skill / external provider over raising the limit.
- `flush_min_turns: 6` in local config.yaml is an UNREFERENCED stale key (dead config).

### Lane C — Web/community (2026-05..08 hot landscape)
- FILE-AS-MEMORY is the industry de facto standard (Anthropic memory tool/CLAUDE.md,
  OpenAI project memory, AGENTS.md ecosystem, akitaonrails/ai-memory, Hermes itself).
- Anthropic effective-context-engineering: context is finite; compaction/summarization/
  retrieval, not unbounded windows. Hermes 2200-char + §-delim + periodic tidy =
  manual context compaction — aligned with official best practice.
- Vector DB / heavy frameworks (mem0/Graphiti/Cognee/Letta) = over-engineering for this
  design; even heavy players moved to token economy (mem0 v3 single-pass ADD-only).
- Hermes community expectations: pluggable providers (Honcho/supermemory already
  integrated) + local-first zero-dep file memory (#85418); NO pressure to swap to vector.
- Hot 3-month: claude-mem (90.7k★), mem0 v3 (63k★), memory-os for Hermes (1.3k★),
  akitaonrails/ai-memory (1.5k★), OpenViking (28k★, trend only).

## 3. Cross-comparison → engineering conclusions

| Question | KB answer (DOC-11) | Hermes native | Community | Verdict |
|---|---|---|---|---|
| Is full-memory an emergency? | No — finite retention is by design | Designed-for state | Normal ops | **No new infra** |
| Primary fix? | Classify → freshness review → supersede/withdraw | In-turn consolidate via apply_batch; >80% tidy | Compaction discipline | **Consolidate + prune (evidence-only, no product code)** |
| Raise limit? | retention finite; budget is a gate | Config-tunable but "limits keep memory focused" | Token economy | **Only modest bump if needed after prune (2200→2600 max), not primary** |
| External provider? | External frameworks = QUARANTINE_UNTIL_REPROBE; tool enablement separate local contract | 7 installed, 0 active | Pluggable is the norm; none needed now | **Do NOT enable now; document as future option** |
| Where do state snapshots go? | State belongs to WorkOrder/evidence, not memory | session_search + kanban + evidence MDs | — | **Move status/hash entries OUT of memory** |
| Procedures/rules in memory? | Procedural → Skill candidate via owner gate | skills dir + curator | Skills are the mechanism | **Already in skills — remove duplicates from memory** |
| Hot tool integration? | — | — | Don't reinvent; adopt discipline patterns | **No new tool install; adopt claude-mem/ai-memory discipline** |

## 4. Recommended plan (evidence-only, no product code, no over-engineering)

**P0 — Immediate consolidation (this session, with user HITL approval — Gate 2):**
1. Classify all 16 MEMORY entries (DOC-11 six-class taxonomy) + apply Operator five-questions.
2. PRUNE: state snapshots (RP-002 status, FDA/FAR hashes, cron ids, DoD-17, MATT
   pending) → move to evidence/kanban/session_search (they are queryable; memory
   holds pointers not copies). Est. reclaim ~45-50%.
3. MERGE: duplicated skill content (強制規則→hgk §15/§6A; 4-failures→skill;
   Gate→Step 10A) → replace with one-line pointer. 
4. COMPACT: env/tool facts → single high-density entries.
5. Target: 2,101 → ~1,100-1,300 chars (~50% headroom).
6. USER.md: 340/1,375 — fine, optionally add contract-format expectation if not already.

**P1 — Disciplines (no code):**
7. Memory hygiene rule: >80% → consolidate before add (official); state snapshots
   never enter memory (DOC-11 state-in-WO); procedures live in skills only.
8. Optional config hygiene: remove stale `flush_min_turns` key (dead config) —
   evidence-only repair.

**P2 — Future option (NOT now):**
9. If semantic retrieval ever needed → `hermes memory setup` (mem0/honcho/supermemory
   already installed) — one command, no reinvention.
10. memory_char_limit modest raise ONLY if pruning proves insufficient.

## 5. Non-goals (anti-over-engineering)
- NO vector DB, NO new tool install, NO product code change, NO external provider
  activation this round, NO auto-compaction implementation.


### 5.2 Plan + Gate-2 submission (M5) — verbatim
# M5 — Plan MD + Gate 2 HITL Submission (DRAFT — pending challenge lane)

## Hermes 持久記憶體（95% 滿）處置計畫 — 用戶決策提交

- WO: WO-HGK-MEM-RESEARCH-001 | Board: hermes-memory-far | 2026-08-14 UTC
- Gate 1 (FAR research) 完成：TRI_SOURCE（知識庫 DOC-11 / Hermes 原始碼+官方 docs / 聯網社群 2026-05-08）
- Gate 2 (本文件)：提交用戶 HITL 決策，不自批准

## 研究結論摘要

1. **記憶體 95% 滿是設計預期狀態，非異常**：Hermes 官方明示 memory 不自動壓縮，滿載時工具回錯誤、agent 當回合自行 consolidate（最多 3 次保險絲，#42405）。上限 `memory_char_limit` 可調但官方建議保持聚焦。
2. **治理面（DOC-11）**：memory 不是 truth；六類分類；retention 必須 finite；狀態快照屬 WorkOrder/evidence 不屬記憶體；程序性內容屬 skill；supersession 保留 lineage；壓縮必須可回讀可 rollback。
3. **社群面（2026-05-08）**：檔案即記憶是業界標準（Anthropic/OpenAI/AGENTS.md）；2200-char + §-分隔 = 手動 context compaction，符合 Anthropic 官方最佳實務；向量庫/重型框架（mem0/Graphiti/Cognee）對單檔是過度工程；Hermes 已內建 7 個外部 provider（mem0/honcho/supermemory 等）為未來選項。
4. **現況分析**：MEMORY.md 16 條目，多條為狀態快照（hash/cron id/進行中專案，7 天後過時）與 skill 重複內容（強制規則→hgk §15/§6A、4-failures→skill、Gate→Step 10A）。

## 建議方案（P0 立即執行，需用戶批准）

### P0-A 逐條分類（DOC-11 六類）
- 16 條目逐條標 class/scope/retention，operator 五問篩選。

### P0-B 修剪（目標 2101 → ~1100-1300 chars）
1. **移除狀態快照**（估釋 ~45-50%）：RP-002 狀態、FDA/FAR hash、cron id、DoD-17、MATT pending、GENIE 進行中 → 內容可由 kanban/evidence/session_search 查得，記憶體只留 pointer。
2. **移除 skill 重複**：已入 skill 的規則改為一行 pointer 或直接刪除。
3. **合併/壓縮環境事實**：Codex lane 細節、SQS data_plane、知識庫路徑 → 高密度單條。

### P0-C 執行方式（保守、可回滾、符合 DOC-11 withdrawal/readback 契約）
1. **備份**：MEMORY.md/USER.md 原始 bytes → var/hermes-memory-research/backup/（rollback 點）。
2. **裁決依據**：以 DOC-11 retention/expiry/supersession policy 逐條裁決（非「容量到了就刪」）：
   - 狀態快照（hash/cron id/進行中專案）→ working/episodic class，暫態不持久化（DOC-11 L177/L185）→ 移出至
     WorkOrder/kanban/evidence（canonical artifact 落地，非無痕消失）。
   - skill 重複內容 → 既有 skill 已建置，記憶體中僅 pointer → 去重（保留指向 skill 的 provenance 註記）。
   - 環境/工具事實 → semantic class，合併壓縮、保留 superseded lineage。
3. **執行**：用 memory tool 的 replace/remove/apply_batch 執行（非手動編輯，避免 drift guard 衝突）；
   若需手動編輯須維持乾淨 `\n§\n` 分隔格式。逐條移除記錄為 WithdrawalEvent（audit trail）。
4. **驗證**：移除後讀回用量（目標 <80%）；frozen snapshot 使編輯要到**下一 session** 才生效——
   效果驗收在下一 session 進行（FINDING-03 操作備註）。
5. 註：provider 數量為 **8**（含 supermemory，FINDING-01 修正）；「prefer session_search/skill
   over raising limit」為研究綜合結論、非 docs 逐字（FINDING-02 歸因修正）。

### P1 紀律（無代碼）
- >80% 先 consolidate 再 add；狀態快照不入記憶體；程序入 skill；session_search 承接細節。
- **Pointer-only 紀律（M8 新增）**：記憶條目存「pointer + 一句話」，細節一律路由知識庫/spine/session_search；
  FAR tri-source retrieval 已是現成檢索資產（spine FTS5 354 docs ENABLED + 知識庫 9,706 md）——無需新工具。
- 選項：移除 config 死鍵 `flush_min_turns`（原始碼零引用）——evidence-only 修補。

### P2 未來選項（本輪不做）
- **觸發條件①已重新表述（M8 質疑回應）**：FABRIC 已自建跨 session 記憶檢索層（spine FTS5 + FAR tri-source +
  知識庫 + session_search）——「需要檢索」不再是啟用 provider 的理由。唯一未滿足的是 **embedding 概念相似度
  檢索**（FTS5 keyword 找不到的語意場景）且 FAR tri-source 已證明不足——目前無此實證。
- 若未來需要 embedding 語意 → `hermes memory setup` 一行啟用已安裝 provider（mem0/honcho/supermemory），
  啟用前走 qualification WO（TOOL-24）；或本地 txtai 等級 embedding（無外部依賴）。
- `memory_char_limit` 微幅調高（2200→2600）僅在修剪後仍不足時考慮。

## 非目標（不過度工程化）
- 不裝向量庫、不啟用外部 provider、不改產品碼、不實作自動壓縮、不新建工具。

## 待用戶決策項目
1. 是否批准 P0 修剪執行（含具體逐條刪除清單）？
2. 是否批准 P1 之 `flush_min_turns` 死鍵移除？
3. 是否維持 2200 上限不動（建議）？


### 5.3 FABRIC-infra retrieval analysis (M8, user-challenge response) — verbatim
# M8 — 用戶質疑回應：FABRIC 基礎設施是否已構成「跨 session 大量記憶的語意檢索層」？

- WO: WO-HGK-MEM-RESEARCH-001 | M8 card t_d4f99204 | 2026-08-14 UTC
- 質疑：Hermes 內建 8 個外部 provider「未來啟用」的觸發條件①（需要跨 session 大量記憶的語意檢索）——
  用戶指出 FABRIC 內 HGK/SQS/FAR/FDA/知識庫已達此需求。本報告實證盤點後回應。

## 1. 實證盤點（2026-08-14 現場查證，非推論）

| 基礎設施 | 檢索能力（實證） | 狀態 |
|---|---|---|
| **HGK Shared Spine** | `knowledge_docs` 354 筆 + `knowledge_fts`（SQLite FTS5 全文索引）；`KnowledgeFactory` API（ingest_text/promote/search/remember/revoke_memory/active_memory/withdraw_source）於 `src/hg_kseos/knowledge.py` | **已啟用**：FTS5 MATCH 實測命中（memory=164、retention=151、promotion=219、Hermes=156） |
| **HGK provider_bindings** | `HGK-PROVIDER-FTS5` = semantic-retrieval / XOR-RETRIEVAL / PREFERRED_DEFAULT / **ENABLED** / builtin SQLite FTS5 probe | 註冊且 ENABLED（79 筆 binding 之一） |
| **HGK memory_records** | DOC-11 式記憶表（memory_id/scope/body/provenance/expires_at/revoked_at），1 筆（PCIV-F01 closure 實例） | 機制存在，使用率低 |
| **FAR（fabric-autonomous-research）** | `far_retrieval.py`：**tri-source 檢索**（知識庫 root 掃描 + spine `knowledge_fts MATCH` + memory rows），tokenize + score_doc + top_k；`retrieve_knowledge_base()` / `retrieve_memory()` | **FAR 已資格化資產**（FAR v3 ACTIVE，103 tests） |
| **知識庫** | 9,706 個 md（工程基座 5,916、專業技術文檔 169、實作相關DOC 157、HG-KSEOS_SSOT 86…）；`search_files`（ripgrep 全文） | 持續擴充（08-14 新域 ASCE-WebX 1,328 md、TCA-10X 449 md） |
| **Hermes session_search** | SQLite FTS5，state.db 138 MB，跨 session 全文檢索，免費無限 | 內建 |
| **SQS data_plane** | duckdb/parquet 金融資料層（非記憶，domain stack） | 與本題無關但屬 FABRIC 資產 |

## 2. 質疑判定：**成立（部分）**——FABRIC 確實已具備「跨 session 大量記憶檢索層」

用戶觀察正確：FABRIC 不是「還沒有檢索能力所以未來要接 provider」，而是
**早已自建一套本地、可稽核、受治理的記憶/知識檢索層**（spine FTS5 + FAR tri-source + 知識庫 + session_search）。
這正是 DOC-11/DOC-12 架構的落地：canonical knowledge 在知識庫/evidence，memory 是 candidate，
檢索經 FTS5（source-backed、可回讀）。

## 3. 但這**強化**而非推翻「不啟用外部 provider」的結論

| 面向 | FABRIC 現有層 | 外部 provider（mem0 等） |
|---|---|---|
| 檢索 | FTS5 keyword（可回讀、可稽核、本地零依賴） | embedding 語意（黑箱相似度，無法解釋 hit 理由） |
| 治理 | KnowledgeFactory 有 provenance/promote/withdraw/verify_citation | DOC-12 明言檢索必須 source-backed；embedding 黑箱與治理原則相斥 |
| 維運 | 零（spine 內建） | API key/自架伺服器/資料外送/每 turn 成本 |
| 資格化 | FAR 已資格化（103 tests） | 未資格化（DOC-11 SC-DOC11-10: QUARANTINE_UNTIL_REPROBE） |
| 語意能力 | FTS5 無同義詞/概念相似（keyword only） | embedding 有概念相似——**唯一勝出點** |

**唯一真實 gap**：FTS5 是 keyword 檢索，非 embedding 語意檢索（例如「找與『記憶治理』概念相關的歷史決策」
需要概念相似度，FTS5 只能命中含字串者）。但：
- 此 gap 是「檢索品質」問題，**不是「容量」問題**——2200-char 的 MEMORY.md 根本不需要檢索（全量注入即 ~800 tokens）；
- 若真需要語意檢索，也**不需外部 provider**：可先用 FAR tri-source（現成）+ 未來選項（txtai 等級本地 embedding、
  `hermes memory setup`）——都不是本輪範疇。

## 4. 對計畫的修正（M5 更新）

1. **P2 觸發條件①重新表述**：從「需要跨 session 大量記憶檢索」→ **「需要 embedding 概念相似度檢索
   （FTS5 keyword 找不到的語意場景），且 FAR tri-source 已證明不足」**——目前無此實證。
2. **Hermes 2200-char MEMORY.md 的正確角色**：hot pointer cache（高頻 pointer），非唯一記憶體；
   大量記憶/知識的 canonical home = 知識庫 + spine（FTS5 可檢索）——與 DOC-11 架構一致。
3. **新增 P1 紀律（無代碼）**：記憶條目應存「pointer + 一句話」，細節一律路由知識庫/evidence/session_search；
   FAR tri-source retrieval 已是現成檢索資產，無需新工具。
4. **非目標新增**：不因「需要檢索」而啟用外部 provider——FABRIC 已自建檢索層。

## 5. 結論

- 用戶質疑**正確**：FABRIC 已達「跨 session 大量記憶檢索」需求（實證：spine FTS5 354 docs ENABLED +
  FAR tri-source + 知識庫 9,706 md + session_search）。
- 但「已自建檢索層」正是**不需要外部 provider 的最強理由**：現有層本地、可稽核、已資格化；
  外部 provider 唯一勝出點（embedding 語意）非本輪需求，且 DOC-12 治理上 embedding 黑箱反而是負分。
- Hermes 記憶體 95% 滿的處理**不變**：P0 修剪（釋放 ~50%）+ P1 紀律（pointer-only）——
  修剪後的內容 canonical home 正是 FABRIC 已具備的知識庫/spine 層。

## 6. 證據
- HGK spine 實測：knowledge_docs 354、knowledge_fts 354、FTS5 MATCH 命中、provider_bindings 79（HGK-PROVIDER-FTS5 ENABLED）
- far_retrieval.py：tri-source retrieval（知識庫 + spine MATCH + memory）
- src/hg_kseos/knowledge.py：KnowledgeFactory 完整 API
- 知識庫 9,706 md、session_search 138 MB


---

## 6. EMBEDDED EVIDENCE — KB/MEMORY/KG UPGRADE RESEARCH (WO-HGK-KBUPGRADE-RESEARCH-001)

### 6.1 Cross-analysis (K4) — verbatim
# K4 — Cross-Analysis: FABRIC KB/Memory/KG Infrastructure Upgrade (TRI_SOURCE integration)

WO-HGK-KBUPGRADE-RESEARCH-001 | Board fabric-kb-upgrade-far | 2026-08-14 UTC

## 1. The user's proposal
拆出 HGK spine 的 memory/knowledge/KG 設施 → 升格為 FABRIC 級共享基礎設施
（Shared Infrastructure Profile Team）→ 整合 FABRIC 現有知識資產 → 受 FABRIC 治理，
服務 HGK/SQS/FAR/FDA 跨 session 共享。

## 2. What the three lanes established

### Lane A — Folder audit (facts)
- HGK knowledge assets are a COHESIVE cluster: 8 tables (sources/source_units/candidates/
  knowledge_docs/knowledge_fts/kg_edges/kg_assertions/memory_records) + KnowledgeFactory
  (11 methods, ingest/promote/search/remember/revoke/verify_citation/withdraw) + CLI +
  5 test files + 3 domain acceptance evidences (L3+L4 ten checks PASS, p0=lexical FTS-first,
  vector DEFERRED_SOURCE_BACKED).
- **DATA DEBT**: 354 FTS docs' canonical_paths are ALL dead (sources point to deleted
  SQS-THC\SSOT + 技術資料庫 dirs; files moved to 知識庫\HG-KSEOS_SSOT etc.) — ERR_SOURCE_DRIFT
  cannot pass until re-ingest.
- **DUPLICATION**: FAR retrieve_memory() re-implements spine FTS MATCH + LIKE fallback (bypasses
  KnowledgeFactory); KB file-scan and FTS index are two parallel non-overlapping retrieval paths.
- **UNUSED**: kg_edges/kg_assertions = 0 rows (KG pipeline complete but never used);
  memory_records = 1 row. evidence_graph.py (EVO-005) is a SECOND graph facility — must disambiguate.
- **GOVERNANCE SLOTS PRE-RESERVED**: KNOWLEDGE_POLICY (shared.* namespace,
  cross_namespace_write_default=DENY, domain_owner_retains_truth_authority=true),
  KG1 provider_runtime_validation_gate, A0_KNOWLEDGE_EXTENSION_EVIDENCE,
  HGK_STACK_MANIFEST knowledge_fts service, hgk-knowledge-factory profile.
- Consumption coupling: SQS data_plane 6 modules `from hg_kseos.knowledge import KnowledgeFactory`
  (direct imports); HGK ~10 reference points.

### Lane B — Web/industry (community consensus)
- Industry mainstream for shared agent knowledge = **shared file/Git layer + namespace isolation**
  (Letta shared-memory repos, OpenAI sessions/layouts, LangGraph Store, Claude memory tool).
  NOT building a standalone memory platform.
- Heavy platforms are the anti-pattern: MemGPT/Letta pivot, OpenMemory retirement, Fowler
  Integration Database, mem0 #5151 shared-graph memory poisoning (high-severity), platform team trap.
- Hermes MemoryProvider ABC already supports external shared providers; "sharing" happens at the
  provider service layer; only one provider active at a time.
- Data-mesh federated governance = platform manages standards, domains own content.
- Recommendation: 3-stage — ① shared data layer (Git KB + conventions + schema) first;
  ② governance first (federated); ③ KG/graph service LAST (only with cross-member consistency
  needs + tenant isolation + audit).

### Lane C — Governance (DOC-01/02/08/11/12/13/20 + FABRIC blueprint)
- 15 governance principles verified with quotes: canonical knowledge is source-backed approved
  artifact; memory is candidate state; KG is rebuildable derived view; taint-as-DATA;
  four-gate memory; no cross-tenant poisoning; grounded retrieval 7-gate admission;
  KG edge admission (schema-first, evidence locator per edge); time-bounded published trust;
  CH-20 candidate-first + AssetHealthRecord; no self-approval.
- Profile-team blueprint exists: RP002-PROFILE-TEAM-MANIFEST/1, team_class
  SHARED_INFRASTRUCTURE_PROFILE_TEAM, FDA/FAR precedents with full WO→CAPC→canary→dual-lane
  acceptance→freeze pipeline; admission gates G0..R1; additive manifest, no fork.
- **VERDICT: feasible = PARTIAL** — feasible ONLY as "FABRIC shared capability substrate"
  (heavy_stack=false, fabric.* candidate-only namespace), NOT as "knowledge truth transfer".
  Extraction is a constitutional change → needs human two-key approval.
  Three bottom lines: domain_owner_retains_truth_authority=true,
  cross_namespace_write_default=DENY, fabric_can_mutate_truth=false.
  Otherwise violates DOC-01 hard invariants #1/#4 + AGENTS.md "no knowledge platform substitution".

## 3. Engineering assessment (SoD + no-over-engineering + consensus)

### The convergence: all three lanes point the SAME direction
- Lane A: HGK knowledge cluster is extractable (high feasibility) BUT has data debt + duplication.
- Lane B: industry says shared FILE/Git layer, not a platform; KG last.
- Lane C: governance says possible as capability substrate with strict conditions.

### Recommended architecture (3-stage, matches industry + governance)
```
STAGE 1 (shared data layer — NOW, low cost, high value):
  - FABRIC 知識庫 (9,698 md) becomes THE canonical shared knowledge layer (already is, de facto).
  - Fix the stale-index debt: re-ingest 知識庫\HG-KSEOS_SSOT + SQS-THC&TW-ICT_SSOT as canonical
    roots into knowledge_fts (354 → full corpus), making the FTS index a true projection of the KB.
  - Converge duplicate retrieval: FAR retrieve_memory() → call KnowledgeFactory.search (one API).
  - Keep hgk-knowledge-factory profile as the operating identity (role-level distillation executor).
  - NO new platform, NO new DB, NO KG enablement yet.

STAGE 2 (formalize the profile team — governance):
  - Materialize fabric-knowledge-infrastructure (name TBD) as SHARED_INFRASTRUCTURE_PROFILE_TEAM
    per RP002 manifest (additive rows, no fork): TEAM.md + governance/ + evidence/ + receipts/ +
    capability matrix + execution binding — FDA/FAR precedent pipeline (WO → CAPC → canary →
    dual-lane acceptance → freeze).
  - Scope: shared capability substrate (index pipeline, retrieval API, admission gates, health
    records) under fabric.* candidate-only namespace; KNOWLEDGE_POLICY updated additively.
  - SoD: team MAY NOT CREATE_WORKORDER / SELF_ACCEPT / SELF_PROMOTE / CREATE_SECOND_KNOWLEDGE_PLATFORM.
  - Truth authority stays with domain owners (HGK hgk.approved.*, SQS sqs.* read-only).

STAGE 3 (KG — LAST, conditional):
  - kg_edges pipeline becomes shared ONLY when a cross-member consistency need is proven AND
    DOC-12 edge admission (schema-first, evidence locator, checker, effective interval,
    high-risk dual-source) + tenant isolation + audit are all in place.
  - Disambiguate kg_edges vs evidence_graph.py (EVO-005) — ONE graph facility.
  - Qdrant/Neo4j/pgvector remain default-off; any enablement = separate qualification event.
```

## 4. Non-goals / anti-over-engineering
- NO new "second knowledge platform" (AGENTS.md invariant).
- NO standalone memory server / vector DB this round.
- NO knowledge-truth transfer out of domain owners.
- NO KG enablement until Stage-3 conditions are proven.
- NO rewrite of Hermes memory system — the 2200-char MEMORY.md stays as the hot pointer cache;
  the shared layer is where the pointer content lives (M8 conclusion unchanged).

## 5. SoD matrix (who does what)
| Role | Authority |
|---|---|
| HGK (governance plane) | WorkOrder existence/owner/acceptance; hgk.approved.* truth authority |
| FABRIC (new team) | Shared substrate operations: index, retrieval API, admission gates, health records (fabric.* candidate-only) |
| Domain owners (SQS/FAR/FDA) | Their own knowledge content; consumption binding |
| Hermes | Orchestration, kanban, dispatch |
| Oracle / AO | Independent acceptance (VERIFY_ONLY) + external |

## 6. Bottom line
User's proposal is architecturally SOUND and matches FABRIC's original design intent
(governance slots were pre-reserved). It is feasible as a SHARED_INFRASTRUCTURE_PROFILE_TEAM
capability-substrate upgrade — NOT as a knowledge-truth migration. Recommended execution:
3 stages, Stage 1 (data-layer consolidation + stale-index repair) is the highest-value,
lowest-risk first move and can proceed under the EXISTING hgk-knowledge-factory profile +
FAR tri-source without any new infrastructure; Stage 2 formalizes governance; Stage 3 (KG)
is conditional and last.


### 6.2 Report + Gate-2 submission (K5) — verbatim
# K5 — Report MD + Gate 2 HITL Submission（草案，待驗收 lane 結果後定稿）

## FABRIC KB/Memory/KG 共享基礎設施升級 — 用戶決策提交

- WO: WO-HGK-KBUPGRADE-RESEARCH-001 | Board: fabric-kb-upgrade-far | 2026-08-14 UTC
- Gate 1 (FAR research) 完成：TRI_SOURCE（資料夾審計 / 聯網 / 治理分析）
- Gate 2 (本文件)：提交用戶 HITL，不自批准

## 研究結論摘要

1. **您的提案方向正確且符合 FABRIC 原始設計意圖**：FABRIC 治理面早已預留槽位
   （KNOWLEDGE_POLICY shared.* namespace、KG1 gate、HGK_STACK_MANIFEST knowledge_fts service、
   hgk-knowledge-factory profile）——缺的只是 runtime 擁有者與統一管線。
2. **可行性判定：部分可行**——僅限「共享能力基板（SHARED_INFRASTRUCTURE_PROFILE_TEAM,
   heavy_stack=false, fabric.* candidate-only）」形式；**不可理解為知識 truth 轉移**。
   拆出屬 constitutional change，需 human two-key approval。
3. **三條底線**（違反即違 DOC-01 硬不變式 + AGENTS.md「no knowledge platform substitution」）：
   domain_owner_retains_truth_authority=true；cross_namespace_write_default=DENY；fabric_can_mutate_truth=false。
4. **業界共識（聯網）**：共享 agent 知識的主流 = 共享檔案/Git 層 + namespace 隔離
   （Letta/OpenAI/LangGraph/Claude），非獨立記憶平台；重型平台為反面教材
   （MemGPT pivot、OpenMemory 退役、mem0 #5151 圖譜記憶投毒）。
5. **資料債**：354 筆 FTS 索引的 canonical_path 全數失效（來源已搬遷知識庫）；FAR retrieve_memory
   與 KnowledgeFactory.search 重複實作；kg_edges 空置（0 行）。

## 建議架構（3-stage，符合業界 + 治理）

```
Stage 1（資料層 — 現在可做，成本最低、價值最高）：
  • 知識庫 9,698 md = FABRIC 共享知識層（已是 de facto）
  • 修復 stale-index 債：以 知識庫\HG-KSEOS_SSOT + SQS-THC&TW-ICT_SSOT 為 canonical root 重新 ingest
  • 收斂重複檢索：FAR retrieve_memory() → 呼叫 KnowledgeFactory.search（單一 API）
  • 維持 hgk-knowledge-factory profile 作為運作身分
  • 不建新平台、不建新 DB、不啟用 KG

Stage 2（治理正規化 — formalize profile team）：
  • 依 FDA/FAR 先例落地 SHARED_INFRASTRUCTURE_PROFILE_TEAM
    （TEAM.md + governance/ + evidence/ + receipts/ + 能力矩陣 + 執行綁定；
    WO → CAPC → canary → 雙 lane 驗收 → 凍結）
  • 範圍：共享能力基板（索引管線、檢索 API、admission gates、health records）
  • SoD：不得 CREATE_WORKORDER / SELF_ACCEPT / SELF_PROMOTE / CREATE_SECOND_KNOWLEDGE_PLATFORM
  • Truth authority 留在各 domain owner

Stage 3（KG — 最後、條件性）：
  • kg_edges 管線僅在「跨成員一致性命中需求被證明」且 DOC-12 edge admission
    （schema-first、每 edge evidence locator + checker + effective interval、高風險雙來源）
    + tenant 隔離 + 審計齊備後才共享
  • 釐清 kg_edges vs evidence_graph.py（EVO-005）——只保留一個圖設施
  • Qdrant/Neo4j/pgvector 維持 default-off
```

## SoD 矩陣

| 角色 | 權限 |
|---|---|
| HGK（治理面） | WorkOrder 存在/owner/驗收；hgk.approved.* truth authority |
| FABRIC（新團隊） | 共享基板操作：索引、檢索 API、admission gates、health records（fabric.* candidate-only） |
| 各 domain owner（SQS/FAR/FDA） | 自己的知識內容；消費綁定 |
| Hermes | 編排、kanban、派發 |
| Oracle / AO | 獨立驗收（VERIFY_ONLY）+ 外部 |

## 非目標（不過度工程化）
- 不建第二知識平台（AGENTS.md 不變式）
- 本輪不建獨立記憶伺服器 / 向量庫 / KG
- 不做知識 truth 轉移出 domain owner
- 不改寫 Hermes 記憶系統（2200-char MEMORY.md 維持 hot pointer cache）

## 待用戶決策
1. 是否批准 **Stage 1**（stale-index 重新 ingest + 檢索 API 收斂）在現有 hgk-knowledge-factory
   profile + FAR tri-source 下執行？（不建新基礎設施）
2. 是否批准啟動 **Stage 2** 治理正規化（SHARED_INFRASTRUCTURE_PROFILE_TEAM 落地，
   constitutional two-key approval 流程）？
3. Stage 3（KG）是否確認「條件性最後、本輪不做」？

## 驗收 lane 修正（FINDING 整合，2026-08-14，挑戰 lane PASS 之 5 項低嚴重度瑕疵）
1. RAG KB acceptance 為 **14/14 checks**（非「十項」）；depth=L3+L4；backend=SQLite FTS5 via KnowledgeFactory。
2. KnowledgeFactory 具名方法 **10 個**（+__init__），非 11。
3. HGK KnowledgeFactory 相關測試檔 **4 個**（test_knowledge / test_knowledge_memory_poison /
   test_knowledge_promotion_gate / test_e2e_vertical_slice），非 5。
4. 治理槽位檔案實際位置：`Fabric/stage/RP002-STAGE-FABRIC/A0_KNOWLEDGE_EXTENSION_EVIDENCE.yaml`、
   `Fabric/stage/RP002-STAGE-HGK/KG1/KG1_NAMESPACE_MODEL.json`、`Fabric/HGK_STACK_MANIFEST.yaml`
   （非全部在 Fabric/control/）。
5. sources **351/351 全數 dead**（12 → SQS-THC\SSOT、339 → SQS-THC\技術資料庫），
   knowledge_fts 354 筆索引全部源於已刪除路徑——stale-index 債確認無誤（比研究者宣稱更徹底）。
以上均不影響結論方向（CHALLENGE_VERDICT=PASS）。


---

## 7. EMBEDDED EVIDENCE — CODEX PRIMARY-EXECUTION ARTIFACTS (writer=codex)

### 7.1 memory_research_analysis.md — verbatim
# Hermes Agent Memory — Research Analysis

**WorkOrder:** WO-HGK-MEM-RESEARCH-001 · **Writer:** codex · **Governance:** HG-KSEOS · **Date:** 2026-08-14 · **Mode:** read-only analysis

## 1. Executive Summary

- MEMORY.md is at 2101/2200 chars (95%) and USER.md at 340/1375 (24%); the working memory is effectively full and the next substantive write is at risk of rejection.
- Memory does not auto-compact by design: an over-limit write returns an error, and the agent must free space in the same turn via replace/remove/apply_batch, capped at 3 failed attempts per turn (issue #42405).
- The 2200-char ceiling is tunable via `memory.memory_char_limit`, but official guidance is to consolidate above 80% and prefer `session_search`, skills, and external providers over raising the limit.
- All necessary native machinery already exists: atomic batch edits, drift guard (#26045), injection/exfil scan, write-approval gate, background review nudge (`nudge_interval 10`), and unlimited free FTS5 `session_search`.
- Governance (KB DOC-11) frames memory as a cache, not truth: four gates, six-class taxonomy, finite retention, readable-back/rollback-able compaction (DOC-10 §9), and state snapshots belong in WorkOrder evidence, not memory.
- The single-file 2200-char design matches 2026 industry consensus: file-as-memory (Anthropic memory tool, OpenAI project memory, AGENTS.md) plus compaction/summarization/retrieval over unbounded context.
- Heavy vector-DB frameworks (mem0, Graphiti, Cognee, Letta) are over-engineering at this scale; the correct move is consolidation plus discipline, not new tooling.
- Recommended path: P0 consolidate+prune to below 80%, P1 standing disciplines, P2 optional one-command provider activation — with explicit non-goals: no vector DB, no new tool install, no product code change.

## 2. Native Capability Inventory

| Capability | Mechanism | How it helps when memory is full |
|---|---|---|
| `memory` tool | add / replace / remove / `apply_batch` (atomic batch) | Frees characters via replace/remove; `apply_batch` consolidates many entries in one atomic, fuse-safe turn |
| No auto-compaction (by design) | over-limit writes error; agent must make room in same turn (#42405) | Forces explicit, auditable consolidation instead of silent eviction |
| `memory.memory_char_limit` | config-tunable limit (default 2200) | Adjustable ceiling, but docs recommend discipline over raising it |
| Drift guard | issue #26045 | Flags stale/contradictory entries, making prune targets identifiable |
| Injection / exfil scan | pre/post-write content scan | Keeps merged/rewritten entries safe during consolidation |
| Write-approval gate | approval on memory mutations | Review point before overwriting existing knowledge |
| Background review nudge | `nudge_interval 10` | Periodic review reminder; prevents silent drift to 95%+ usage |
| `session_search` | FTS5, unlimited, free | Offloads detail: memory holds pointers, search retrieves full context on demand |
| `hermes memory` CLI | setup / status / off / reset; 7 providers | `status` shows headroom; `reset` is an escape hatch; `setup` unlocks provider overflow |
| Journey timeline | episodic timeline in Hermes | Episodic history lives outside MEMORY.md; memory can reference it instead of copying it |
| `/memory` slash commands | user-facing memory UI | Operator-triggered status/consolidation without agent-turn overhead |

## 3. Memory-Full Handling Paths

**What happens (ordered):**
1. A write that would exceed 2200 chars is rejected with an error; nothing is auto-compacted or silently evicted.
2. The agent must free space in the same turn — replace, remove, or `apply_batch` — with a fuse of max 3 failed attempts per turn (#42405).
3. If space cannot be freed, the write is dropped and memory is unchanged: no silent loss, but no new information retained.
4. Unmanaged, MEMORY.md sits at 95% (2101/2200) — the next substantive write is already at risk.

**Official paths:**
- Consolidate at >80% before adding: merge, summarize, prune.
- Prefer `session_search`, skills, and external providers over raising `memory.memory_char_limit` ("Character limits keep memory focused").
- Use atomic `apply_batch` for safe multi-entry consolidation in one turn.
- When a provider is configured, provider overflow via the `hermes memory` CLI is the sanctioned escape valve; otherwise keep memory small and curated.

**Our recommended path:**
- P0 (now): consolidate+prune MEMORY.md below 80% with entry classification; keep semantic/procedural, compress working/episodic, drop stale/duplicated; supersede, preserving lineage; snapshot the pre-change state in WorkOrder evidence so compaction is readable-back and rollback-able (DOC-10 §9).
- P1 (standing): enforce the >80% rule before every write; no state snapshots in memory; `session_search` for detail; promote reusable entries to Skill/KB only via the owner gate with anti-loop; remove the stale dead key `memory.flush_min_turns: 6` (unreferenced in source).
- P2 (optional): if capacity pressure recurs, `hermes memory setup` (one command) activates a provider as the sanctioned overflow layer.

## 4. Community Best-Practice Alignment

- **File-as-memory is the 2026 standard.** Anthropic's memory tool, OpenAI project memory, and the AGENTS.md ecosystem all use small human-readable files as the durable memory layer; Hermes' MEMORY.md + USER.md pair is exactly this design family.
- **Anthropic effective-context-engineering** explicitly recommends compaction, summarization, and retrieval over unbounded context windows — matching Hermes' hard char limit, `session_search`, and consolidation model.
- **Token economy:** MEMORY.md is injected as a frozen snapshot into every system prompt, so every character costs tokens on every turn. A small curated memory is cheaper than external retrieval for hot facts, and unlimited FTS5 `session_search` covers the long tail.
- **Auditable compaction:** "No auto-compact; agent makes room" aligns with the shift from silent summarization to explicit, rollback-able consolidation (DOC-10 §9).
- **Tooling consensus:** vector-DB memory frameworks earn their complexity only at multi-agent or large-corpus scale; for a single 2.2 KB file they are the outlier, not the answer.

## 5. External Tool Landscape Assessment

| Tool | Stars / heat | Mechanism | Fit for 2200-char design |
|---|---|---|---|
| claude-mem | 90.7k stars | File/note persistent memory for Claude Code | NOT NEEDED — duplicates the native MEMORY.md pattern |
| mem0 v3 | 63k stars | Vector-store memory with LLM extraction | OVER-ENGINEERING — extraction + vectors for a single small file |
| Graphiti / Cognee / Letta | large | Knowledge-graph / semantic memory engines | OVER-ENGINEERING — graph + vector infrastructure with no scale to justify it |
| akitaonrails/ai-memory | 1.5k stars | AI memory framework | DISCIPLINE-ONLY — same file + prune discipline, no new capability |
| memory-os for Hermes | 1.3k stars | Memory OS integration for Hermes | FUTURE-OPTION — relevant only if provider-based memory is activated (P2) |
| OpenViking | trending | Provider option in `hermes memory` CLI | FUTURE-OPTION — one of 7 providers; activate via `setup` if needed |

## 6. Recommended Plan

**P0 — Consolidate + prune (immediate):**
- Classify every MEMORY.md entry with the six-class taxonomy (working / episodic / semantic / procedural / shared / fleet).
- Keep semantic and procedural facts reused every session; compress working/episodic entries to one-line pointers; drop stale, superseded, or duplicated entries; supersede with lineage preserved.
- Target < 80% (~1760 chars) with headroom for at least one turn of writes.
- Keep the pre-consolidation snapshot in WorkOrder evidence; verify the result reads back correctly (readable-back, rollback-able per DOC-10 §9).

**P1 — Standing disciplines:**
- >80% rule: consolidate before adding; never write into >80% without freeing space first.
- No state snapshots in memory: state belongs in WorkOrder/evidence, not MEMORY.md (DOC-11).
- `session_search` for detail: memory holds pointers; search holds full context (FTS5, unlimited, free).
- Promotion with owner gate + anti-loop before moving entries to Skill/KB.
- Config hygiene: delete the stale dead key `memory.flush_min_turns: 6` (referenced nowhere in source).
- Use `nudge_interval 10` background reviews to schedule consolidation.

**P2 — Future option (only if capacity pressure recurs):**
- `hermes memory setup` — one-command activation of a provider (honcho / openviking / mem0 / hindsight / holographic / retaindb / byterover) as the sanctioned overflow layer.
- Re-evaluate external memory frameworks only if scale (multi-agent, large corpus) actually demands it.

**Non-goals (explicit):**
- No vector DB adoption.
- No new tool installation.
- No product code change.
- No change to `memory.memory_char_limit` behavior unless an operator explicitly decides otherwise after P0/P1.

## 7. Evidence Trail

- WorkOrder: WO-HGK-MEM-RESEARCH-001 (writer: codex)
- Governance: HG-KSEOS
- Board: HG-KSEOS research board — three independent research lanes: L1 native capabilities, L2 KB governance, L3 community/tool landscape
- Key file paths:
  - `%LOCALAPPDATA%/hermes/memories/MEMORY.md` (2101/2200 chars, 95%)
  - `%LOCALAPPDATA%/hermes/memories/USER.md` (340/1375 chars, 24%)
  - KB `Hermes_Agent_OS` DOC-11 (Agent Memory governance) and DOC-10 §9 (compaction rollback/readback)
  - Local config: stale dead key `memory.flush_min_turns: 6` (unreferenced in source)
  - Issue refs: #42405 (memory-full turn fuse), #26045 (drift guard)
  - This deliverable: `C:\Projects\Agent_Workspace\var\hermes-memory-research\codex_output\memory_research_analysis.md`

### 7.2 fabric_kb_upgrade_analysis.md — verbatim
# FABRIC KB Upgrade — HGK SharedSpine Shared-Infrastructure Analysis

WorkOrder: WO-HGK-KBUPGRADE-RESEARCH-001 | Writer: codex | Date: 2026-08-14 | Mode: read-only analysis

## 1. Executive Summary

- HGK SharedSpine memory/knowledge/KG facilities are viable extraction candidates for a FABRIC-level shared infrastructure profile team — but only as a shared capability substrate (heavy_stack=false, fabric.* candidate-only namespace), never as a knowledge-truth transfer.
- The knowledge cluster is cohesive and evidence-backed: knowledge_fts FTS5 (354 docs), KnowledgeFactory API (11 methods: ingest_text/promote/search/rebuild/add_kg_assertion/verify_citation/withdraw_source/remember/active_memory/revoke_memory), CLI, 5 tests, and RAG_KB_RUNTIME_ACCEPTANCE L3+L4 (ten checks PASS; p0_disposition=ACTIVE_REQUIRED, lexical/FTS-first, vector DEFERRED_SOURCE_BACKED).
- Data debt blocks the runtime guard today: all 354 knowledge_docs canonical_path sources point to deleted SQS-THC directories; ERR_SOURCE_DRIFT cannot pass until re-ingest from the two relocated SSOT directories.
- Duplication exists: FAR retrieve_memory() (far_retrieval.py L149-229) re-implements spine FTS MATCH + LIKE fallback and bypasses KnowledgeFactory; the KB raw-file scan and the FTS index are two parallel, non-overlapping retrieval paths.
- kg_edges/kg_assertions hold 0 rows and memory_records holds 1 row; evidence_graph.py (EVO-005) is a second, distinct graph facility that must be disambiguated before any KG work.
- Governance slots are pre-reserved: KNOWLEDGE_POLICY.yaml (FABRIC-KNOWLEDGE-POLICY/1), KG1_NAMESPACE_MODEL.json, A0_KNOWLEDGE_EXTENSION_EVIDENCE.yaml, HGK_STACK_MANIFEST.yaml, and the existing Fabric\profiles\hgk-knowledge-factory profile.
- Governance verdict is PARTIAL: feasible only as a FABRIC shared capability substrate; the extraction itself is a constitutional change requiring human two-key approval.
- Three bottom lines must hold: domain_owner_retains_truth_authority=true, cross_namespace_write_default=DENY, fabric_can_mutate_truth=false.
- Industry consensus favors a shared file/Git layer with namespace isolation (Letta, OpenAI Agents SDK sessions/layouts, LangGraph Store namespaces, Claude memory tool); standalone memory platforms are anti-patterns (MemGPT/Letta pivot, OpenMemory retirement, Fowler Integration Database, mem0 #5151 shared graph-based agent memory poisoning).
- Recommended sequencing: Stage-1 shared data layer now; Stage-2 formal SHARED_INFRASTRUCTURE_PROFILE_TEAM; Stage-3 KG/graph service last and conditional on proven cross-member consistency needs, tenant isolation, and audit.

## 2. Current State Inventory

| Asset | Location | Scale | Status |
|---|---|---|---|
| HGK knowledge cluster | HGK SharedSpine (knowledge_fts, KnowledgeFactory, memory_records, kg_edges/kg_assertions) | 8 tables; 354 docs (FTS5); KnowledgeFactory 11 methods; CLI; 5 tests; 3 acceptance evidences | ACTIVE_REQUIRED; lexical/FTS-first; vector DEFERRED_SOURCE_BACKED; ERR_SOURCE_DRIFT blocks guard until re-ingest |
| FABRIC KB | FABRIC knowledge base | 9,698 md files | Live FABRIC knowledge asset under FABRIC governance |
| FAR tri-source retrieval | far_retrieval.py (L149-229) | KB_ROOTS 9/12 subroots; 2000-file/2MB cap; 103 qualified tests | Active; duplicates spine FTS via retrieve_memory() bypassing KnowledgeFactory |
| Governance slots | Fabric\control\KNOWLEDGE_POLICY.yaml; KG1_NAMESPACE_MODEL.json; A0_KNOWLEDGE_EXTENSION_EVIDENCE.yaml; HGK_STACK_MANIFEST.yaml | 4 pre-reserved slots; namespaces hgk/sqs/fabric/assurance/shared | Reserved, not yet activated; KG1 runtime validation gate defined |
| Profile teams | FDA/FAR precedents; Fabric\profiles\hgk-knowledge-factory | TEAM.md + governance/ + evidence/ + receipts/ + capability matrix + execution binding pattern | Established pattern; hgk-knowledge-factory exists as role-level distillation executor with empty skills/ |

## 3. Feasibility Assessment

Technical — extraction cohesion:
- The extraction surface is cohesive: one cluster (8 tables, 11-method KnowledgeFactory API, CLI, 5 tests, 3 acceptance evidences) with clear domain acceptance (RAG_KB_RUNTIME_ACCEPTANCE L3+L4, ten checks PASS).
- Data debt is the hard blocker: all 354 knowledge_docs canonical_path sources point to deleted SQS-THC directories; files now live in 知识库\HG-KSEOS_SSOT\RBWI_WP_CONTROL_PACK and 知识库\SQS-THC & TW-ICT_FSDT-Stack_SSOT. ERR_SOURCE_DRIFT cannot pass until re-ingest.
- Coupling is real but manageable: SQS data_plane imports KnowledgeFactory in 6 modules; HGK has ~10 reference points; FAR retrieve_memory() is a duplicate implementation to be converged.

Governance:
- Extraction = constitutional change → human two-key approval (DOC-01: each decision domain has ONE canonical owner; constitutional change requires two-key human approval).
- Feasible only as 'FABRIC shared capability substrate': heavy_stack=false, fabric.* candidate-only namespace, candidate_is_truth=false, provider_runtime_validation_gate=KG1.
- Three bottom lines: domain_owner_retains_truth_authority=true; cross_namespace_write_default=DENY; fabric_can_mutate_truth=false.
- Profile-team pattern exists (FDA/FAR): RP002_PROFILE_TEAM_MANIFEST additive, no fork; WO→CAPC→canary→dual-lane acceptance→freeze pipeline.

Industry:
- Mainstream shared agent knowledge = shared file/Git layer + namespace isolation (Letta shared-memory repositories, OpenAI Agents SDK sessions/layouts, LangGraph Store namespaces, Claude memory tool), not standalone memory platforms.
- Anti-patterns: MemGPT/Letta pivot to Git-file model; OpenMemory self-hosted platform retired; Fowler Integration Database anti-pattern; mem0 issue #5151 shared graph-based agent memory poisoning (high severity); platform team trap (build-it-and-they-won't-come).
- Hermes MemoryProvider ABC supports external providers (honcho/supermemory/mem0/openviking/retaindb/hindsight/holographic/byterover); only one external provider is active at a time — do not architect a multi-provider platform.
- Data-mesh federated governance: platform manages standards/pipelines; domains own content as products.
- Direction: ① shared data layer (Git KB + conventions + schema) first; ② governance first (federated); ③ KG/graph service last, only with proven cross-member consistency needs + tenant isolation + audit.

## 4. Recommended Architecture

Stage-1 — Shared data layer (NOW):
- Keep the work inside the existing Fabric\profiles\hgk-knowledge-factory profile and the FAR tri-source retrieval; no new platform.
- Re-ingest the stale index: repoint all 354 knowledge_docs canonical_path sources to the relocated SSOT directories (知识库\HG-KSEOS_SSOT\RBWI_WP_CONTROL_PACK; 知识库\SQS-THC & TW-ICT_FSDT-Stack_SSOT), rebuild FTS, and clear ERR_SOURCE_DRIFT.
- Converge retrieval: replace FAR retrieve_memory() FTS MATCH + LIKE fallback with KnowledgeFactory search so one spine retrieval path serves HGK/SQS/FAR/FDA cross-session sharing.
- Add shared conventions/schema for the shared Git KB layer (file layout, naming, ownership, namespace tagging).

Stage-2 — Formalize SHARED_INFRASTRUCTURE_PROFILE_TEAM:
- Follow the FDA/FAR precedent: TEAM.md + governance/ + evidence/ + receipts/ + capability matrix + execution binding + folder-reorganization receipt.
- Run the standard pipeline: WO→CAPC→canary→dual-lane acceptance→freeze; RP002_PROFILE_TEAM_MANIFEST additive, no fork.
- Bind the profile to heavy_stack=false, fabric.* candidate-only namespace, fabric_can_mutate_truth=false, cross_namespace_write_default=DENY.

Stage-3 — KG/graph service (conditional-last):
- Enable only with proven cross-member consistency needs + tenant isolation + audit; do NOT enable this round.
- Apply DOC-12 KG edge admission: schema-first; per-edge direct evidence locator + checker + effective interval; inferred vs source edges layered; high-risk edges require two independent sources or human approval.
- Enforce tenant isolation per DOC-11 (cross-tenant memory injection = poisoning incident).
- Disambiguate kg_edges/kg_assertions vs evidence_graph.py (EVO-005) before any graph work.

## 5. SoD Matrix

| Role | Responsibility | Boundaries |
|---|---|---|
| HGK governance | Truth authority for hgk.*; owns source_ledger/evidence_store/knowledge_fts; approves constitutional change (two-key human) | domain_owner_retains_truth_authority=true; truth authority not delegable |
| FABRIC substrate (profile team) | Operates shared infrastructure profile: standards, pipelines, hosting of shared capability; fabric.* candidate-only namespace | fabric_can_mutate_truth=false; cross_namespace_write_default=DENY; candidate_is_truth=false; no knowledge platform substitution |
| Domain owners (HGK/SQS/FAR/FDA) | Own content as products; consume shared substrate; retain canonical truth for their decision domain | One canonical owner per decision domain; writes confined to own namespace |
| Hermes | External memory provider adapter; one provider active at a time; memory_records lifecycle (remember/active_memory/revoke_memory) | Derived memory only; cannot replace canonical knowledge |
| oracle-AO | Runtime validation gate KG1; DOC-12 7-gate admission (identity→sanitation→rights/tenant→canonical state→segmentation/dedup→projection plan→checker admission) | MISSING_TOOL_ROW=FAIL_CLOSED; popularity cannot override hard gates; auto_promotion_from_agent_output=false |

## 6. Risks and Mitigations

- Constitutional boundary — extraction is a constitutional change. Mitigation: human two-key approval; DOC-01 invariant (no knowledge platform substitution; one canonical owner per decision domain).
- Truth drift — parallel retrieval paths diverge. Mitigation: Stage-1 retrieval API convergence onto KnowledgeFactory; single spine path; retire the raw-file scan duplicate.
- Owner contention — multiple domains sharing a namespace. Mitigation: namespace isolation; cross_namespace_write_default=DENY; federated data-mesh ownership.
- Qualification debt — unmapped gates accumulate. Mitigation: full qualification lifecycle (consumer_need→...→migration_rollback_exit); MISSING_TOOL_ROW=FAIL_CLOSED.
- Dual-stack split — raw-file KB scan vs FTS index drift. Mitigation: single retrieval path; stale-index re-ingest; ERR_SOURCE_DRIFT guard enforced.
- Promotion loop — agent output promoted to truth. Mitigation: auto_promotion_from_agent_output=false; CH-20 candidate-first (no direct write).
- Health responsibility — health must not collapse to a single score. Mitigation: multi-dimensional AssetHealthRecord (freshness/correctness/safety/usage/dependency_impact).
- Source-backed weakening — derived memory/KG mistaken for canonical. Mitigation: candidate_is_truth=false; per-edge direct evidence locators; ERR_SOURCE_DRIFT guard retained.

## 7. Non-Goals

- No second knowledge platform: the HGK knowledge cluster must not substitute for FABRIC KB.
- No standalone memory server/platform (industry anti-pattern).
- No vector DB enablement this round (vector backend stays DEFERRED_SOURCE_BACKED).
- No KG enablement this round (kg_edges/kg_assertions remain at 0 rows; Stage-3 conditional only).
- No truth transfer: fabric.* stays candidate-only; domain owners retain truth authority.
- No fork of existing profile manifests (RP002 additive only).

## 8. Evidence Trail

- WorkOrder: WO-HGK-KBUPGRADE-RESEARCH-001 (writer=codex).
- Board: HG-KSEOS governance; FABRIC blueprint RP002-PROFILE-TEAM-MANIFEST/1; SHARED_INFRASTRUCTURE_PROFILE_TEAM class; admission gates G0..R1.
- Research lanes (2026-08-14): Lane A folder audit; Lane B industry; Lane C governance.
- Governance slots: Fabric\control\KNOWLEDGE_POLICY.yaml (FABRIC-KNOWLEDGE-POLICY/1); Fabric\control\KG1_NAMESPACE_MODEL.json; Fabric\control\A0_KNOWLEDGE_EXTENSION_EVIDENCE.yaml; Fabric\control\HGK_STACK_MANIFEST.yaml.
- Profile: Fabric\profiles\hgk-knowledge-factory (role-level distillation executor; skills/ empty); FDA/FAR profile-team precedents.
- Retrieval code: far_retrieval.py (L149-229); duplicate graph facility evidence_graph.py (EVO-005).
- Relocated sources: 知识库\HG-KSEOS_SSOT\RBWI_WP_CONTROL_PACK; 知识库\SQS-THC & TW-ICT_FSDT-Stack_SSOT.
- Governance docs: DOC-01 (canonical knowledge; constitutional change), DOC-11 (memory four gates; cross-tenant injection), DOC-12 (grounded retrieval 7-gate admission; KG edge admission), DOC-20 (CH-20 candidate-first; AssetHealthRecord multi-dimensional).

---

## 8. CHALLENGE LANES (fresh-context independent verification)

### 8.1 Lane A — memory-full research (deleg_ebfeb0ea, 2026-08-14 11:43-11:46 UTC)
**CHALLENGE_VERDICT=PASS** — A1..A10 all PASS. Verified: config limits (2200/1375),
`flush_min_turns` dead key (0 .py references), no auto-compaction (docs + source),
apply_batch + 3-failure fuse (#42405), drift guard (#26045), session_search FTS5 free,
8 external providers. Findings (LOW, integrated): provider count 7→8 (supermemory);
"prefer session_search over raising limit" is researcher synthesis not verbatim docs;
frozen-snapshot means edits take effect next session.

### 8.2 Lane B — KB/memory/KG upgrade research (deleg_292ece9c, 2026-08-14 12:37-12:44 UTC)
**CHALLENGE_VERDICT=PASS** — A1..A10 all PASS. Verified: spine 5 tables (kg 0 rows);
KnowledgeFactory 10 methods; KNOWLEDGE_POLICY 3 keys + KG1 gate; hgk-knowledge-factory
profile dir; far_retrieval.py retrieve_memory L149-229 directly queries spine DB (no
KnowledgeFactory call — duplication CONFIRMED); sources 351/351 dead paths. Findings
(LOW, integrated): RAG acceptance 14/14 (not "ten"); 10 methods not 11; 4 test files
not 5; governance slot file locations corrected; debt more thorough than claimed.

---

## 9. RISKS & MITIGATIONS
| Risk | Mitigation |
|---|---|
| Constitutional boundary (extraction = constitutional change) | Human two-key approval; DOC-01 invariant |
| Truth drift (parallel retrieval paths diverge) | Stage-1 convergence onto KnowledgeFactory; retire raw-file scan duplicate |
| Owner contention (multi-domain shared namespace) | Namespace isolation; cross_namespace_write_default=DENY; federated data-mesh ownership |
| Qualification debt (unmapped gates) | Full qualification lifecycle; MISSING_TOOL_ROW=FAIL_CLOSED |
| Dual-stack split (KB scan vs FTS drift) | Single retrieval path; stale-index re-ingest; ERR_SOURCE_DRIFT enforced |
| Promotion loop (agent output → truth) | auto_promotion_from_agent_output=false; CH-20 candidate-first |
| Health responsibility ambiguity | Multi-dimensional AssetHealthRecord with owner + SLO per dimension |
| Source-backed weakening (derived mistaken for canonical) | candidate_is_truth=false; per-edge evidence locators; NO_SOURCE_NO_NORM |

---

## 10. GATE 2 — USER DECISIONS REQUESTED (COV-11-06 human gate; NOT self-approved)
1. Approve **P0** memory consolidation+prune execution (entry-by-entry removal list will be presented)?
2. Approve **Stage 1** (stale-index re-ingest + retrieval API convergence; no new infrastructure)?
3. Approve starting **Stage 2** governance formalization (SHARED_INFRASTRUCTURE_PROFILE_TEAM,
   constitutional two-key approval flow)?
4. Confirm **Stage 3 (KG)** stays conditional-last / not this round?
5. Keep memory_char_limit at 2200 (recommended)?

---

## 11. ARTIFACT INDEX (sha256 from final bytes; all frozen before this document was generated)
| artifact | bytes | sha256 |
|---|---|---|
| MEMORY_FULL_FAR_RESEARCH_EVIDENCE.md | 21204 | `49a874dce99ce7b4aea88eca9dcaf4de94d29dc93b89a1ea45c156863a4d8d54` |
| FABRIC_KB_UPGRADE_RESEARCH_EVIDENCE.md | 6547 | `87912f88f200526c589b19c302d82a011c03b0a3829527903fcc8f3ecde324ae` |
| M4_cross_analysis.md | 5807 | `efb78c90a4646d60680b851f2b413be94fb893bbf533d71fbe9a38bd25af9a1a` |
| M5_plan_hitl_draft.md | 5160 | `354d82e10ab1b82af9d550a712cc129b8f5a6830fcf78cbf5f852ac617686bea` |
| M8_fabric_retrieval_analysis.md | 5723 | `1721a6ceb2bfb8c540667df6304392db0586c9e81f702524c3b33a0caa2c1035` |
| K4_cross_analysis.md | 7980 | `0b913c3a342e376c9243cd522a901002035c90fec504138661e643f3a0f2a9d8` |
| K5_report_draft.md | 5290 | `ad6ee857598c3d81765ae63fa2357a7925f8c0a3da523996ed3602bcbfe4fa2a` |
| codex_output/memory_research_analysis.md | 9772 | `84078a9efe42747bc41ccb12a3f7578c72f595499fe551584624bf157c8c8e31` |
| codex_output/fabric_kb_upgrade_analysis.md | 12483 | `53a88b4e2afc743eea7b05de1cba545dad6871634e52384e00b6e048c3f8652d` |

---

## 12. NON-CLAIMS / STOP
- STOP: awaiting user HITL on §10. No self-approval of Gate 2.
- No migration executed; no truth transfer; no provider enablement; no vector/KG activation.
- Production / live-trading / remote-deployment: NOT claimed.
