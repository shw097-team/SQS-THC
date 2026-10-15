---
artifact_id: HGK_SQS_TWICT_MEMORY_KB_KG_MINIMAL_PATCH_20260811_R1
formal_name: HG-KSEOS、SQS-THC、TW-ICT_FSDT-Stack_記憶／知識庫／知識圖譜_最小修改方案
version: v2026.08.11-r1
generated_at: 2026-08-11T14:28:00+08:00
language: zh-TW
artifact_type: INTEGRATED_MINIMAL_PATCH_AND_IMPLEMENTATION_PLAN
task_kind: DESIGN
patch_mode: PRESERVE_EXTEND_BIND_NO_GREENFIELD_REBUILD
source_policy: FILES_FIRST_NO_SOURCE_NO_NORM_EXTERNAL_EVIDENCE_SUPPORT_ONLY
runtime_status: NOT_EXECUTED_BY_THIS_DOCUMENT
independent_acceptance_status: NOT_RUN
production_status: NOT_CLAIMED
---

# HG-KSEOS、SQS-THC、TW-ICT_FSDT-Stack
# 記憶／知識庫／知識圖譜最小修改方案
## v2026.08.11-r1

---

## 0. Executive Decision／最終工程裁決

本方案整合既有《「記憶／知識庫／知識圖譜」架構規劃_專業工程鑑定結論》與《工程鑑定結論&建議採用的最小修改方案》，並以現行 HG-KSEOS、SQS-THC、TW-ICT_FSDT-Stack、RBWI/WP/CONTROL 的既有 owner、truth-store、tool-admission 與 daily preflight 規則為硬邊界。

### 0.1 一句話方案

> **HG-KSEOS 繼續作為通用 Agent Engineering／Memory／Knowledge／RAG／KG substrate；SQS-THC／TW-ICT_FSDT-Stack 不重建第二套 Knowledge Platform，而以 PKG-DOC-14 與 TW-ICT knowledge objects 對 HG-KSEOS 做 financial-domain binding。Baseline 立即落地 SQLite + FTS5；Qdrant 與 Neo4j 立即完成 provider-specific「可安裝、可路由、可測、可卸載、可回滾」的 READY-TO-ACTIVATE 工程包，但 runtime 預設關閉；pgvector 僅在 PostgreSQL 因其他核心需求被正式採用時重新競標。**

### 0.2 必須保持的六項不變量

1. **Canonical Knowledge 不等於資料庫。**
   - Canonical knowledge = owner-bound Source / Git Markdown / Source Ledger / SourceCapsule / approved Memory artifact。
   - FTS、Vector、KG、GraphRAG 皆為 rebuildable projection。

2. **Memory 不得自動升格為 Financial Truth。**
   - Chat、LLM summary、retrieval result、agent observation 只能先成 `MemoryCandidate`。
   - 不得直接變成 `FinancialSpec`、`SetupQualification`、`RiskAuthorization`、`OrderIntent`。

3. **一個 Knowledge ownership，不新增第三套 SSOT。**
   - SQS/TW-ICT financial semantics 由其 domain owner 持有。
   - HG-KSEOS 提供 infrastructure/mechanics。
   - `Knowledge/AIKD/Grounding Owner` 負責 knowledge projection、grounding、memory candidate 與 KG edge。

4. **Fast Loop 不安裝、不升級、不重新綁定 provider。**
   - Fast Loop 只使用已 admission 的 CapabilityProfile。
   - 安裝／升級／provider change 一律走 Slow/Engineering Change。

5. **Deferred capability 必須 READY-TO-ACTIVATE，而不是「以後再研究」。**
   - 未啟用可以。
   - 沒有 install profile、adapter、route、test、rollback 不可以。

6. **RepoContext 未綁定前，不硬編 Windows 絕對路徑。**
   - 先固定 logical topology。
   - 真實 root/path 由 RepoContext → WorkspaceProfile 綁定並 readback。

---

# 1. Source Basis／本方案依據

## 1.1 直接整合來源

- 《「記憶／知識庫／知識圖譜」架構規劃_專業工程鑑定結論》
- 《工程鑑定結論&建議採用的最小修改方案》
- 《HG-KSEOS_實作前開發文檔包_v2026.08.06-r2》
- 《HG-KSEOS_藍圖_r2》
- 《HG-KSEOS_實作任務交接報告_v1_20260810》
- `SQS-THC_P0-CIP-PACK_v2026.08.06-r2`
- `SQS-THC_工程開發文檔`
- `TW-ICT_FSDT-Stack_P0-CIP-PACK_v2026.08.06-rFINAL-r2`
- `TW-ICT_FSDT-Stack_專業技術文檔`
- `SQS-THC_TW-ICT_FSDT-Stack_實作前開發文檔包_v2026.08.09-r2_G01/G02`
- `SQS-THC_TW-ICT_FSDT-Stack_RBWI_WP_CONTROL_PACK G01～G07 FULL GROUP r2`
- `TW-ICT_RBWI_v3.0.0_r2_2026-07-30`

## 1.2 已存在、不得重做的上游決策

### Knowledge owner / object family

現行 SQS/FSDT 已有：

- `SourceCapsule`
- `SourceLocator`
- `ClaimSourceMap`
- `KnowledgeRecord`
- `RetrievalReceipt`
- `MemoryCandidate`
- `KnowledgeGraphEdge`
- `GroundingReceipt`
- `SemanticFidelityScore`
- `AIKDBodyReceipt`

其 writer 維持：

> `Knowledge/AIKD/Grounding Owner`

### Physical truth-store topology

既有 local-first topology：

```text
single local process / CLI
├─ agentos_control.sqlite
├─ fsdt_financial.sqlite
├─ evidence/*.jsonl + index
├─ research.duckdb + Parquet
└─ knowledge_fts.sqlite
```

其中：

`knowledge_fts.sqlite = reviewed knowledge index / rebuildable`

### Daily runtime dependency

`SF-00` 使用：

- Hermes
- local spec store
- read-only WIKI adapter
- OpenTelemetry

且要求：

> `SF-16 preflight PASS`

### Tool-admission responsibility

既有 SF-16 責任鏈：

| Responsibility | Owner |
|---|---|
| Accountable | `ROLE-TOOL-OWNER` |
| Installer / capability maker | `ROLE-TOOL-CAPABILITY-MAKER` |
| Security / capability checker | `ROLE-SECURITY-TOOL-CHECKER` |
| Veto | `ROLE-SECURITY-VETO` |
| Human approver | `ROLE-PLATFORM-OPERATOR` |
| Preflight agent | `AGENT-LOCAL-PREFLIGHT` |
| Consumer | `SF-00 Runtime Owner` |

因此本方案**不新增新的 Tool Owner／Knowledge Owner／Runtime Owner**。

---

# 2. Gap Diagnosis／真正需要修的缺口

## 2.1 已閉合，不應重做

| Item | Verdict |
|---|---|
| Knowledge owner | CLOSED BY UPSTREAM DESIGN |
| Knowledge canonical/projection boundary | CLOSED |
| Memory candidate lifecycle | CLOSED AT DESIGN LEVEL |
| MVP store class | CLOSED: `knowledge_fts.sqlite` |
| Daily knowledge capability | CLOSED AT DESIGN LEVEL |
| SF-16 preflight responsibility | CLOSED |
| Tool install/admission responsibility | CLOSED |
| Financial truth isolation | CLOSED |
| KnowledgeGraphEdge schema-level capability | CLOSED |

## 2.2 真正缺口

| Gap | Severity | Required patch |
|---|---|---|
| Actual RepoContext / absolute paths 尚未綁定 | External binding gap | WorkspaceProfile 綁定 |
| FTS5 runtime install/admission 尚未實證 | P0 | Baseline construction + NRTV |
| HG-KSEOS ↔ PKG-DOC-14 binding adapter 尚未 materialize | P0 | Binding profile + adapters |
| Memory persistent read/write/promotion/forget readback 尚未閉合 | P0/P1 | Minimal memory artifact service |
| Vector provider-specific readiness 不足 | P1 | Qdrant prequalification pack |
| Graph provider-specific readiness 不足 | P1 | Neo4j GraphRAG prequalification pack |
| `DEFERRED` 狀態過粗 | P1 | Capability Readiness Matrix |
| Provider enable/disable route 未形成單一 machine-readable profile | P1 | Route + profile registry |
| Runtime NRTV / poisoning / stale / leakage 測試未全跑 | P0 | Test matrix + evidence |

---

# 3. Target Architecture／最小目標架構

```text
                     ┌─────────────────────────────┐
                     │ Canonical Domain Sources    │
                     │ Git / Source Ledger / Files │
                     └──────────────┬──────────────┘
                                    │
                                    ▼
                         ┌────────────────────┐
                         │ SourceCapsule      │
                         │ ClaimSourceMap     │
                         └─────────┬──────────┘
                                   │
                       owner review / grounding
                                   │
               ┌───────────────────┴───────────────────┐
               │                                       │
               ▼                                       ▼
       Git-approved Knowledge                    MemoryCandidate
       / approved memory artifact                artifact
               │                                       │
               └───────────────────┬───────────────────┘
                                   │
                                   ▼
                         knowledge_fts.sqlite
                         SQLite + FTS5
                         BASELINE / ACTIVE
                                   │
            ┌──────────────────────┼──────────────────────┐
            │                      │                      │
            ▼                      ▼                      ▼
       Lexical Search        Qdrant Projection      Neo4j Projection
       DEFAULT                DEFAULT OFF             DEFAULT OFF
       REQUIRED               READY-TO-ACTIVATE       READY-TO-ACTIVATE
            │                      │                      │
            └──────────────────────┼──────────────────────┘
                                   ▼
                         RetrievalPort / KGPort
                                   │
                                   ▼
                         RetrievalReceipt
                         GroundingReceipt
                                   │
                                   ▼
                          Hermes ContextPack
                                   │
                                   ▼
                  SQS/TW-ICT bounded agents/workflows
```

## 3.1 Architecture boundary

### HG-KSEOS owns

- General memory governance
- Knowledge ingestion mechanics
- SourceCapsule-compatible processing
- Retrieval adapters
- Memory candidate mechanics
- KG projection mechanics
- Provider lifecycle scaffolding
- Harness / evidence / rollback mechanics

### SQS-THC / TW-ICT FSDT owns

- Financial source semantics
- Financial ontology
- PIT / time / rights semantics
- Method / setup / risk / execution owner truth
- Financial knowledge publication rules
- Which knowledge can enter Daily/Weekly Context
- Financial-domain retrieval acceptance criteria

### Shared, but one writer only

- `KnowledgeRepositoryProfile`
- `CapabilityProfile`
- `RetrievalReceipt`
- `GroundingReceipt`
- `MemoryCandidate`
- `KnowledgeGraphEdge`

---

# 4. Physical Ownership／實體儲存與 namespace

## 4.1 Canonical knowledge

Canonical layer 不以 DB 為唯一真相：

```text
<repo-root>/
  knowledge/
    canonical/
      hg-kseos/
      sqs-thc/
      tw-ict-fsdt/
    source-ledger/
    source-capsules/
    memory/
      candidates/
      approved/
      tombstones/
```

> 上述是 logical path template；實際 absolute path 由 RepoContext 綁定。

### Writer rules

| Path family | Writer |
|---|---|
| `canonical/hg-kseos` | HG-KSEOS Knowledge Owner |
| `canonical/sqs-thc` | SQS Knowledge/AIKD/Grounding Owner |
| `canonical/tw-ict-fsdt` | TW-ICT domain Knowledge Owner |
| `source-ledger` | Source/Knowledge owner per source |
| `memory/candidates` | bounded agent may propose candidate |
| `memory/approved` | Knowledge Owner after promotion |
| `memory/tombstones` | Knowledge Owner / governance flow |

## 4.2 Projection stores

```text
<workspace-data>/
  knowledge/
    knowledge_fts.sqlite
    qdrant/              # optional provider data, not canonical
    neo4j/               # optional graph projection, not canonical
```

### `knowledge_fts.sqlite`

Required baseline.

Recommended tables:

- `source_capsule`
- `knowledge_record`
- `knowledge_fts` (FTS5)
- `claim_source_map`
- `memory_projection`
- `retrieval_receipt_index`
- `kg_edge_projection`
- `projection_generation`
- `invalidations`

No financial order/risk/execution truth is stored here as owner truth.

---

# 5. Memory System／最小記憶系統方案

## 5.1 不導入新的 all-in-one AI Memory Framework

本次不把下列任何一套升為 core：

- Mem0
- Zep
- Letta/MemGPT
- LangGraph Memory
- CrewAI Memory
- 任一 vendor-hosted shared semantic memory

理由：HG-KSEOS 與 SQS 已有 Memory Governance + `MemoryCandidate`；再引入新的 memory authority 會製造第三套 state/knowledge truth。

## 5.2 Memory types

沿用 HG-KSEOS：

- working
- episodic
- semantic
- procedural
- relational

## 5.3 Memory lifecycle

```text
Observation
→ MemoryCandidate
→ provenance check
→ scope check
→ privacy/security
→ dedup
→ contradiction
→ freshness / TTL
→ owner review / eval
→ VALIDATED / REJECTED
→ approved memory artifact
→ index projection
→ supersede / expire / tombstone
```

## 5.4 Minimal APIs

只要求薄介面，不造大型 memory server：

```text
memory.propose(candidate)
memory.get(id)
memory.search(query, scope)
memory.validate(id, evidence)
memory.promote(id, approval)
memory.expire(id, reason)
memory.supersede(old_id, new_id)
memory.forget(id, policy)
memory.readback(id)
```

### Security rule

- Retrieval 前先做 scope/access check。
- Multi-agent shared memory 預設 read-only snapshot。
- Agent write = candidate-only。
- Promotion 只能由 owner/gate。
- Forgetting 必須留下 tombstone / audit receipt。

---

# 6. Knowledge Retrieval／baseline 與 provider 選型

## 6.1 P0 Baseline — SQLite + FTS5

### Decision

`SQLite FTS5 = REQUIRED / DEFAULT_ENABLED`

### Required capabilities

- exact lexical search
- BM25/FTS retrieval
- source/owner/status filters
- exact locator return
- stale/expired exclusion
- deterministic rebuild
- backup/restore
- NRTV wrong-anchor rejection

### Daily use

SF-16 驗證：

- DB readable
- schema generation correct
- index generation matches approved source generation
- no stale/corrupt state
- read-only adapter works
- capability profile not expired

SF-00 只消費已通過的 read-only WIKI/knowledge capability。

---

# 7. Vector Retrieval／Qdrant vs pgvector

## 7.1 Final minimal-patch decision

### Qdrant

Target status:

> `PREQUALIFIED_DEFAULT_CANDIDATE / RUNTIME_DEFAULT_OFF`

不是 Daily baseline hard dependency，但**現在就必須完成 READY-TO-ACTIVATE 工程包**。

### pgvector

Target status:

> `CONDITIONAL_CANDIDATE / DO_NOT_PREINSTALL_UNLESS_POSTGRESQL_ADOPTED`

只有當 PostgreSQL 因其他核心需求被正式採用，才重新與 Qdrant 做 ADR/benchmark。

## 7.2 Qdrant readiness package

必須在 production go-live 前完成：

1. provider identity / version pin
2. license/security record
3. Windows-compatible install profile
4. optional Docker profile
5. local service healthcheck
6. collection schema
7. namespace rules
8. metadata/source/owner filters
9. `RetrievalPort` adapter
10. golden retrieval corpus
11. FTS5 vs Qdrant benchmark
12. wrong-source / wrong-anchor negative test
13. poisoned embedding/document test
14. stale/deleted source propagation
15. snapshot backup
16. restore drill
17. uninstall
18. residue scan
19. admission receipt
20. enable/disable route

## 7.3 Enable gate

Qdrant 只有在下列條件成立時才能從 `ADMITTED_DISABLED` 升至 `PROFILE_ENABLED`：

```text
FTS5 evaluation below preregistered threshold
AND semantic retrieval gives material improvement
AND latency/cost/resource budget passes
AND grounding / provenance does not regress
AND backup/restore passes
AND security gate passes
AND Human/Platform approval exists
```

---

# 8. Knowledge Graph／Neo4j 最小方案

## 8.1 Schema first, DB second

現有 `KnowledgeGraphEdge` 保持 canonical contract。

最小 edge：

```yaml
edge_id:
namespace:
subject:
predicate:
object:
source_locator:
source_hash:
valid_from:
valid_to:
confidence:
review_status:
owner:
supersedes:
```

先允許其 projection 落在 SQLite/JSONL。

## 8.2 Neo4j target status

> `P1_GRAPH_PROVIDER_CANDIDATE / PROFILE_READY / RUNTIME_DEFAULT_OFF`

不設為 baseline always-on service。

## 8.3 現在必須先做的工程

即使不啟用 DB，也必須先完成：

- `GraphRetrievalPort`
- `KnowledgeGraphEdge → provider projection` mapping
- schema/constraint definition
- namespace isolation
- provenance query
- multi-hop fixtures
- source delete/supersede cascade
- graph rebuild
- graph corruption recovery
- adapter disable
- provider uninstall
- residue test
- readiness receipt

## 8.4 Install/enable trigger

只有以下 use case 真的被證明：

- multi-hop relation retrieval
- lineage traversal
- entity relationship exploration
- graph analytics
- relation-dense queries where FTS/vector underperform

才允許實際 install/admit Neo4j provider。

Graph output 永遠不能反寫 canonical source truth。

---

# 9. Capability Readiness State Machine／必新增的最小控制

現有 `DEFERRED` 太粗，新增以下狀態但不新增新的 authority plane：

```text
DECLARED
→ PROVIDER_SELECTED
→ INSTALL_PROFILE_READY
→ SANDBOX_QUALIFIED
→ INSTALLED_DISABLED
→ ADMITTED_DISABLED
→ PROFILE_ENABLED
→ ACTIVE
→ DEGRADED
→ REVOKED
→ UNINSTALLED
```

## 9.1 State semantics

| State | Meaning |
|---|---|
| DECLARED | 只有 capability contract |
| PROVIDER_SELECTED | 已選具名 provider |
| INSTALL_PROFILE_READY | pin/install/config/uninstall recipe 完整 |
| SANDBOX_QUALIFIED | smoke/functional/negative/security 通過 |
| INSTALLED_DISABLED | 已安裝但不在 runtime route |
| ADMITTED_DISABLED | 已通過 admission，但 default off |
| PROFILE_ENABLED | 某 WorkspaceProfile 授權啟用 |
| ACTIVE | 本 Run SF-16 驗證成功 |
| DEGRADED | fallback route |
| REVOKED | 禁用且不得 route |
| UNINSTALLED | 卸載與 residue readback 完成 |

## 9.2 Required registry row

```yaml
capability_id:
provider_id:
version:
pin:
license:
install_profile:
adapter:
routes:
default_state:
allowed_profiles:
healthcheck:
functional_tests:
negative_tests:
security_tests:
parity_tests:
backup_restore:
uninstall:
residue_check:
fallback:
rollback:
owner:
installer:
checker:
veto:
human_approver:
last_qualified_at:
expires_at:
evidence_refs:
```

---

# 10. Routing／啟用路由

## 10.1 Retrieval route

```text
query
→ access/scope check
→ lexical FTS5
→ score/evidence sufficiency check
   ├─ sufficient → return grounded result
   └─ insufficient
        ├─ Qdrant profile ACTIVE → hybrid/semantic retrieval
        └─ Qdrant inactive → abstain / manual / TT
→ relation-heavy?
   ├─ Neo4j profile ACTIVE → GraphRetrievalPort
   └─ inactive → no graph escalation
→ exact-anchor grounding
→ RetrievalReceipt
```

## 10.2 No silent escalation

禁止：

- FTS5 搜不到 → 自動下載 Qdrant
- Vector 結果不好 → 自動安裝 Neo4j
- Graph 有 edge → 視為 canonical fact
- Provider unavailable → 改用未 admission 的 cloud RAG

---

# 11. RBWI Integration／與 TW-ICT_RBWI v3 的接合

## 11.1 SF-16

只做：

- capability/version/hash/config readback
- license/security/permission
- health
- profile state
- expiry
- fallback availability

不做：

- install
- upgrade
- provider selection
- schema migration
- benchmark

### SF-16 output additions

`CapabilityProfile` 增加：

```yaml
knowledge:
  fts5: ACTIVE|DEGRADED|BLOCKED
  vector: DISABLED|ACTIVE|DEGRADED
  graph: DISABLED|ACTIVE|DEGRADED
  knowledge_generation:
  source_generation:
  grounding_policy:
  last_nrtv_receipt:
```

## 11.2 SF-00

保持：

> WIKI read-only

新增硬規則：

- only consume `SF-16 ACTIVE/DEGRADED` knowledge profile
- DEGRADED 不得提高 claim
- vector/graph inactive 不構成 error，除非本 Run TaskSpec 明確 requires capability
- unknown capability → WAIT / manual fallback / BLOCK according to task criticality

## 11.3 Daily Fast Loop

Daily Fast Loop 不需要知道 Qdrant/Neo4j 產品名。

只看 capability：

- `CAP-KNOWLEDGE-LEXICAL`
- `CAP-KNOWLEDGE-SEMANTIC`
- `CAP-KNOWLEDGE-GRAPH`

避免 workflow 與 provider 綁死。

---

# 12. Slow/Engineering Change／工具安裝與變更流程

```text
Capability gap / benchmark finding
→ ChangeRequest
→ ToolDecision
→ provider select
→ install profile
→ sandbox install
→ adapter bind
→ smoke
→ functional
→ negative/edge/adversarial
→ security
→ parity
→ backup/restore
→ uninstall/residue
→ independent check
→ admission
→ ADMITTED_DISABLED
→ WorkspaceProfile approval
→ PROFILE_ENABLED
→ next Run SF-16
```

Fast Loop 不得插入這條流程。

---

# 13. Roles & RACI／不新增角色，只綁既有角色

| Work | A | R | C/Veto | Human |
|---|---|---|---|---|
| Knowledge policy | Knowledge Owner | Knowledge maker | Security / Evidence | Product/Domain authority as required |
| FTS5 install | ROLE-TOOL-OWNER | ROLE-TOOL-CAPABILITY-MAKER | ROLE-SECURITY-TOOL-CHECKER | ROLE-PLATFORM-OPERATOR |
| Qdrant prequalification | ROLE-TOOL-OWNER | capability maker + adapter implementer | Security + Independent checker | Platform operator |
| Neo4j prequalification | ROLE-TOOL-OWNER | capability maker + graph adapter implementer | Security + Independent checker | Platform operator |
| Daily preflight | ROLE-RUNTIME-OWNER | AGENT-LOCAL-PREFLIGHT / Runtime operator | Security Tool Checker | Human operator |
| Memory promotion | Knowledge Owner | proposer | independent/knowledge checker | Human when policy requires |
| Financial promotion | Financial owner | domain maker | Risk/Evidence veto | Financial Human authority |

---

# 14. Windows / Local-first Implementation Profile

## 14.1 Required baseline

Clean-machine construction wave 必須有：

- Python/runtime prerequisites as already defined by host pack
- SQLite available
- FTS5 capability check
- `knowledge_fts.sqlite` bootstrap
- migration command
- rebuild command
- backup command
- restore command
- NRTV command
- health command

## 14.2 Suggested logical commands

以下為 **contract names**，實際 path/CLI 在 RepoContext 後 materialize：

```text
knowledge doctor
knowledge rebuild --provider fts5
knowledge query --provider fts5 --require-anchor
knowledge backup
knowledge restore --verify
knowledge nrtv

provider qdrant install --profile local
provider qdrant qualify
provider qdrant disable
provider qdrant uninstall --residue-check

provider neo4j qualify-profile
provider neo4j install --when-approved
provider neo4j disable
provider neo4j uninstall --residue-check
```

本文件不宣稱這些 commands 已存在；它們是後續實作的 bounded command contract。

---

# 15. Tests / Acceptance／最小但完整的驗收矩陣

## 15.1 P0 FTS5 tests

1. correct file + correct anchor
2. correct file + wrong anchor → FAIL
3. stale source excluded
4. superseded source excluded/repointed
5. revoked source excluded
6. namespace isolation
7. permission scope
8. rebuild parity
9. backup/restore parity
10. deterministic query fixture
11. injection in source treated as DATA
12. memory candidate not promoted to financial truth

## 15.2 Memory tests

1. task-local working memory does not leak
2. semantic candidate missing provenance → reject
3. stale memory → expire
4. conflicting memory → hold
5. PII/secret → quarantine/redact
6. cross-agent write → candidate-only
7. promotion requires owner
8. forgetting creates tombstone
9. supersession invalidates old projection
10. retrieval before access check → fail

## 15.3 Qdrant prequalification

- install/readback
- schema/filter
- hybrid/dense/sparse as applicable
- source locator retention
- wrong-anchor rejection
- stale delete/update propagation
- benchmark vs FTS5
- latency/resource
- poisoned document/metadata
- snapshot
- restore
- disable
- uninstall
- residue

## 15.4 Neo4j prequalification

- edge provenance
- constraints
- multi-hop correctness
- source delete cascade
- supersession
- stale edge
- graph rebuild
- no-source edge reject
- GraphRAG result grounding
- graph output cannot promote financial truth
- disable
- uninstall/residue

---

# 16. Promotion Thresholds／避免工具為裝而裝

## 16.1 Vector enable criteria

至少預先登錄：

- retrieval precision / anchor correctness
- recall on known semantic paraphrases
- abstention correctness
- latency budget
- memory footprint
- rebuild duration
- backup/restore RTO
- false-positive tolerance

只有相對 FTS5 有**實質、可重現**改善才 enable。

## 16.2 Graph enable criteria

至少需要：

- relation-heavy query set
- multi-hop benchmark
- source provenance correctness
- graph-specific gain over FTS5/Qdrant
- acceptable maintenance/rebuild cost

未達門檻維持 `ADMITTED_DISABLED` 或 `PROFILE_READY`。

---

# 17. Minimal Patch Set／只修改必要工件

本方案不新增新的 PKG-DOC，也不改四 truth plane。

## PATCH-MEM-01 — HG-KSEOS Knowledge/Memory Profile

位置：
- PRE-19 Context Engineering and Memory Governance
- PRE-20 Grounded Retrieval、RAG、KB、KG and GraphRAG
- Provider/Capability Registry

新增：
- `SQS_TWICT_KNOWLEDGE_PROFILE`
- namespace contract
- KnowledgeRepositoryProfile
- Qdrant/Neo4j readiness lifecycle
- no financial authority statement

## PATCH-MEM-02 — SQS PKG-DOC-14

新增：
- HG-KSEOS substrate binding
- namespace mapping
- canonical vs projection store table
- MemoryCandidate artifact persistence rule
- RetrievalPort / GraphRetrievalPort
- no silent provider escalation

## PATCH-MEM-03 — G02 Tool Decision Ledger

修正：

### TD-018

由：

`DEFER_BENCHMARK`

細化為：

`QDRANT_PREQUALIFICATION_REQUIRED / DEFAULT_OFF / ENABLE_ON_BENCHMARK_GATE`

### pgvector

新增條件：

`P2_CONDITIONAL_IF_POSTGRESQL_ADOPTED`

### TD-019

由：

`DEFER_ROUTE_OUT_MVP`

細化為：

`NEO4J_GRAPHRAG_PROFILE_READY / DEFAULT_OFF / INSTALL_ON_GRAPH_GATE`

## PATCH-MEM-04 — Capability Readiness Matrix

在 G02 / RBWI-WP-Control 加：

- capability state machine
- provider-specific readiness
- install/admission evidence
- default enable policy
- expiry
- rollback/uninstall

## PATCH-MEM-05 — TW-ICT RBWI SF-16/SF-00

只補：

- lexical/vector/graph capability state
- knowledge generation/readback
- fallback
- no install in Fast Loop

不改原 SF flow。

## PATCH-MEM-06 — Windows Install Profile

增加：

- FTS5 baseline
- Qdrant prequalification profile
- Neo4j profile-ready recipe
- uninstall/residue
- backup/restore
- clean-machine test

## PATCH-MEM-07 — Assurance/NRTV

加入：

- knowledge anchor NRTV
- memory scope/leak tests
- vector poisoning
- graph provenance
- source supersession/rebuild
- cross-store authority mutation tests

---

# 18. Work Packages／最小施工順序

## WP-MEM-00 — RepoContext & Binding

Outputs:

- repo root
- data root
- knowledge paths
- existing HG-KSEOS runtime readback
- existing memory/knowledge APIs
- existing SQLite/FTS capabilities
- current provider state

Gate:

`REPO_CONTEXT_BOUND`

## WP-MEM-01 — FTS5 Baseline

Outputs:

- knowledge_fts.sqlite
- schema
- SourceCapsule indexer
- RetrievalPort
- rebuild
- backup/restore
- NRTV

Gate:

`LEXICAL_KNOWLEDGE_BASELINE_PASS`

## WP-MEM-02 — Memory Binding

Outputs:

- MemoryCandidate persistence
- promotion/expire/supersede/forget
- HG-KSEOS↔SQS adapter
- scope/permission
- tests

Gate:

`MEMORY_GOVERNANCE_RUNTIME_PASS`

## WP-MEM-03 — Qdrant Prequalification

Outputs:

- provider lock
- install profile
- adapter
- benchmark
- security
- backup/restore
- uninstall
- admission

Target end state:

`ADMITTED_DISABLED`

Gate:

`SEMANTIC_PROVIDER_READY`

## WP-MEM-04 — Neo4j Profile Readiness

Outputs:

- graph adapter
- schema mapping
- fixtures
- provider install/uninstall recipe
- qualification plan

Target end state before actual graph need:

`INSTALL_PROFILE_READY` or `SANDBOX_QUALIFIED`

If graph trigger passes:

`ADMITTED_DISABLED`

Gate:

`GRAPH_PROVIDER_READY`

## WP-MEM-05 — RBWI Integration

Outputs:

- SF-16 profile fields
- SF-00 consumer rules
- fallback
- no-fast-loop-install test

Gate:

`DAILY_PREFLIGHT_KNOWLEDGE_PASS`

## WP-MEM-06 — Independent NRTV

Outputs:

- independent test evidence
- rollback drill
- stale/poisoning/leakage fixtures
- provider disable test

Gate:

`INDEPENDENT_KNOWLEDGE_NRTV_PASS`

---

# 19. Handoff Artifacts／施工交付物

最低需要以下 artifacts：

```text
knowledge/
  KNOWLEDGE_REPOSITORY_PROFILE.yaml
  MEMORY_GOVERNANCE_PROFILE.yaml
  RETRIEVAL_PORT.schema.json
  GRAPH_RETRIEVAL_PORT.schema.json
  CAPABILITY_READINESS_MATRIX.yaml

providers/
  qdrant/
    provider.yaml
    install-profile.yaml
    qualification.yaml
    uninstall.yaml
  neo4j/
    provider.yaml
    install-profile.yaml
    qualification.yaml
    uninstall.yaml

windows/
  KNOWLEDGE_BASELINE_INSTALL.md
  QDRANT_PREQUALIFICATION.md
  NEO4J_PROFILE_READY.md

tests/
  knowledge/
  memory/
  qdrant/
  neo4j/

evidence/
  knowledge/
  provider-admission/
```

實際路徑由 target repo context 對應；以上是邏輯工件集。

---

# 20. Failure / Degrade / Rollback

| Failure | Degrade | Forbidden |
|---|---|---|
| FTS5 corrupt | restore/rebuild；必要時 BLOCK knowledge-dependent run | fabricate result |
| WIKI unavailable | local pinned knowledge | free web/RAG substitute without admission |
| Qdrant unavailable | FTS5 | auto-install/auto-cloud |
| Neo4j unavailable | FTS5/Qdrant + no graph claim | infer missing graph relation |
| memory stale/conflict | exclude/hold | silent merge |
| source revoked | invalidate all projections | retain stale “known fact” |
| adapter mismatch | last-known-good profile | silent schema coercion |
| security issue | revoke provider | downgrade to warning |
| backup restore fail | block promotion | continue as if recoverable |

---

# 21. Definition of Done

本最小修改方案只有在以下條件成立時，才可宣稱「Memory/KB/KG integration implementation candidate complete」：

1. RepoContext 真實綁定完成。
2. HG-KSEOS current memory/knowledge API readback 完成。
3. PKG-DOC-14 binding materialize。
4. `knowledge_fts.sqlite` 可建立、查詢、重建、備份、還原。
5. SF-16 能辨識 knowledge capability 狀態。
6. SF-00 只使用 admitted read-only profile。
7. MemoryCandidate promotion/forget/supersede 可驗證。
8. Qdrant provider-specific readiness pack 完整，至少到 `ADMITTED_DISABLED` 前所需工程已完成。
9. Neo4j Graph profile 至少完成 `INSTALL_PROFILE_READY`；若 trigger 已成立則完成 admission。
10. 所有 negative/security/NRTV fixture 通過。
11. uninstall/residue/rollback readback 完成。
12. Independent Checker 完成 subject-bound evidence。
13. 不存在 Memory/Vector/KG 反向取得 Financial/Control/Execution authority。
14. Runtime/Paper/Shadow/Production claim 仍依各自 gate，不由本方案自動升格。

---

# 22. Recommended Final Decision／建議定案

## P0 — 現在就落地

- HG-KSEOS substrate reuse
- SQS/TW-ICT namespace binding
- Git/source-ledger canonical knowledge
- SourceCapsule
- KnowledgeRecord
- MemoryCandidate
- `knowledge_fts.sqlite`
- SQLite FTS5
- RetrievalPort
- exact-anchor grounding
- SF-16 / SF-00 integration
- NRTV / backup / restore

## P1 — 現在就做 READY-TO-ACTIVATE，不預設啟用

### Qdrant
- provider pin
- install/uninstall
- adapter
- benchmark
- security
- backup/restore
- admission
- default OFF

### Neo4j / GraphRAG
- provider shortlist
- install profile
- GraphRetrievalPort
- edge projection
- benchmark fixtures
- rebuild/uninstall
- default OFF

## P2 — 條件式

### pgvector
只有 PostgreSQL 因其他核心需求被採用時才啟動 ADR/benchmark。

---

# 23. Claim Ceiling

本文件是：

> **AUTHOR_SIDE_INTEGRATED_MINIMAL_PATCH_AND_IMPLEMENTATION_PLAN**

它不證明：

- target Windows machine 已安裝 SQLite/Qdrant/Neo4j
- HG-KSEOS persistent memory service 已完成
- Qdrant/Neo4j 已 admission
- Independent NRTV 已執行
- Production 已可用

直到實際 repo/runtime/evidence readback 完成之前：

```text
DESIGN_READY
IMPLEMENTATION_NOT_EXECUTED_BY_THIS_DOCUMENT
PROVIDER_ADMISSION_NOT_CLAIMED
INDEPENDENT_NRTV_NOT_RUN
PRODUCTION_NOT_CLAIMED
```

---

# 24. Machine-readable Decision Summary

```yaml
decision:
  reuse_hg_kseos: true
  greenfield_knowledge_platform: false

canonical_knowledge:
  type: git_source_ledger_source_capsule
  db_is_ssot: false

baseline:
  sqlite: REQUIRED
  fts5: REQUIRED_DEFAULT_ENABLED
  knowledge_store: knowledge_fts.sqlite

memory:
  external_memory_framework_core: false
  model: HG_KSEOS_MEMORY_GOVERNANCE_PLUS_SQS_MEMORYCANDIDATE
  agent_direct_promotion: false

vector:
  primary_candidate: qdrant
  target_state: ADMITTED_DISABLED
  runtime_default: false
  enable_gate: FTS5_BENCHMARK_INSUFFICIENT_AND_QDRANT_MATERIAL_GAIN
  pgvector:
    status: CONDITIONAL
    condition: POSTGRESQL_ADOPTED_FOR_OTHER_CORE_NEED

graph:
  primary_candidate: neo4j_graphrag
  runtime_default: false
  minimum_pre_go_live_state: INSTALL_PROFILE_READY
  enable_gate: RELATION_DENSE_MULTI_HOP_BENCHMARK_MATERIAL_GAIN

fast_loop:
  install_allowed: false
  provider_upgrade_allowed: false
  preflight_only: true

slow_loop:
  provider_install: true
  provider_upgrade: true
  benchmark: true
  admission: true

owners:
  knowledge: Knowledge/AIKD/Grounding Owner
  tool: ROLE-TOOL-OWNER
  installer: ROLE-TOOL-CAPABILITY-MAKER
  security_checker: ROLE-SECURITY-TOOL-CHECKER
  veto: ROLE-SECURITY-VETO
  platform_approver: ROLE-PLATFORM-OPERATOR
  runtime_consumer: SF-00 Runtime Owner
```

---

## End of document
