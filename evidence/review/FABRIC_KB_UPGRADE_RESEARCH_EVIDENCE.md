# FABRIC KB/Memory/KG Shared-Infrastructure Upgrade — FAR Research + Report (single evidence MD)

**WO:** WO-HGK-KBUPGRADE-RESEARCH-001 · **Board:** fabric-kb-upgrade-far · **Generated:** 2026-08-14T04:47:00Z
**Gate 1 (FAR research):** PASS — challenge lane CHALLENGE_VERDICT=PASS (A1..A10, 5 LOW findings integrated)
**Gate 2 (user HITL):** PENDING — this MD is the submission; no self-approval.

## 0. Claim ceiling
- This round produced RESEARCH + REPORT only. NO schema migration, NO spine mutation, NO KB re-ingest performed.
- NO product code changed in HG-KSEOS / SQS-THC / Fabric (task tooling under gitignored var/).
- NO vector DB / KG / provider enablement.
- HERMES_DIRECT_TRACKED_PRODUCT_WRITE = 0 (Codex write confined to gitignored var/hermes-memory-research/codex_output/).

## 1. WorkOrder / governance binding
- REQ-HGK-KBUPGRADE-RESEARCH-001 FROZEN (canonical event EVT-…)
- TS-HGK-KBUPGRADE-RESEARCH-001 (taskspec, writer=codex, writable_root var/a2/wt-kbupgrade-research)
- WO-HGK-KBUPGRADE-RESEARCH-001 (workorder, writer=codex, base_head 22e21f0, rollback_pointer RB-WO-HGK-KBUPGRADE-RESEARCH-001)

## 2. Artifacts (raw index, sha256 from final bytes)
| artifact | bytes | sha256 |
|---|---|---|
| K4_cross_analysis.md | 7980 | `0b913c3a342e376c9243cd522a901002035c90fec504138661e643f3a0f2a9d8` |
| K5_report_draft.md | 5290 | `ad6ee857598c3d81765ae63fa2357a7925f8c0a3da523996ed3602bcbfe4fa2a` |
| codex_output/fabric_kb_upgrade_analysis.md | 12483 | `53a88b4e2afc743eea7b05de1cba545dad6871634e52384e00b6e048c3f8652d` |
| M8_fabric_retrieval_analysis.md | 5723 | `1721a6ceb2bfb8c540667df6304392db0586c9e81f702524c3b33a0caa2c1035` |

## 3. KANBAN trace
K1 Folder audit: done (8 tables + 10 APIs; 9698 md; 351/351 dead sources; governance slots pre-reserved)
K2 Web research: done (13 sources; file-layer + namespace isolation consensus; anti-patterns)
K3 Governance analysis: done (15 DOC principles; profile-team blueprint; feasible=PARTIAL)
K4 Cross-analysis: done (3-stage architecture; SoD matrix; non-goals)
K5 Report MD + Gate2 HITL: done (challenge findings integrated)
K6 Evidence freeze: in progress
K7 Codex primary execution: done (fabric_kb_upgrade_analysis.md 12483 B)

## 4. SWARM trace
- Research lanes: deleg_031e33db (3 parallel: folder audit / web / governance), 12:24-12:33 UTC.
- Acceptance lane: deleg_292ece9c (1 fresh-context VERIFY_ONLY challenge), 12:37-12:44 UTC.

## 5. CODEX trace (writer=codex, K7)
- Spawn: codex-cli 0.147.0-alpha.6.5 sealed lane; isolated CODEX_HOME/OPENCODEX_HOME; credential from canonical .env.
- Output: var/hermes-memory-research/codex_output/fabric_kb_upgrade_analysis.md (12,483 B, 8 sections).
- Provider receipt: status OK (WS 426 → HTTP fallback, defect-class OPENCODEX-WS-426-001).

## 6. Challenge lane — CHALLENGE_VERDICT=PASS
```
CHALLENGE_VERDICT=PASS
A1..A10 verification table (fresh-context VERIFY_ONLY lane, deleg_292ece9c, 2026-08-14 12:37-12:44 UTC):
- A1 spine five tables exist, kg_edges/kg_assertions = 0 rows: PASS (sqlite3 RO, hg-kseos.db 793MB)
- A2 knowledge.py KnowledgeFactory + search/remember/revoke_memory: PASS (10 named methods)
- A3 KNOWLEDGE_POLICY.yaml cross_namespace_write_default=DENY / domain_owner_retains_truth_authority=true / candidate_is_truth=false: PASS
- A4 profiles/hgk-knowledge-factory dir (SOUL.md/config/distribution/skills-empty): PASS
- A5 far_retrieval.py retrieve_memory directly queries spine DB (sqlite3 RO, bypasses KnowledgeFactory): PASS — duplication confirmed
- A6 research docs no baseless claims: PASS (14/14 checks actual; minor count/path nits only)
- A7 conclusions match facts: PASS
- A8 no over-engineering (no immediate platform/vector/new service): PASS
- A9 3-stage vs non-goals consistency: PASS (reasonable layering, no contradiction)
- A10 stale-index debt: CONFIRMED — sources 351/351 dead paths (12 SQS-THC\SSOT + 339 SQS-THC\技術資料庫), FTS 354 docs all from deleted dirs
FINDINGS (all LOW, no impact on direction):
1. RAG KB acceptance = 14/14 checks (not 'ten'); depth L3+L4; backend SQLite FTS5 via KnowledgeFactory
2. KnowledgeFactory = 10 named methods (+__init__), not 11
3. KnowledgeFactory tests = 4 files, not 5
4. Governance slot files at Fabric/stage/RP002-STAGE-FABRIC/A0_KNOWLEDGE_EXTENSION_EVIDENCE.yaml + Fabric/stage/RP002-STAGE-HGK/KG1/KG1_NAMESPACE_MODEL.json + Fabric/HGK_STACK_MANIFEST.yaml (not all under Fabric/control/)
5. sources 351/351 dead (researcher said 354 FTS docs; actual source rows 351 — debt MORE thorough than claimed)

```

## 7. Key conclusions (condensed)
1. User proposal is architecturally sound and matches FABRIC original design intent — governance slots pre-reserved (KNOWLEDGE_POLICY shared.* / KG1 gate / HGK_STACK_MANIFEST knowledge_fts service / hgk-knowledge-factory profile).
2. Feasible = PARTIAL: ONLY as SHARED_INFRASTRUCTURE_PROFILE_TEAM capability substrate (heavy_stack=false, fabric.* candidate-only); NOT knowledge-truth transfer. Extraction = constitutional change → human two-key approval.
3. Three bottom lines: domain_owner_retains_truth_authority=true; cross_namespace_write_default=DENY; fabric_can_mutate_truth=false.
4. Industry consensus: shared file/Git layer + namespace isolation (Letta/OpenAI/LangGraph/Claude); heavy platforms = anti-pattern (MemGPT pivot, OpenMemory retired, mem0 #5151 KG poisoning).
5. Data debt: sources 351/351 dead canonical_paths; FAR retrieve_memory duplicates KnowledgeFactory.search; kg_edges empty (0 rows).
6. Recommended: 3 stages — Stage-1 data-layer consolidation NOW (re-ingest 知識庫\HG-KSEOS_SSOT + SQS-THC&TW-ICT_SSOT as canonical roots; converge retrieval on KnowledgeFactory; no new platform/DB/KG); Stage-2 formalize profile team per FDA/FAR precedent; Stage-3 KG conditional-last (DOC-12 edge admission + tenant isolation + kg_edges-vs-evidence_graph disambiguation; Qdrant/Neo4j default-off).

## 8. Gate 2 — user decisions requested
1. Approve Stage 1 (stale-index re-ingest + retrieval API convergence) under existing hgk-knowledge-factory profile + FAR tri-source (no new infrastructure)?
2. Approve starting Stage 2 governance formalization (SHARED_INFRASTRUCTURE_PROFILE_TEAM landing, constitutional two-key approval flow)?
3. Confirm Stage 3 (KG) stays conditional-last / not this round?

## 9. Non-claims / STOP
- STOP: awaiting user HITL on §8. Do NOT self-approve Gate 2.
- No migration executed; no truth transfer; production/live/remote not claimed.
