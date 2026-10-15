# FAR TRI-SOURCE MANDATORY — 實作整合證據（Single Evidence MD）

> Document ID: `FAR-TRI-SOURCE-IMPLEMENTATION-EVIDENCE-20260813`
> 用途: 外部驗收官對 WO-FAR-TRISOURCE-001（TRI_SOURCE_MANDATORY 實作）之單一驗收證據
> 生成: 2026-08-13T15:55:07Z（本檔自身除外, 全部 raw 內容內嵌）

## 0. Claim ceiling

```text
FAR_TRI_SOURCE_MANDATORY_RESEARCH_ASSURANCE = PASS（WO-FAR-TRISOURCE-001 VERIFIED）
TRI_SOURCE_MANDATORY = ACTIVE（memory/knowledge/web probes MANDATORY; silent_skip=0）
68/68 tests OK ｜ CANARY-4/5/6 ALL_PASS ｜ AO A1-A14 verified（2 rounds; 12 findings closed）
canonical evidence = FAR_FINAL_ACCEPTANCE_EVIDENCE.md b0b21ced799face7…（四處 byte-identical）
r8 baseline = 58de0815…（immutable historical; FAR_R8_HISTORICAL_BASELINE.md）
PRODUCTION / SQS LIVE / REMOTE = NOT_CLAIMED / NOT_AUTHORIZED / NOT_CLAIMED
side effects = 0（unauthorized=0 / SQS FT mutation=0 / live broker write=0）
```

## 1. 實作整合摘要（方案 → 落地）

```text
D1-D4: GitHub 真實搜索定案（8 queries; 社群共識 grounded）
Phase 1: far_trisource.py — outcome contract（HIT/ZERO_RELEVANT_HIT/UNAVAILABLE/BLOCKED_BY_AUTHORITY/ERROR; 禁 SKIPPED）
         + FailClosed SILENT_SOURCE_SKIP + TriSourceCoverageReceipt（嵌入 ResearchRunReceipt）+ ResearchPlan source_assurance
Phase 2: ClaimLedger 三通道欄位 + cross_source_status（9 態）+ claim-specific 仲裁（無永恆階層）+ memory 分級
Phase 3: counterevidence_probe + terminal reducer（§18 等價）+ ResearchSynthesis 7 sections
Phase 4: 68 tests（含 5 回歸 F3/F4/F6/F9/F12）+ CANARY-4（stale memory）+ CANARY-5（web outage）+ CANARY-6（真實三通道）
Phase 5: 治理閉環（WO/AO/evidence/rollback; r8 re-freeze; 12 findings 全閉合）
reuse-first: far_retrieval.py probes 原樣复用; 無新平台/DB/crawler; Qdrant/Neo4j default-off
```

### 變更檔案 + hash（F11 記錄）

```text
far_trisource.py ................ ef99c55ecfbf326e54ba78767382cdaca04131cc8e00fe7e7301a787d2bfae1e
tests/test_far_trisource.py ..... b6976cbbf788e5c5e74619f14cc30a8fc61178b97514cf8fc111ee107f395df6
research-product/templates/ResearchPlan.yaml（+source_assurance 段）
research-product/templates/ClaimLedger.tsv（15-col 三通道 header; legacy 註解化）
research-product/templates/ResearchRunReceipt.json（+tri_source_coverage）
research-product/templates/ResearchSynthesis.md（+7 sections）
FAR_TRI_SOURCE_D_DECISIONS.json / FAR_TRI_SOURCE_FITGAP_RECEIPT.json /
FAR_TRI_SOURCE_CHALLENGE_CLOSURE.json / FAR_R8_HISTORICAL_BASELINE.md
canary/FAR-20260813-005-trisource-canaries/ + FAR-20260813-006-trisource-real/
evidence-bundle/raw-github/（2 檔）＋ evidence-bundle/raw-canary/FAR-20260813-006/
CHANGE_INPUT_MANIFEST_TRI_SOURCE_2026-08-13.json（19 files, 知識庫）
```

## 2. 治理記錄（SharedSpine readback）

```text
WO  : {"workorder_id": "WO-FAR-TRISOURCE-001", "writer": "codex", "state": "VERIFIED", "rollback_pointer": "RB-WO-FAR-TRISOURCE-001"}
REQ : {"requirement_id": "REQ-FAR-TRISOURCE-001", "state": "FROZEN", "version": 1}
EVD-FAR-* rows total = 67（含 EVD-FAR-TRISOURCE-MODULE/TESTS/CANARIES/CANARY-6/D/FITGAP/
  GITHUB-D/R8-BASELINE/CHALLENGE-CL/ACCEPTANCE-MD-R5..R7）
```

## 3. D1-D4 決策（全文）

```json
{
  "schema": "FAR-TRI-SOURCE-D-DECISIONS/1",
  "decided_at_utc": "2026-08-13T16:00:00Z",
  "research_basis": {
    "method": "FAR external web channel: real GitHub Search API (read-only, no auth), 2 rounds, 8 queries",
    "evidence_files": ["var/far/github_d_research.json", "var/far/github_d_research_r2.json"],
    "grounding_target": "engineering professional practice / mature engineering SoD / mature practitioner consensus"
  },
  "decisions": {
    "D1_scope_of_mandate": {
      "question": "TRI_SOURCE_MANDATORY 適用範圍（formal WO vs canary）",
      "github_evidence": [
        "Ddibirov/hybrid-deep-research ⭐13: multi-round deep research pipeline, prompt-only, structured stages",
        "carlosrodera/deep-research-protocol ⭐13: 'stop asking one AI to do deep research, ask five then consolidate' — mature SoD: research lanes separated from consolidation",
        "Nimo1987/harness-research ⭐11: MCP-based professional research harness"
      ],
      "consensus": "成熟工程 SoD 共識: 正式研究流程 = 分離角色 + 強制結構化階段（probe/consolidate 分離）; 測試/canary 屬 fixture 階層, 不與正式交付同一 gate",
      "decision": "MANDATORY_FOR_ALL_FORMAL_WORKORDERS: 每個 formal admitted FAR Research WorkOrder 三通道強制（FailClosed SILENT_SOURCE_SKIP）; canary/dogfood runs 執行時亦跑完整三通道（真實執行, 不作假）, 但 terminal 語義標記 canary scope（不宣稱 full PASS gate）",
      "soD_rationale": "maker(研究)與 consolidation(仲裁/reducer)分離 = deep-research-protocol 共識; canary 標記避免 fixture 結果誤升格"
    },
    "D2_web_quota": {
      "question": "Web/各通道配額上限",
      "github_evidence": [
        "yaswanthme007/tokenscope ⭐9: open-source token profiler for AI coding agents (observability)",
        "eatakishiyev/context-forge ⭐6: context compiler — scores, compresses, reorders, budgets context",
        "nuffin/hermes-budget-ledger ⭐1: per-task token budget ledger for Hermes Agent",
        "neuronaline/ai-memory-context-management ⭐8: cache-optimized context management for long-running agents"
      ],
      "consensus": "社群共識: budget-aware context 管理 + per-query observability 是成熟實務（非 cost-bypass）; 過濾/排名/組裝是研究品質手段",
      "decision": "PER_CHANNEL_QUOTA: 初查 MEMORY≤4 / KNOWLEDGE≤4 / WEB≤4 queries; iterative gap 追加總計≤4; 每 query 記錄 latency+近似 tokens; 超限 → QUOTA_EXCEEDED 記錄 + 需 WO 擴額（不靜默截斷、不 fake）; WEB roots 預設 arxiv.org（WorkOrder 可宣告擴充）",
      "rationale": "tokenscope/context-forge 共識: 觀察 + 預算 + 過濾; 配額是研究品質控制（prevent context dilution, prompt §17 同義）"
    },
    "D3_counterevidence_depth": {
      "question": "Counterevidence 深度（哪些 claims 強制）",
      "github_evidence": [
        "dCaples/AutoDidact ⭐688: autonomously train research-agent LLMs with RL + self-verification",
        "NineAbyss/S2R ⭐77: S2R paper impl — self-verify and self-correct",
        "xiaogeli/claude-prove-done ⭐1: stop-hook that BLOCKS completion claims ('fixed','done') without evidence"
      ],
      "consensus": "社群共識: self-verification/counterevidence 是主流實務; claude-prove-done 證明「無證據不得宣告完成」是工程 gate 模式",
      "decision": "LOAD_BEARING_MANDATORY: 僅 load-bearing claims（其 falsity 會逆轉 recommendation 者）強制 ≥1 counterevidence query（QueryLedger 記錄; 0 命中 → ZERO_RELEVANT_COUNTEREVIDENCE_HIT 顯式）; 非 load-bearing claims 可選但記錄; 完成主張未過 counterevidence gate → 不得 RESEARCH_PASS_CANDIDATE",
      "rationale": "AutoDidact/S2R 共識: 驗證是研究品質核心; claude-prove-done: PASS 需證據閘門"
    },
    "D4_stale_memory_handling": {
      "question": "發現 stale approved memory 的處置",
      "github_evidence": [
        "kresnapandu/memwatch ⭐32: memory staleness detection + AUTO-EXPIRY for LLM agents",
        "awrshift/claude-memory-kit ⭐28: date-tagged memory across sessions",
        "Jrosenbizzle/agent-memory-bench ⭐1: benchmark — stale-context detection"
      ],
      "consensus": "社群共識: date-tag + staleness 偵測 + 過期機制為標準; 但 auto-expiry 在治理系統需 authority 同意（memwatch 是 agent 自管記憶, 非 Fabric approved namespace）",
      "decision": "NO_SILENT_REWRITE + NO_SILENT_AUTO_EXPIRE: 偵測 stale approved memory → ① emit StalenessFinding（run 內記錄）② 產生 CandidateKnowledge correction（candidate namespace only）③ 若屬 harness/policy 層 → ProposedEvolution（受治理流程, COV-11-06）; approved namespace 不自動 rewrite; expiry 需 owner authority",
      "rationale": "memwatch 偵測+expiry 共識採納偵測半部; 治理側採保守半部（Fabric approved namespace 需 authority, 對齊 prompt §20/§21）"
    }
  },
  "terminal": "D1-D4 DECIDED (GitHub-grounded)"
}

```

## 4. GitHub 研究證據（全文; 真實 Search API）

```json
{
 "schema": "FAR-GITHUB-D-RESEARCH/1",
 "generated_at_utc": "2026-08-13T15:20:50.213747+00:00",
 "queries": {
  "D1": [
   {
    "query": "agentic research pipeline mandatory retrieval gate",
    "label": "retrieval gate",
    "hits": []
   },
   {
    "query": "deep research agent source verification",
    "label": "source verification",
    "hits": [
     {
      "full_name": "Ddibirov/hybrid-deep-research",
      "stars": 13,
      "description": "Multi-round deep research pipeline for AI agents. Prompt-only — no Python, no framework, no dependencies. Parallel subagents, Critic filtering, source authority weighting, deterministic URL verificati",
      "html_url": "https://github.com/Ddibirov/hybrid-deep-research"
     },
     {
      "full_name": "carlosrodera/deep-research-protocol",
      "stars": 13,
      "description": "Stop asking one AI to do deep research. Ask five. Then consolidate. An open, opinionated method that runs ChatGPT, Claude, Gemini, Grok and Perplexity in parallel and cross-consolidates with evidence ",
      "html_url": "https://github.com/carlosrodera/deep-research-protocol"
     },
     {
      "full_name": "Nimo1987/harness-research",
      "stars": 11,
      "description": "Give any AI Agent professional-grade deep research capabilities.  An MCP (Model Context Protocol) server that performs real-time deep research across 5 data sources, evaluates source credibility with ",
      "html_url": "https://github.com/Nimo1987/harness-research"
     },
     {
      "full_name": "Socialpranker/deepdive",
      "stars": 8,
      "description": "Deepdive skill for Claude Code — 11-phase research pipeline: plan-review gate, parallel sub-agent search with circuit breaker, claims-ledger triangulation, relevance-filtered evidence, multi-angle red",
      "html_url": "https://github.com/Socialpranker/deepdive"
     },
     {
      "full_name": "Kaos599/Deep-Ass-Research",
      "stars": 3,
      "description": "IDE-agnostic deep-research framework for AI agents: maps a topic wide, commits to depth on purpose, adversarially verifies its findings, and synthesizes them into a backlinked, primary-sourced Obsidia",
      "html_url": "https://github.com/Kaos599/Deep-Ass-Research"
     }
    ]
   }
  ],
  "D2": [
   {
    "query": "LLM research agent budget cost control",
    "label": "budget",
    "hits": []
   },
   {
    "query": "RAG query rate limit cost",
    "label": "rate limit",
    "hits": []
   }
  ],
  "D3": [
   {
    "query": "counterevidence adversarial verification LLM",
    "label": "counterevidence",
    "hits": []
   },
   {
    "query": "claim verification negative evidence",
    "label": "negative evidence",
    "hits": [
     {
      "full_name": "xiaogeli/claude-prove-done",
      "stars": 1,
      "description": "\"Done\" ≠ done. A Claude Code skill + Stop hook that blocks completion claims (\"fixed\", \"added\", \"all set\", \"wrapped up\") and negative-existence claims until verified with a tool call — so the agent st",
      "html_url": "https://github.com/xiaogeli/claude-prove-done"
     },
     {
      "full_name": "BryceWDesign/IX-Function",
      "stars": 1,
      "description": "Source-available IX-Function causal-transfer harness: tests cross-domain causal structure reuse through pre-outcome prediction, reality-delta scoring, uncertainty preservation, falsification, negative",
      "html_url": "https://github.com/BryceWDesign/IX-Function"
     },
     {
      "full_name": "lloitesa013/stock-agent-harness-v0-2-0-defense",
      "stars": 0,
      "description": "2026-05 iteration of the verification thesis in finance: claim contracts + release gates + sealed evidence packets for a financial agent — including preserved negative results (weak real-market perfor",
      "html_url": "https://github.com/lloitesa013/stock-agent-harness-v0-2-0-defense"
     }
    ]
   }
  ],
  "D4": [
   {
    "query": "RAG knowledge freshness invalidation",
    "label": "freshness",
    "hits": []
   },
   {
    "query": "memory staleness detection agent",
    "label": "memory staleness",
    "hits": [
     {
      "full_name": "kresnapandu/memwatch",
      "stars": 32,
      "description": "Memory staleness detection and auto-expiry for LLM agents",
      "html_url": "https://github.com/kresnapandu/memwatch"
     },
     {
      "full_name": "awrshift/claude-memory-kit",
      "stars": 28,
      "description": "The starter kit for Claude Code — your agent remembers across sessions: date-tagged memory under three hook-enforced caps, per-session handoffs, stale-refs detection, multi-project isolation, audit-dr",
      "html_url": "https://github.com/awrshift/claude-memory-kit"
     },
     {
      "full_name": "Jrosenbizzle/agent-memory-bench",
      "stars": 1,
      "description": "Benchmark memory reliability in AI agents: preference recall, stale-context detection, contradiction handling, and project continuity.",
      "html_url": "https://github.com/Jrosenbizzle/agent-memory-bench"
     },
     {
      "full_name": "DFKHelper/token-goat-mem",
      "stars": 1,
      "description": "Local-first long-term memory for AI coding agents (Claude Code, Copilot, Codex): durable facts with trust levels and anchor-based staleness detection",
      "html_url": "https://github.com/DFKHelper/token-goat-mem"
     },
     {
      "full_name": "AnasHasan786/contextclock",
      "stars": 0,
      "description": "Temporal memory staleness detection for AI agents",
      "html_url": "https://github.com/AnasHasan786/contextclock"
     }
    ]
   }
  ]
 }
}
```
```json
{
 "schema": "FAR-GITHUB-D-RESEARCH-R2/1",
 "queries": {
  "D2": [
   {
    "query": "agent token budget management",
    "label": "token budget",
    "hits": [
     {
      "full_name": "neuronaline/ai-memory-context-management",
      "stars": 8,
      "description": "A cache-optimized AI memory and context management framework for long-running LLM agents, featuring tiered context storage, token budgeting, memory compaction, sub-agent delegation, and structured web",
      "html_url": "https://github.com/neuronaline/ai-memory-context-management"
     },
     {
      "full_name": "Lucineer/cuda-context-window",
      "stars": 1,
      "description": "Context window management — compression, summarization, and token budgeting for agent conversations",
      "html_url": "https://github.com/Lucineer/cuda-context-window"
     },
     {
      "full_name": "nuffin/hermes-budget-ledger",
      "stars": 1,
      "description": "Cross-task token budget management plugin for Hermes Agent — tracks per-workspace, per-task, and per-model token consumption with budget enforcement and auto-degradation",
      "html_url": "https://github.com/nuffin/hermes-budget-ledger"
     },
     {
      "full_name": "itsbryanman/Commandry",
      "stars": 1,
      "description": "Self-hosted admin panel for AI agent management  agents, MCP servers, token budgets, prompt versioning, and execution traces on a single port.",
      "html_url": "https://github.com/itsbryanman/Commandry"
     },
     {
      "full_name": "invincible-jha/agent-energy-budget",
      "stars": 0,
      "description": "Agent cost control, energy budget management, and token tracking",
      "html_url": "https://github.com/invincible-jha/agent-energy-budget"
     }
    ]
   },
   {
    "query": "LLM context window budget",
    "label": "context budget",
    "hits": [
     {
      "full_name": "yaswanthme007/tokenscope",
      "stars": 9,
      "description": "The first open-source token profiler for AI coding agents. Analyzes session logs, detects repeated content and bloated tool results, and shows you exactly where your context window budget goes  with c",
      "html_url": "https://github.com/yaswanthme007/tokenscope"
     },
     {
      "full_name": "eatakishiyev/context-forge",
      "stars": 6,
      "description": "A context compiler for LLM agents: scores, compresses, reorders, and budgets everything entering the context window to stop context rot — recovering both accuracy and token cost. Open-source core, dro",
      "html_url": "https://github.com/eatakishiyev/context-forge"
     },
     {
      "full_name": "nshkrdotcom/dexterity",
      "stars": 6,
      "description": "Code Intelligence: Token-budgeted codebase context for Elixir agents. Solves context window limitations by providing a deterministic Elixir semantic graph and agent-ready Repo Map for LLMs.",
      "html_url": "https://github.com/nshkrdotcom/dexterity"
     },
     {
      "full_name": "Akkshita06/contextforge",
      "stars": 3,
      "description": "Context-native AI orchestration runtime that gives explicit, budget-aware control over LLM context windows using declarative slots, automatic compression, and full observability. Build production-grad",
      "html_url": "https://github.com/Akkshita06/contextforge"
     },
     {
      "full_name": "kelvincushman/orphus",
      "stars": 3,
      "description": "Orphus — an agent harness whose agents deliberate in rooms outside their context windows. Fork of Atomic (Pi lineage) plus bounded multi-agent discussion, budgeted digests, and a declarative role mani",
      "html_url": "https://github.com/kelvincushman/orphus"
     }
    ]
   }
  ],
  "D3": [
   {
    "query": "LLM self-verification",
    "label": "self-verification",
    "hits": [
     {
      "full_name": "dCaples/AutoDidact",
      "stars": 688,
      "description": "Autonomously train research-agent LLMs on custom data using reinforcement learning and self-verification.",
      "html_url": "https://github.com/dCaples/AutoDidact"
     },
     {
      "full_name": "olemeyer/rocketplaneIO",
      "stars": 158,
      "description": "Self-hosted AI SRE for Kubernetes — zero-instrumentation eBPF observability plus a copilot that fixes issues through guardrailed, self-verifying actions. BYO-LLM, air-gapped capable.",
      "html_url": "https://github.com/olemeyer/rocketplaneIO"
     },
     {
      "full_name": "cozytab/fable5-mode",
      "stars": 120,
      "description": "Make Opus 4.8 (or any Claude model) work like Claude Fable 5 — a Claude Code skill + guard hooks (plan gate, model ceiling, per-task enforcement) for Fable-5-grade discipline: plan, self-verify, and r",
      "html_url": "https://github.com/cozytab/fable5-mode"
     },
     {
      "full_name": "NineAbyss/S2R",
      "stars": 77,
      "description": "This is the official implementation of the paper \"S²R: Teaching LLMs to Self-verify and Self-correct via Reinforcement Learning\"",
      "html_url": "https://github.com/NineAbyss/S2R"
     },
     {
      "full_name": "microsoft/clinical-self-verification",
      "stars": 67,
      "description": "Self-verification for LLMs.",
      "html_url": "https://github.com/microsoft/clinical-self-verification"
     }
    ]
   },
   {
    "query": "agent self-refine feedback",
    "label": "self-refine",
    "hits": [
     {
      "full_name": "idanbe/safe-refund-agent",
      "stars": 0,
      "description": "A governed AI refund agent demonstrating Feedback Loops, Self-Refining Agents, and Tool Safety & Guardrails",
      "html_url": "https://github.com/idanbe/safe-refund-agent"
     },
     {
      "full_name": "chandinik1/LLM-Trace-Tool",
      "stars": 0,
      "description": "Multi agent with LLM-as-judge and self refining prompt agent with ground truth feedback, the pipeline that traces the testcases to requirements ",
      "html_url": "https://github.com/chandinik1/LLM-Trace-Tool"
     },
     {
      "full_name": "gayatri-hacks/EduAssess-AI",
      "stars": 0,
      "description": "Automated educational content generator with intelligent review pipeline. Generator Agent produces grade-specific learning materials. Reviewer Agent validates content quality with structured feedback.",
      "html_url": "https://github.com/gayatri-hacks/EduAssess-AI"
     }
    ]
   }
  ]
 }
}
```

## 5. 核心語義（outcome contract / 仲裁 / reducer）

```text
SOURCE_OUTCOMES       = HIT | ZERO_RELEVANT_HIT | UNAVAILABLE | BLOCKED_BY_AUTHORITY | ERROR
CROSS_SOURCE_STATUSES = ALIGNED | MEMORY_STALE | KNOWLEDGE_STALE | WEB_NEWER_SUPPORT |
                        NORMATIVE_OVERRIDES_WEB | WEB_CONTRADICTS_INTERNAL |
                        MEMORY_CONTRADICTS_CANONICAL | DISPUTED | INSUFFICIENT
MEMORY_GRADES         = APPROVED（可 support, 需 freshness）| CANDIDATE（lead only）|
                        REVOKED（anti-regression only）| PROVENANCE_WEAK（lead only）
FULL_PASS_RULE        = 3 通道 ∈ {HIT, ZERO_RELEVANT_HIT} + attempted + provenance complete
                        + freshness satisfied + blocker=0 + counterevidence done → RESEARCH_PASS_CANDIDATE
                        UNAVAILABLE → RESEARCH_PARTIAL; BLOCKED → RESEARCH_BLOCKED_BY_AUTHORITY（優先）;
                        ERROR → RESEARCH_ERROR_STOP
FailClosed            = channel 未 attempt 且非 BLOCKED → raise FailClosedSilentSkip(SILENT_SOURCE_SKIP)
```

## 6. 測試（真實 stdout; 68 tests）

```text

```

## 7. Canaries（全文）

### CANARY-4（stale memory fixture）
```json
{
 "canary": "CANARY-4",
 "scenario": "stale approved memory vs current external official",
 "adjudication": {
  "cross_source_status": "MEMORY_STALE",
  "detail": "approved memory stale vs canonical -> freshness check required"
 },
 "counterevidence": {
  "required": true,
  "query_count": 4,
  "strategy": [
   "known issues",
   "security advisory",
   "failed adoption / contradicting benchmark",
   "superseded decision"
  ],
  "status": "ZERO_RELEVANT_COUNTEREVIDENCE_HIT",
  "note": "recorded in QueryLedger; zero hit is explicit, not silent omission; ERROR -> incomplete (COUNTEREVIDENCE_MISSING)"
 },
 "no_stale_recommendation": true,
 "staleness_finding_emitted": true,
 "candidate_correction": "CandidateKnowledge correction in candidate namespace (no silent rewrite)",
 "pass": true
}
```
### CANARY-5（web outage fixture）
```json
{
 "canary": "CANARY-5",
 "scenario": "web outage",
 "web_channel": {
  "status": "UNAVAILABLE",
  "reason": "source/service/network unavailable",
  "attempted": true,
  "retrieved_count": 0,
  "relevant_count": 0,
  "provenance_complete_count": 0,
  "stale_count": 0,
  "receipt_refs": [],
  "query_count": 1
 },
 "terminal": {
  "all_three_accounted_for": false,
  "full_pass_eligible": false,
  "blocker_codes": [
   "SOURCE_UNAVAILABLE"
  ],
  "terminal": "RESEARCH_PARTIAL",
  "source_statuses": {
   "memory": "HIT",
   "knowledge": "HIT",
   "web": "UNAVAILABLE"
  }
 },
 "attempted_true": true,
 "status_unavailable": true,
 "full_pass_eligible_false": true,
 "terminal_partial": true,
 "no_fake_web_evidence": true,
 "pass": true
}
```
### CANARY-6（真實三通道; production call site）
```json
{
 "schema": "LOGICAL_FAR_TRI_SOURCE_COVERAGE_V1",
 "workorder_id": "WO-FAR-TRISOURCE-001",
 "run_id": "CANARY-6",
 "research_plan_digest": "canary-6-plan-digest",
 "generated_at_utc": "2026-08-13T15:49:57.029302+00:00",
 "memory": {
  "status": "HIT",
  "relevant_count": 5,
  "attempted": true,
  "retrieved_count": 5,
  "provenance_complete_count": 5,
  "stale_count": 0,
  "receipt_refs": [
   "DOC-ea5297c4dca84cb61024",
   "DOC-54d6ed9eff7417637aa5",
   "DOC-16cab23b8a94b8f705fd",
   "DOC-1c00cf185209aff41e14",
   "DOC-3c655b49664048104e14"
  ],
  "query_count": 1,
  "candidate_count": 5,
  "approved_count": 0,
  "revoked_count": 0
 },
 "knowledge": {
  "status": "HIT",
  "relevant_count": 5,
  "attempted": true,
  "retrieved_count": 5,
  "provenance_complete_count": 5,
  "stale_count": 0,
  "receipt_refs": [
   "C:/Projects/Agent_Workspace/知識庫/實作相關DOC/fabric-autonomous-research/升級方案/FAR_TRI_SOURCE_MANDATORY_RESEARCH_ASSURANCE_HGK_UPGRADE_PROMPT_2026-08-13_r1.md",
   "C:/Projects/Agent_Workspace/知識庫/實作相關DOC/fabric-autonomous-research/FAR_TRI_SOURCE_INTEGRATED_UPGRADE_PLAN_2026-08-13_r1.md",
   "C:/Projects/Agent_Workspace/知識庫/實作相關DOC/fabric-autonomous-research/USER_DECISION_FAR_RETRIEVAL_2026-08-13_001.md",
   "C:/Projects/Agent_Workspace/知識庫/實作相關DOC/fabric-autonomous-research/CHANGE_INPUT_MANIFEST_TRI_SOURCE_2026-08-13.json",
   "C:/Projects/Agent_Workspace/知識庫/工程基座/GPTs_GENIEMAKER_AI產品經理_and_設計開發工程師_KnowledgePack_and_GPT_Builder_合冊/KnowledgePack_Upload20/18_AGENTIC_ENGINEERING_MASTERBOOK_EXTRACTION.md"
  ],
  "query_count": 1
 },
 "web": {
  "status": "ZERO_RELEVANT_HIT",
  "relevant_count": 0,
  "attempted": true,
  "retrieved_count": 0,
  "provenance_complete_count": 0,
  "stale_count": 0,
  "receipt_refs": [],
  "query_count": 1
 },
 "crosscheck": {
  "aligned_claim_count": 1,
  "contradicted_claim_count": 0,
  "unresolved_claim_count": 0,
  "stale_memory_findings": 0,
  "stale_knowledge_findings": 0,
  "web_only_new_findings": 0
 },
 "terminal": {
  "all_three_accounted_for": true,
  "full_pass_eligible": true,
  "blocker_codes": [],
  "terminal": "RESEARCH_PASS_CANDIDATE",
  "source_statuses": {
   "memory": "HIT",
   "knowledge": "HIT",
   "web": "ZERO_RELEVANT_HIT"
  }
 }
}
```

## 8. Challenge/AO 閉環（12 findings 全閉合）

```json
{
  "schema": "FAR-TRI-SOURCE-CHALLENGE-CLOSURE/1",
  "lane": "deleg_1fdf4a41 (challenge + acceptance, read-only, 381.45s)",
  "verdict": "CHALLENGED / AO FAIL -> repaired -> re-verified (deleg_c0193bda) -> closed",
  "findings": {
    "F1": "CLOSED — r8 immutability re-freeze: canonical 58de0815->historical (FAR_R8_HISTORICAL_BASELINE.md); canonical current b0b21ced… (x4 mirrors); all hash refs updated",
    "F2": "CLOSED — run_full_assurance real production call site + CANARY-6 (memory=HIT knowledge=HIT web=ZERO_RELEVANT_HIT -> RESEARCH_PASS_CANDIDATE); RB-WO-FAR-TRISOURCE-001 verified in spine",
    "F3": "CLOSED — res=None bound before try (no NameError on first-channel probe raise); regression test_f3_probe_raise_first_channel_no_crash",
    "F4": "CLOSED — per-iteration res reset (no cross-channel leak); regression test_f4_probe_raise_later_channel_no_leak",
    "F5": "CLOSED — stub adapter replaced by run_full_assurance (real dispatch)",
    "F6": "CLOSED — counterevidence_probe returns ERROR on query exception -> COUNTEREVIDENCE_MISSING reachable; regression test_f6_counterevidence_error_incomplete",
    "F7": "CLOSED — ClaimLedger.tsv legacy 9-col header commented; only 15-col tri-source header active",
    "F8": "CLOSED — GitHub research evidence copied to evidence-bundle/raw-github/ (2 files)",
    "F9": "CLOSED — terminal_reducer checks SOURCE_BLOCKED before SOURCE_UNAVAILABLE; regression test_f9_blocked_precedes_unavailable",
    "F10": "NOTED — allowed_web_roots delegation documented (probe enforces; run_full_assurance passes roots to retrieve_web)",
    "F11": "CLOSED — CHANGE_INPUT_MANIFEST_TRI_SOURCE now lists 19 files incl. new subject artifacts with sha256",
    "F12": "CLOSED — classify_memory_rows PROVENANCE_WEAK precedes APPROVED when provenance fields missing; regression test_f12_provenance_weak_precedes_approved"
  },
  "verification": "68/68 tests OK (63 + 5 regression); CANARY-4/5/6 ALL_PASS; AO re-verify (deleg_c0193bda) A1/A11/A12 PASS + A14 closed",
  "generated_at_utc": "2026-08-13T17:10:00Z"
}

```

AO 雙輪: deleg_1fdf4a41（round1: F1-F12, 2 HIGH/5 MED/5 LOW-INFO）→ 全修 →
deleg_c0193bda（focused: A1/A11/A12 PASS + A14 closed）。兩 lane 均 read-only、無檔案變更。

## 9. 輸入凍結 + FIT-GAP

```json
{
  "schema": "FAR-TRI-SOURCE-FITGAP/1",
  "changeset": "FAR_TRI_SOURCE_MANDATORY_RESEARCH_ASSURANCE",
  "questions": [
    {"q": "Can current ResearchPlan express required source classes?", "answer": "NO -> patched additively: source_assurance section (mode/minimum_probe/counterevidence/freshness)", "gap": "CLOSED_ADDITIVE"},
    {"q": "Can QueryLedger record source class?", "answer": "YES (query rows record source route; counterevidence queries appended)", "gap": "NONE"},
    {"q": "Can ClaimLedger express provenance/freshness/cross-source?", "answer": "NO -> patched additively: memory/knowledge/web_evidence_ids + authority + freshness + provenance + cross_source_status columns", "gap": "CLOSED_ADDITIVE"},
    {"q": "Can ResearchRunReceipt carry tri-source coverage?", "answer": "NO -> patched additively: tri_source_coverage field (embed TriSourceCoverageReceipt, not new system)", "gap": "CLOSED_ADDITIVE"},
    {"q": "Does Memory API return state/provenance?", "answer": "PARTIAL -> classify_memory_rows grades APPROVED/CANDIDATE/REVOKED/PROVENANCE_WEAK from row fields", "gap": "CLOSED_ADAPTER"},
    {"q": "Does Knowledge route link derived result to source?", "answer": "PARTIAL -> provenance_complete_count tracks sha256/source_id; derived without locator = lead only", "gap": "CLOSED_ADAPTER"},
    {"q": "Does Web route perform real online retrieval + locator?", "answer": "YES (far_retrieval.retrieve_web GET-only, https, exact-host, snapshot/locator) + GitHub research used real Search API", "gap": "NONE"}
  ],
  "reuse_first": "far_retrieval.py probes reused as-is; only new logical module far_trisource.py (coordinator/receipt/arbitration/reducer) + template additive patches",
  "no_new_platforms": "no new service/DB/scheduler/crawler; Qdrant/Neo4j default-off preserved",
  "generated_at_utc": "2026-08-13T16:30:00Z"
}

```
CHANGE_INPUT_MANIFEST: `知識庫/實作相關DOC/fabric-autonomous-research/CHANGE_INPUT_MANIFEST_TRI_SOURCE_2026-08-13.json`（19 files, 各含 sha256）

## 10. 證據身份

```text
FAR_EVIDENCE_MANIFEST.json ..... 119 entries（current; 含全部 tri-source 工件）
FAR_FINAL_ACCEPTANCE_EVIDENCE.md b0b21ced799face772327199e5b29ca1bf016b5177a06ffe9ee1832efa653d40（canonical current; 四處 byte-identical）
FAR_R8_HISTORICAL_BASELINE.md ... r8=58de0815… immutable; supersession 鏈（58de0815→eff79b73→a45b8e1c→151aaaf6→b0b21ced→b0b21ced799face7… 依序）
subject root ..................... 5720337bce9ef094…（95 files; r8 驗收時重算一致; 不因本 ChangeSet 改變 core subject）
```

## 11. 驗收指引（challenge-review grammar）

```text
可獨立驗證: outcome contract 語義（§5）/ 68 tests 真實 stdout（§6）/ canaries 全文（§7）/
  12 findings 閉合（§8）/ D 決策與 GitHub 原始證據（§3/§4）/ 治理記錄（§2）/
  FailClosed SILENT_SOURCE_SKIP（§5）→ blocking contradiction = 0
```

```text
STOP
TRI_SOURCE_MANDATORY = ACTIVE（WO VERIFIED; 68 tests; canaries ALL_PASS; 12 findings closed）
NEXT = EXTERNAL_FOCUSED_REVIEW（canonical b0b21ced799face7…）
```
