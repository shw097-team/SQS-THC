# you asked

message time: 2026-08-11 11:49:25

任務目標：
你必須針對目前「HG-KSEOS蜂群/KANBAN/多智能體能力」  ，提出符合上游文件設計原意、符合最佳工程評估的自進化方案，並且要和「gstack」的多智能體分工流水線達成良好合作。

任務要求：
你必須針對任務目標，和全部相關資料進行「專業分析+交叉比對+深度整合」，再逐項對任務目標進行大數據搜索"2026年8月8日"以後的最新資料，搜索相關主題的「技術社群論壇(如HuggingFace / GitHub)、網站、專欄、部落格、專業研究」，並對搜索資料進行「專業分析+交叉比對+深度整合」，再逐項對任務目標進行符合「工程專業實務作法、技術社群成熟技術者共識、不自己造輪子、導入現有最新熱門方法/教程」的最佳工程評估、設計規劃、補充、勘誤，並且避免過度工程化。

---

# chatgpt response

# 1. Reuse Plan｜總體工程裁決與自進化方向

針對目前 **HG-KSEOS 蜂群／Kanban／多智能體能力**，我建議的下一階段不是把系統改造成「預設全蜂群」，而是建立一個**窄範圍、可驗真的 Governed Evolution ChangeSet**：

> **`HGK-MAS-EVO-002 — Deterministic Parallel Admission + Hermes Swarm Qualification + Codex Subagent Route Qualification + gstack Review-Army Cooperation`**

核心裁決是：

> **保留既有「Single-Agent Default → deterministic admission → bounded parallelism」架構；補強的是「該平行時真的平行、該單工時仍單工」，以及把 gstack 的 specialist review 多智能體能力放到正確的 review/advisory 層，而不是再造第四個 orchestrator。**

目前 Reference Project-001 已經證明 Hermes Kanban 能真實運作，但最新 WAVE3 evidence 的 G4 明確是 `KANBAN_SINGLE + CODEX_BOUNDED`，並沒有證明 multi-worker fan-out/join 或 genuine Codex child-agent runtime；因此真正缺的是 **parallel topology qualification**，不是 Kanban 有無問題。

這與上游 P0-CIP / deterministic admission原意一致：Hermes應是唯一 global durable runtime orchestrator；Codex subagents只服務單張 Coding Card；gstack是 review/QA/security/release-readiness advisory，最後仍回 HG-KSEOS independent checker與 reducer。

建議的最終架構如下：

```text
User
Goal / Source / Constraints
        │
        ▼
HG-KSEOS Normative / Governance Plane
Authority
Source Admission
Requirement / ADR
TaskSpec / WorkOrder
Risk / HITL
Evidence Contract
        │
        ▼
Topology Selector v2
        │
        ├── DIRECT
        │
        ├── Hermes delegate_task
        │        short / read-heavy fork-join
        │
        ├── KANBAN_SINGLE
        │        durable but non-parallel
        │
        └── KANBAN_DAG / HERMES SWARM
                 independent parallel work
                 │
                 ├── read/research worker
                 ├── test/analysis worker
                 └── Coding Card
                        │
                        ▼
                    Codex Main
                    SOLE WRITER
                     ├── subagent: explore
                     └── subagent: test/triage
                        │
                        ▼
                     WorkResult
                        │
                        ▼
                 gstack selected stage
          plan-eng-review / review / qa / cso
                 specialist micro-swarm
                        │
                        ▼
                 EvidenceCandidate
                        │
                        ▼
              HG-KSEOS Independent Checker
                        │
                        ▼
                    Reducers
                        │
                        ▼
                   Delivery
```

這仍是：

> **Hierarchical Bounded Orchestration**

而不是：

> `Hermes swarm × Codex swarm × gstack swarm = swarm-of-swarms`。

---

# 2. Evidence｜上游設計與 2026-08-08 後最新資料交叉鑑定

## 2.1 Hermes：應充分利用原生 Swarm，但不能打開無治理 auto-decompose

Hermes目前官方 Kanban已明確區分兩種 primitive：

- `delegate_task`：短生命週期 fork→join；
- Kanban：durable queue/state machine，支援 named profiles、restart、handoff、audit與多 agent生命週期。官方工程範例直接包含「parallel worktrees → review → iterate」。([GitHub](https://github.com/nousresearch/hermes-agent/blob/main/website/docs/user-guide/features/kanban.md))

更重要的是，目前 Hermes CLI 已經原生提供：

> `hermes kanban swarm`

其 primitive就是：

> **parallel workers → verifier → synthesizer**。([GitHub](https://github.com/NousResearch/hermes-agent/blob/main/hermes_cli/kanban.py))

因此 HG-KSEOS **完全沒有理由自己重新寫 swarm scheduler**。

但我仍不建議把現行：

```yaml
auto_decompose: false
```

改回 Hermes預設 `true`。

因為官方 current Kanban確實預設 `auto_decompose:true`，會讓 decomposer自動根據 profile roster產 JSON task graph、分配 child tasks並觸發 dispatch。([GitHub](https://github.com/nousresearch/hermes-agent/blob/main/website/docs/user-guide/features/kanban.md))

而就在 **2026-08-09**，Hermes官方 repo出現一個很關鍵的實際問題：assigned Kanban task可能很快被 dispatcher執行，而 mutating assignment缺乏 operator audit；side-effectful worker也可能在缺乏額外 authorization gate的情況下啟動，auto-decomposer所產 child task同樣受影響。([GitHub](https://github.com/NousResearch/hermes-agent/issues/82689))

所以 HG-KSEOS現行：

```text
HGK admission
→ approved WorkOrder
→ Hermes runtime
```

不是保守過頭，而是**必要治理邊界**。

### 裁決

保持：

```yaml
auto_decompose: false
```

但增加：

> **HGK-controlled decomposition / swarm admission adapter**

而不是開啟 Hermes raw autonomous decomposition。

---

## 2.2 Hermes還需要一個很薄的 liveness guard

另一個 **2026-08-09** Hermes issue指出，task可能已經顯示：

```text
status = running
```

但：

```text
worker_pid = NULL
heartbeat = NULL
log = absent
```

結果 crash recovery可能數小時才發現；官方 issue甚至給出的現行 workaround也是偵測這個 signature後呼叫 Hermes既有 `kanban reclaim`。([GitHub](https://github.com/NousResearch/hermes-agent/issues/82622))

這對 HG-KSEOS很重要。

因為日後從：

```text
1 worker
→ 3 parallel workers
```

後，ghost worker風險會增加。

### 不應做

不要重寫 Hermes dispatcher。

### 應做

在 HG-KSEOS adapter旁增加一個**薄型 runtime liveness gate**：

```text
claimed/running
     │
     ▼
PID?
heartbeat?
log/runtime evidence?
     │
 ┌───┴────┐
YES       NO
 │         │
continue   grace window
           │
           ▼
     official reclaim
           │
           ▼
       bounded retry
```

只使用 Hermes現有 reclaim/retry能力。

---

## 2.3 Codex：現在最需要的是「能力探針」，不是直接假定 subagents可用

OpenAI current Codex官方 guidance非常符合 HG-KSEOS現有設計：

> subagents最適合先用在 **exploration、tests、triage、summarization等 read-heavy工作**；parallel write-heavy需要更謹慎，因為會增加 conflict與 coordination overhead。([OpenAI Developers](https://developers.openai.com/codex/agent-configuration/subagents))

所以：

```text
Codex Main = sole writer
Subagents = mostly read-only
```

這條上游原設計應該保留。

問題是 HG-KSEOS目前不是單純跑 first-party Codex route，而是既有：

```text
Codex
→ OpenCodex
→ OpenCode Go
→ deepseek-v4-flash
```

且現行規劃要求不 silent fallback至 OpenAI。

這時 **2026-08-10** Codex剛好出現數個非常相關的新 issue。

其中 custom `model_providers.*` 路徑被回報存在：

- reasoning可以正常；
- server-side multi-agent未必可用；
- client multi-agent可能只有部分功能；
- 甚至可能 silent single-agent；
- first-party ChatGPT path與regular API-key provider行為不一致。([GitHub](https://github.com/openai/codex/issues/37858?utm_source=chatgpt.com))

同日另一個 issue甚至重現 `spawn_agent` 成功建立 child agent，但 task message沒有真正到達 subagent context。([GitHub](https://github.com/openai/codex/issues/37822?utm_source=chatgpt.com))

這些 issue **不能證明 DeepSeek/OpenCode Go現在一定壞掉**。

但足以證明：

> **HG-KSEOS不能把「Codex支援subagents」當成 current provider route已資格化。**

另外還有 0.147.0 subagents完成後殘留 MCP helper process的回報；這同樣應作 process-hygiene regression，而不是直接認定本機有bug。([GitHub](https://github.com/openai/codex/issues/37870))

---

## 2.4 gstack：最新 upstream反而支持「不要另造 swarm」

HG-KSEOS目前 local certified gstack定位非常合理：

- `office-hours`
- `plan-eng-review`
- `review`
- `qa`
- `cso`
- `ship`
- `retro`

而且 gstack output只是 `EvidenceCandidate / advisory`；`ship`不是 ReleaseReducer、`review`不是 independent checker、`cso`不是 HGK security authority。

最新 upstream current main的 `Review Army` 已經在做實際 specialist parallel review：按變更內容選 specialist，再將 selected specialists平行 dispatch，最後合併 findings。([GitHub](https://github.com/garrytan/gstack/blob/main/ship/sections/review-army.md))

更值得注意的是，gstack自己的 TODO對 generic reusable swarm abstraction寫得很保守：

> 先從具體 `/ship` use case取得經驗，等至少兩個 consumer真正暴露共用需求後再抽象，而且明確要求避免 premature abstraction。([GitHub](https://github.com/garrytan/gstack/blob/main/TODOS.md))

這幾乎直接回答 HG-KSEOS該怎麼做：

> **不要把 gstack的 Review Army重新實作成 HG-KSEOS自己的 GenericSwarmEngine。**

另外目前 gstack main對 Hermes integration仍定位為 methodology artifacts，並引導使用 `bun run gen:skill-docs --host hermes`，而不是提供另一個 global orchestration daemon。([GitHub](https://github.com/garrytan/gstack/blob/main/setup))

因此：

```text
Hermes = execution swarm
gstack = review swarm methodology
```

正是目前最適當的責任切割。

---

# 3. Implementation Recipe｜建議的完整自進化方案

## Phase 0 — Freeze current Reference Project baseline

不要先改 code。

先封存目前：

```text
HGK HEAD = 60820e5
G4 topology = KANBAN_SINGLE + CODEX_BOUNDED
SQS suite = 211/211
HGK suite = 245/245
```

作為性能與可靠度比較 baseline。現有 r2 evidence已證明這次 G4沒有 genuine swarm/subagent runtime。

目的不是證明現在很差，而是之後回答：

> 「增加 multi-agent究竟有沒有真的變快／變好？」

---

## Phase 1 — 不改架構，先資格化三個現有 primitive

### 1A. Hermes Swarm Canary

直接利用 upstream現有：

```text
Hermes Kanban
Hermes kanban swarm
delegate_task
dependency graph
reclaim/retry
verifier
synthesizer
```

不得另寫 scheduler。

最小 canary：

```text
Root
├─ READ-A
├─ READ-B
└─ READ-C
    ↓
Verifier
    ↓
Synthesizer
```

驗：

```text
3 real worker IDs
concurrent overlap
heartbeats
dependency/join
result handoff
verifier
synthesizer
```

---

### 1B. Codex exact-route Subagent Capability Probe

對 **現在真正使用的 Codex/OpenCodex/OpenCode Go/DeepSeek V4 Flash route** 跑：

```text
Codex Main
├─ Subagent-A: read-only repo/data investigation
└─ Subagent-B: read-only tests/log triage
       ↓
parent receives A+B
       ↓
synthesis
```

必須實際取得：

```text
parent thread id
child A id
child B id
child task payload
provider/model identity
child outputs
join/synthesis
writes by children = 0
process cleanup
```

只有如此才：

```text
CODEX_NATIVE_SUBAGENT_ROUTE = QUALIFIED
```

否則：

```text
CODEX_NATIVE_SUBAGENT_ROUTE = DEGRADED
```

**禁止 silent switch provider/model。**

---

### 1C. gstack Review Army Host Qualification

現行 gstack pin不要因 upstream main有新功能就直接升級。

先對目前 pinned gstack做：

```text
selected review skill
→ Hermes discovers
→ actual invocation
→ specialist selection
→ parallel specialist execution?
→ findings merge
→ typed EvidenceCandidate
```

若 current pinned/Hermes host不能真正 native spawn specialist：

**不要偽造 Review Army PASS。**

走下面 fallback：

```text
gstack
= determines review methodology / specialist roles

HG-KSEOS
= admits review work

Hermes
= runs temporary read-only review workers

gstack
= synthesis/advisory semantics

HGK
= final checker
```

仍然沒有新 orchestrator。

---

# Phase 2 — `Topology Selector v2`

這是我認為**唯一真正值得修改的 HG-KSEOS核心點**。

現有 policy不應砍掉，只補 execution classification。

### Stage A — DIRECT vs durable

```text
atomic
single role
no durable handoff
no restart requirement
no dependency graph
→ DIRECT
```

短 read-heavy、parent要拿答案回來繼續：

```text
→ HERMES delegate_task
```

需要持久狀態、跨角色、restart、HITL、handoff：

```text
→ KANBAN_SINGLE
```

Hermes官方本身就是這樣區分 `delegate_task`與 Kanban。([GitHub](https://github.com/nousresearch/hermes-agent/blob/main/website/docs/user-guide/features/kanban.md))

---

### Stage B — KANBAN_SINGLE vs KANBAN_DAG

只有全部滿足才 fan-out：

```text
parallelizable child work >= 2
child scopes can be isolated
write conflicts absent or strictly partitioned
join predicate exists
cancel propagation exists
verifier exists
single synthesizer exists
coordination cost < expected gain
```

否則：

```text
KANBAN_SINGLE
```

這正是現有 HG-KSEOS admission原意，不需要創造新的 policy DSL。

---

### Stage C — Codex subagent admission

```text
coding_card = true
AND
parallelizable read-heavy child problems >= 2
AND
native subagent capability probe = PASS
AND
children do not require second writer

→ CODEX_SUBAGENTS
```

否則：

```text
CODEX_MAIN_ONLY
```

關鍵改變在於：

> 不再只是 `subagents_allowed=true`

而是對符合條件的 Card由 TaskSpec/AGENTS/Skill明確投影：

```text
SUBAGENT_EXECUTION_EXPECTED
```

然後驗實際 runtime。

---

# Phase 3 — Concurrency budget先不要放大

現有 pilot budget方向是正確的：

```text
max active Kanban cards ≈ 3
Codex subagents / Card ≤ 2
same worktree writers = 1
nesting depth = 1
```



我不建議現在就：

```text
8 workers
16 subagents
depth 3
```

現在還沒有證據證明那有收益。

另外現行：

```yaml
max_in_progress_per_profile: 1
```

會造成同一 profile工作序列化。

但也**不要直接改成 unlimited**。

最佳做法是：

> 優先 reuse目前 approved profiles；若沒有適合的 read-only worker，再最多補 2 個穩定 specialist profile。

例如：

```text
hgk-read-analyst
hgk-test-analyst
```

而不是每個專案臨時創建十幾個 persona。

---

# Phase 4 — gstack分工流水線正式接入

建議把 gstack合作方式固定成：

| 工程階段 | 全域Owner | gstack角色 | Multi-agent方式 |
|---|---|---|---|
| ambiguity | HGK | office-hours advisory | 通常單 agent |
| engineering plan | HGK | plan-eng-review | specialist advisory |
| implementation | Hermes + Codex | 不搶 writer | Hermes DAG / Codex |
| code review | HGK | gstack review | Review Army / micro-swarm |
| runtime QA | HGK | gstack qa | conditional |
| security | HGK | gstack cso | specialist review |
| release readiness | HGK | gstack ship | advisory only |
| learning | HGK GE | gstack retro | GapSignal candidate |

這沿用現有 deterministic named-method router，不讓 LLM臨時猜。

### 最重要的控制邊界

```text
gstack specialist
≠ Kanban WorkOrder authority

gstack finding
≠ acceptance PASS

gstack ship
≠ release

gstack review army
≠ independent checker
```

所以完整流程應是：

```text
Hermes worker(s)
      ↓
Codex implementation
      ↓
focused tests
      ↓
gstack Review Army
      ↓
EvidenceCandidate
      ↓
HGK Independent Checker
      ↓
affected regression
      ↓
Reducer
```

這樣 gstack多智能體是真正有價值的「第二意見層」，而不是第二個 project manager。

---

# Phase 5 — Reference Project-001 真實 swarm stress canary

我建議**不要再造一個假 benchmark**。

直接 reuse目前 `DSV-2026-08-11-r1` 和已經執行過的 G4同類 workload。

舊版：

```text
one Codex worker
→ coverage
→ calendar
→ anomaly
→ SQL
→ volume semantics
→ corporate actions
→ PIT
```

新版 canary：

```text
G4-ROOT
│
├─ G4-A
│  Calendar / coverage / session
│  READ ONLY
│
├─ G4-B
│  Corporate actions / discontinuities
│  READ ONLY
│
├─ G4-C
│  SQL / PIT / OHLC / Volume integrity
│       │
│       ▼
│   Codex Main
│   ├─ subagent SQL/schema
│   └─ subagent test/data triage
│
└─────────────┐
              ▼
          JOIN
              │
              ▼
         Synthesizer
              │
              ▼
       gstack review
       Review Army
              │
              ▼
    Independent Checker
```

其中刻意注入一次：

```text
one child fail
```

驗：

```text
retry / reclaim
resume
no duplicate effect
join waits correctly
```

再刻意 interrupt一次，驗：

```text
checkpoint
→ restart
→ durable continuation
```

這才是 Reference Project真正應有的 swarm acceptance。

---

# Phase 6 — 不只看 PASS，要和舊 G4比較效益

這一步很重要。

**不要把「spawn出3個 agent」當成功指標。**

要比較同一 frozen DatasetVersion、相同目標下的：

| Metric | 舊 KANBAN_SINGLE | 新 Parallel |
|---|---:|---:|
| wall-clock time | baseline | measured |
| worker active overlap | 1 | measured |
| dispatch/join overhead | baseline | measured |
| token/model usage | baseline | measured |
| tool calls | baseline | measured |
| defect/anomaly recall | baseline | measured |
| false-positive findings | baseline | measured |
| retry/recovery time | baseline | measured |
| double writer | 0 | 必須 0 |
| evidence completeness | baseline | 不得下降 |

Promotion不應要求：

> 「一定比較快」。

而應要求：

> **耗時下降，或缺陷發現/驗證品質提升，且 coordination/security/evidence沒有退化。**

如果 multi-agent：

```text
慢了 25%
token 多 2 倍
品質沒提升
```

那 Topology Selector下次就應選 single。

這才是真正會「自進化」的 admission policy，而不是迷信 swarm。

---

# 4. Governance｜Promotion、Evidence與防過度工程

## 建議只修改四個 affected surface

整個自進化 ChangeSet最好控制在：

1. **既有 Topology/Admission Router的小幅擴充**
2. **WorkOrder → Hermes swarm/delegate thin binding**
3. **Codex exact-route subagent capability gate**
4. **gstack EvidenceCandidate / review micro-swarm binding**

不要新增：

```text
SwarmDB
AgentGraphDB
new task protocol
new orchestration DSL
new generic agent framework
new event bus
new scheduler
new evidence framework
```

這與 gstack自己「先具體use case，晚一點才抽generic swarm」的 current upstream思想一致。([GitHub](https://github.com/garrytan/gstack/blob/main/TODOS.md))

---

## Hermes安全補強只做 adapter guard

受 8/9 issue影響，我建議額外加入兩個薄 gate：

```text
PRE_DISPATCH:
sensitive side effect?
→ HGK risk / HITL / permission admitted?

POST_DISPATCH:
running?
→ PID/heartbeat/runtime/log proof within grace?
```

若 ghost：

```text
→ official reclaim
→ bounded retry
```

不要 fork Hermes自行修 dispatcher。

---

## Codex明確三態

不要只有：

```text
SUPPORTED / UNSUPPORTED
```

應採：

```text
QUALIFIED
DEGRADED
UNAVAILABLE
```

例如 current DeepSeek/OpenCode route如果：

```text
subagent spawn = works
message delivery = works
join = works
provider identity = correct
cleanup = works
```

才：

```text
QUALIFIED
```

若任一核心功能失敗：

```text
DEGRADED
```

Fallback：

```text
Hermes delegate_task
or
Hermes read-only Kanban workers
```

Codex Main仍做 sole writer。

---

## gstack也採兩種 runtime mode

```text
GSTACK_NATIVE_SPECIALIST_PARALLEL
```

若 current host真正支援。

否則：

```text
GSTACK_METHODOLOGY_ON_HERMES_WORKERS
```

即：

> gstack選 methodology / review role，Hermes提供 runtime worker。

這比重新造一個 gstack swarm adapter framework更薄。

---

## Governed Evolution正式流程

這輪仍應完全走既有：

```text
observe
→ gap
→ FIT-GAP
→ candidate
→ sandbox
→ positive
→ negative
→ security
→ holdout
→ NRTV
→ independent checker
→ policy gate
→ canary
→ rollback
→ promotion
```

而不是因為這份分析直接修改 current active baseline。這也是目前 HG-KSEOS既有 Governed Evolution contract。

---

## 最終 acceptance invariants

建議至少要求：

```text
double_writer = 0
second_orchestrator = 0
unauthorized_effect = 0
duplicate_effect = 0
lost_handoff = 0
stale_lease_unrecovered = 0
secret_cross_profile = 0
release_authority_escape = 0
unbounded_agent_recursion = 0
silent_provider_fallback = 0
kanban_done_without_runtime_evidence = 0
gstack_final_authority = 0
```

以及能力結果必須明確：

```text
HERMES_REAL_FANOUT_JOIN =
PASS | FAIL

CODEX_GENUINE_SUBAGENT_RUNTIME =
PASS | DEGRADED_CURRENT_PROVIDER | FAIL

GSTACK_REVIEW_ARMY_RUNTIME =
PASS_NATIVE
| PASS_HERMES_BACKED
| DEGRADED_NATIVE_REVIEW

REFERENCE_PROJECT_SWARM_STRESS =
PASS | FAIL
```

---

# 5. If-No-Fit｜最終規劃與不適用時的降級策略

## 我建議的施工順序

```text
E0
Freeze current 60820e5 / Wave3 evidence baseline
        ↓
E1
Hermes swarm primitive qualification
        ↓
E2
Codex exact DeepSeek/OpenCode subagent probe
        ↓
E3
gstack specialist-review capability probe
        ↓
E4
Minimal Topology Selector v2 patch
        ↓
E5
deterministic routing regression
        ↓
E6
Reference Project G4 swarm canary
        ↓
E7
gstack Review Army cooperation
        ↓
E8
failure / reclaim / restart / rollback stress
        ↓
E9
single-vs-parallel performance comparison
        ↓
E10
Independent acceptance
        ↓
E11
Governed Evolution promotion decision
```

### 只有 E1～E3證明 upstream primitive真的缺能力

才考慮 adapter。

不是先寫 adapter再找用途。

---

## 最終工程裁決

我會把 HG-KSEOS下一階段多智能體目標從：

> 「把更多任務改成蜂群。」

修正成：

> **「讓 deterministic admission具有可靠的 parallelism calibration，能自動選擇 DIRECT / delegate_task / KANBAN_SINGLE / KANBAN_DAG / Codex subagents / gstack specialist review，並用真實 Reference Project evidence證明選擇具有收益。」**

其中責任分配固定為：

```text
HG-KSEOS
= WHY / WHETHER / AUTHORITY / ACCEPTANCE

Hermes
= DURABLE WHO / WHEN / DEPENDENCY / RETRY

Codex Main
= CODE WRITER

Codex subagents
= CARD-LOCAL READ-HEAVY HELPERS

gstack
= SPECIALIST REVIEW / QA / SECURITY ADVISORY

HG-KSEOS Checker/Reducer
= FINAL VERDICT
```

這是目前最符合上游設計原意，也最符合 2026-08-09～08-11 最新 Hermes/Codex/gstack實務訊號的方案：Hermes已經有成熟 swarm primitive，不應重造；Codex subagents值得用，但你的 custom provider route必須先資格化；gstack Review Army值得導入，但 upstream自己都還避免過早抽象 generic swarm，因此 HG-KSEOS更不應另外建一套。([GitHub](https://github.com/NousResearch/hermes-agent/blob/main/hermes_cli/kanban.py))

所以這次建議的變更是**窄、深、可實證**的：

> **升級 Topology Selector，而不是升級 agent 數量；整合 gstack Review Army，而不是讓 gstack接管 orchestrator；資格化 Codex subagents，而不是假定 provider支援；重用 Hermes swarm，而不是自己造 swarm engine。**

這會是目前 `HG-KSEOS Reference Project-001` 最值得進入下一個 Governed Evolution candidate 的項目。

---
Powered by [AI Exporter](https://saveai.net)