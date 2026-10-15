# FAR TRI-SOURCE FOCUSED HARDENING — 單一實作證據 v2（Single Evidence MD, 全量 raw）

> Document ID: `FAR-TRI-SOURCE-FOCUSED-HARDENING-EVIDENCE-20260814-R2`
> 用途: 外部驗收官對 WO-FAR-HARDENING-001 之單一驗收證據（EXT-FAR-TS-HARD-001..006 閉合版）
> 生成: 2026-08-13T17:48:34Z（UTC; 全事件時間戳 <= 本時間戳）
> 本版: EXT-FAR-TS-RE-001（subject/evidence 分離）+ RE-002（final evidence manifest）+ RE-NBO-001（欄位名）閉合

## 0. Claim ceiling

```text
FAR_TRI_SOURCE_FOCUSED_HARDENING = PASS（WO-FAR-HARDENING-001 VERIFIED）
CURRENT_FAR_TRI_SOURCE_IMPLEMENTATION = PASS_ELIGIBLE_FOR_EXTERNAL_FINAL_ACCEPTANCE
Swarm/multi-subagent = DEFAULT-ON（UD-FAR-SWARM-DEFAULT-ON-2026-08-14-001; CANARY-7 真實 fanout）
103/103 tests（exact denominator; nodeids digest 626d647284c1f755…）
CANARY-H1..H5 ALL_PASS + CANARY-7（swarm 實證）
SECURITY: redirects DISABLED（EXT-FAR-TS-HARD-001 repair）; AO PASS（AO-H01..H15）
r8 baseline = 58de0815… immutable ｜ SQS FT=0 ｜ broker write=0
PRODUCTION / SQS LIVE / REMOTE = NOT_CLAIMED / NOT_AUTHORIZED / NOT_CLAIMED
```

## 1. External Challenge Closure（EXT-FAR-TS-HARD-001..006 + RE-001/002/NBO-001）



```text
HARD-001 CONFIRMED_DEFECT → CLOSED: automatic redirects DISABLED (_NoRedirectHandler 對任何
  redirect 直接 raise; strict allowlist + pre-connect public-IP 驗證 + 無 redirect chain =
  凍結 plan preferred smallest path）; FH-T013/T014 更新 + CANARY-H4 re-verified（5 targets 全 REJECTED）
HARD-002 CONFIRMED_DEFECT → CLOSED: 全時間戳改 timezone-aware UTC（H2 retrieved_at=實際 fetch UTC;
  security closure/AO/rollback/subject 全 generated_at_utc 實際 UTC）; 無未來時間（§0 生成時間為上界）
HARD-003 EVIDENCE_GAP → CLOSED: 真實 test raw stdout（合併 2>&1）+ 完整 nodeids + exit code 內嵌（§11）
HARD-004 EVIDENCE_GAP → CLOSED: post-change subject manifest 全文（§15）+ current evidence manifest
  全文（§16）+ ExecutionBinding 全文（§17）+ compile receipt + rollback receipt + changed-file diff
HARD-005 EVIDENCE_GAP → CLOSED: CANARY-H1..H5 全 JSON 內嵌（§13）+ security/AO raw receipts（§14）
HARD-006 NBO → CLOSED: H2 補 requested_url/final_url/redirect_chain=[]（§13; http:// 為 arXiv XML
  內 canonical link 非 fetch target）
```

## 2. 治理記錄（SharedSpine readback）

```text
WO  : {"workorder_id": "WO-FAR-HARDENING-001", "writer": "codex", "state": "VERIFIED", "rollback_pointer": "RB-WO-FAR-HARDENING-001"}
EVD-FAR-HARDENING* rows:
- EVD-FAR-HARDENING-AO JSON fe7196e456667531
- EVD-FAR-HARDENING-CANARIES JSON fa3da43947301284
- EVD-FAR-HARDENING-COMPILE JSON 511868d87228ea86
- EVD-FAR-HARDENING-DENOM JSON 7d9407c1f88770b4
- EVD-FAR-HARDENING-EVIDENCE-V2 MARKDOWN 58849ecdc2649e2b
- EVD-FAR-HARDENING-EVIDENCE-V3 MARKDOWN 91debeb4e1916028
- EVD-FAR-HARDENING-EVIDENCE-V4 MARKDOWN 02fb12cbab6f1757
- EVD-FAR-HARDENING-EVIDENCE-V5 MARKDOWN 85367fe314ce68c3
- EVD-FAR-HARDENING-FITGAP JSON ff6c80408464d7d1
- EVD-FAR-HARDENING-MODULE PYTHON 47d0ce54ef6329a4
- EVD-FAR-HARDENING-ROLLBACK JSON 28a4ae6c63b1ad4e
- EVD-FAR-HARDENING-SECCL JSON 871ca85f0f0aa4a7
- EVD-FAR-HARDENING-SUBJECT JSON aee7b7efd2a1b65a
- EVD-FAR-HARDENING-TESTS PYTHON 1e93885de3601c9a
- EVD-FAR-HARDENING-TRISOURCE PYTHON 9d18a78ca90c3eb7
```

## 3. C0 凍結（HARDENING_CHANGE_INPUT_MANIFEST 全文）

```json
{
 "schema": "FAR-HARDENING-CHANGE-INPUT-MANIFEST/1",
 "changeset": "FAR_TRI_SOURCE_FOCUSED_HARDENING_20260814",
 "baseline": "FAR_TRI_SOURCE_IMPLEMENTATION_2026-08-13_r1 (WO-FAR-TRISOURCE-001 VERIFIED)",
 "frozen_at_utc": "2026-08-13T16:22:57.811023+00:00",
 "files": {
  "Fabric\\fabric-autonomous-research\\far_retrieval.py": {
   "sha256": "6fd1eee2875272fa606dca48089cd76786e223a4977e1fa69cdb58e478576703",
   "bytes": 18244
  },
  "Fabric\\fabric-autonomous-research\\far_trisource.py": {
   "sha256": "ef99c55ecfbf326e54ba78767382cdaca04131cc8e00fe7e7301a787d2bfae1e",
   "bytes": 15670
  },
  "Fabric\\fabric-autonomous-research\\tests\\test_far_retrieval.py": {
   "sha256": "7dad36128a8f85581dbd757a1fdfc815c8354d57dd38d0c88a49c4e3e1a82f9d",
   "bytes": 6483
  },
  "Fabric\\fabric-autonomous-research\\tests\\test_far_trisource.py": {
   "sha256": "b6976cbbf788e5c5e74619f14cc30a8fc61178b97514cf8fc111ee107f395df6",
   "bytes": 11852
  },
  "Fabric\\fabric-autonomous-research\\research-product\\templates\\ClaimLedger.tsv": {
   "sha256": "aa2e27b351b108d236df9c080fd09227f9526645040e8069c76e6d7d7429ef64",
   "bytes": 589
  },
  "Fabric\\fabric-autonomous-research\\research-product\\templates\\ResearchPlan.yaml": {
   "sha256": "dcadff4e2d1af057965093275bf23e9989e34cf468a44c10ef7a3788dd76077f",
   "bytes": 713
  },
  "Fabric\\fabric-autonomous-research\\research-product\\templates\\ResearchRunReceipt.json": {
   "sha256": "e3fb41db474ace01f1a27f5ed6962063d780a3db6fc300fde5a9dee76278c9d5",
   "bytes": 401
  },
  "Fabric\\fabric-autonomous-research\\research-product\\templates\\ResearchSynthesis.md": {
   "sha256": "26832ca0afce5417d936f66c70f8f5a25c082c35bad522fea71bedee5a7ead57",
   "bytes": 901
  },
  "Fabric\\fabric-autonomous-research\\FAR_TRI_SOURCE_D_DECISIONS.json": {
   "sha256": "92fe09130c4cd55d13cc00a193bccfbb37c8c3499e6b1fcbde1e5e3d4f449562",
   "bytes": 5075
  },
  "Fabric\\fabric-autonomous-research\\FAR_TRI_SOURCE_FITGAP_RECEIPT.json": {
   "sha256": "bf25fde57ae4102ec5c724624a3fb1bc432f0e33ffd7c2174404e0f0fc25df3d",
   "bytes": 1848
  },
  "Fabric\\fabric-autonomous-research\\FAR_TRI_SOURCE_CHALLENGE_CLOSURE.json": {
   "sha256": "1e325082cb7726066b4055fa3933d5ce49d8b6583832ff7725885aaa53039a34",
   "bytes": 2086
  },
  "Fabric\\fabric-autonomous-research\\FAR_TRI_SOURCE_IMPLEMENTATION_EVIDENCE.md": {
   "sha256": "4793e16fa1b3f322bfde633d4dcbf5fc383de6aa942869ebcd533689b971bfde",
   "bytes": 31720
  },
  "Fabric\\fabric-autonomous-research\\FAR_FINAL_ACCEPTANCE_EVIDENCE.md": {
   "sha256": "b0b21ced799face772327199e5b29ca1bf016b5177a06ffe9ee1832efa653d40",
   "bytes": 78746
  },
  "知識庫\\實作相關DOC\\fabric-autonomous-research\\FAR_TRI_SOURCE_IMPLEMENTATION_2026-08-13_r1.md": {
   "sha256": "55a1f080a0bffe4f708178156b3ab4b58c25387e848b8a8e918d7dd0f88f1f48",
   "bytes": 8146
  },
  "知識庫\\實作相關DOC\\fabric-autonomous-research\\CHANGE_INPUT_MANIFEST_TRI_SOURCE_2026-08-13.json": {
   "sha256": "cf9da7e0b599c27e389ea12232b9a1ffd19b2b66fde9f44722177264f577cf10",
   "bytes": 3781
  }
 }
}
```

## 4. C1 FIT-GAP（全文）

```json
{
 "schema": "FAR-HARDENING-FITGAP/1",
 "changeset": "FAR_TRI_SOURCE_FOCUSED_HARDENING_20260814",
 "questions": [
  {
   "q": "Does evidence already have origin artifact id?",
   "answer": "NO — retrieval rows carry source_id/sha256 but no origin_artifact_id/origin_artifact_digest/source_family lineage fields",
   "gap": "FH-01 ADD"
  },
  {
   "q": "Does memory record retain source capsule/digest?",
   "answer": "PARTIAL — knowledge_fts rows carry doc_id (usable as origin_artifact_id); memory_records carry provenance text; no explicit digest linkage",
   "gap": "FH-01 ADD lineage fields"
  },
  {
   "q": "Does web client follow redirects?",
   "answer": "YES — urllib HTTPRedirectHandler with exact-host allowlist; no resolved-IP validation per hop",
   "gap": "FH-02 SSRF"
  },
  {
   "q": "Does web client expose resolved IP?",
   "answer": "NO — urllib hides peer address; need explicit DNS resolution + IP classification before connect",
   "gap": "FH-02 ADD"
  },
  {
   "q": "Does it reject all DOCTYPE or only XML DTD?",
   "answer": "_parse_atom rejects ANY DOCTYPE in first 4096B (too broad for HTML5 <!DOCTYPE html>); no MIME-aware semantics",
   "gap": "FH-02 MIME semantics"
  },
  {
   "q": "Does response receipt record truncation?",
   "answer": "NO — no bytes_received/bytes_read/content_complete/truncation_reason fields",
   "gap": "FH-03 ADD"
  },
  {
   "q": "Does query budget participate in PASS reducer?",
   "answer": "NO — query_count hardcoded 1 per channel; no DEFAULT_QUERY_BUDGET / exhaustion semantics in reducer",
   "gap": "FH-04 ADD"
  },
  {
   "q": "Does raw test denominator really equal 68?",
   "answer": "AMBIGUOUS — '63 existing + 26 tri-source 中 5 regression' wording not exact; need collect-only inventory",
   "gap": "EV-01"
  },
  {
   "q": "Is there already a Web HIT canary in implementation evidence?",
   "answer": "NO — evidence shows UNAVAILABLE + ZERO_RELEVANT_HIT only",
   "gap": "FH-05 ADD"
  },
  {
   "q": "Is corroboration policy claim-class-aware?",
   "answer": "NO — arbitration is claim-role aware but no minimum-evidence-by-class policy (INTERNAL_NORMATIVE vs EXTERNAL_CURRENT_FACT vs COMMUNITY_DEFECT)",
   "gap": "FH-06 ADD"
  },
  {
   "q": "Is D1-D4 '社群共識' wording too strong?",
   "answer": "YES — GitHub small repos = SUPPORT/COMMUNITY_SIGNAL not normative consensus; need EV-02 wording + authoritative calibration (OWASP/WHATWG/arXiv)",
   "gap": "EV-02"
  }
 ],
 "generated_at_utc": "2026-08-13T16:22:57.815023+00:00"
}
```

## 5. Compile Gate（Prompt Compiler current equivalent）

```json
{
  "schema": "FAR-HARDENING-COMPILE-RECEIPT/1",
  "changeset": "FAR_TRI_SOURCE_FOCUSED_HARDENING_20260814",
  "equivalent_note": "Prompt Compiler current equivalent: WO admission (typed SharedSpine) + python compile gate + lint + full test entry (per REUSE-FIRST; no new compile system)",
  "gates": {
    "workorder_admission": "REQ-FAR-HARDENING-001 FROZEN v1 -> WO-FAR-HARDENING-001 CREATED (writer=codex; RB-WO-FAR-HARDENING-001)",
    "python_compile": "far_retrieval.py / far_trisource.py / tests/test_far_hardening.py py_compile PASS",
    "lint": "patch-tool syntax checks PASS (0 new errors)",
    "test_entry": "unittest discover -s tests -t . -> 103 tests (see TEST_DENOMINATOR.json)",
    "yaml_validate": "FAR_LONG_HORIZON_CONTRACT.yaml / FAR_ROUTE_CHECK.yaml parse PASS"
  },
  "generated_at_utc": "2026-08-13T17:10:00Z"
}

```

## 6. Swarm DEFAULT-ON（UD-FAR-SWARM-DEFAULT-ON-2026-08-14-001）

```text
USER 指令: 「把 FAR 改成默認開啟 Swarm 和多子代理」
契約變更: FAR_LONG_HORIZON_CONTRACT.yaml fanout.default_on=true（allowed_shapes 預設可用;
  max_lanes=WorkOrder budget; runtime_choices=[HERMES_SWARM, ...]）;
  FAR_ROUTE_CHECK.yaml lane_vs_execution 註記 DEFAULT_ON
不變式: canonical_parallel_writers=0; merge_collision=RESEARCH_DISPUTE_OPEN; cancel_on 同前;
  單線執行仍合法（swarm 是 default 非強制）
實證: CANARY-7（§13.7）— 真實 HERMES_SWARM fanout（2 平行 leaf: kb-worker + web-worker）→ merge
```
---
decision_id: UD-FAR-SWARM-DEFAULT-ON-2026-08-14-001
authority: USER
decided_at: 2026-08-14
status: FROZEN
supersedes: null
bound_into: [FAR_LONG_HORIZON_CONTRACT.yaml fanout, FAR_ROUTE_CHECK.yaml lane_vs_execution, TEAM.md, README.md, AGENTS.md, FAR_TRI_SOURCE_FOCUSED_HARDENING_20260814]
---

# USER DECISION — FAR Swarm / Multi-subagent DEFAULT-ON

## 指令

「把 FAR 改成默認開啟 Swarm 和多子代理。」

## 決策內容

1. **FAR research 執行預設 = 多子代理（swarm）啟用**：不須每次 WorkOrder 另行宣告 fanout shape 才允許；
   預設即以 HERMES_SWARM（Hermes delegate_task 平行子代理）執行獨立工作流。
2. **預設 fanout shapes 保持受治理**：SOURCE_FAMILY_SPLIT / HYPOTHESIS_SPLIT / INDEPENDENT_EXPERIMENT_SPLIT 預設可用；
   max_lanes 仍受 WorkOrder budget 管轄（預設上限 = WorkOrder resource budget）。
3. **不變式維持**（不因 default-on 而放鬆）：
   - canonical_parallel_writers = 0（平行子代理不得寫 canonical; tracked_mutation_writer=codex 不變）
   - merge_collision = RESEARCH_DISPUTE_OPEN（無多數決）
   - cancel_on = [BUDGET_EXHAUSTED, DUPLICATED_SCOPE, DEPENDENCY_INVALIDATED, SECURITY_BLOCK, NO_PROGRESS]
   - 每個子代理仍是 read-only research worker（Candidate 產出; 不可 self-accept; 不可寫 SQS FT / broker）
4. **單一執行緒仍允許**：問題簡單或 WO 明確單線時，native 直接執行合法（swarm 是 default 不是強制）。

## 依據（EV-02 措辭）

COMMUNITY_SUPPORT / DESIGN CALIBRATION：
- deep-research-protocol（5-agent research/consolidation SoD 分離）
- harness-research（MCP professional research pipeline）
- 成熟工程 SoD：research 平行分工 + 單一 canonical writer + 獨立 checker
- 治理邊界維持（HGK WorkOrder 唯一控制面; Fabric assurance; Hermes runtime）

## 生效範圍

FAR research runs（R0-R8）於 2026-08-14 起預設開啟 swarm/multi-subagent；
本決策不改變 production/live/remote claim ceiling。


## 7. FH-01..06 語義（不變; 見 v1 §5-§10）

```text
FH-01 lineage: origin_artifact_digest>id key; INDEPENDENT/DERIVED_SAME_ORIGIN/PARTIALLY_INDEPENDENT/ORIGIN_UNRESOLVED
FH-02 SSRF: https-only + port 443 + exact-host + IP 分類（含 6to4/Teredo）+ redirects DISABLED（HARD-001）
FH-03 truncation: content_read 欄位 + 負向推論規則
FH-04 budget: DEFAULT_QUERY_BUDGET 4+4; Case A PASS_ELIGIBLE / Case B PARTIAL_BUDGET_EXHAUSTED
FH-05 real web HIT: CANARY-H2（real arXiv; content_complete=True）
FH-06 corroboration: CLAIM_CLASS_MINIMUM（INTERNAL_NORMATIVE/EXTERNAL_CURRENT_FACT/COMMUNITY_DEFECT/RECOMMENDATION）
```

## 8. 變更檔案 exact set + diff 摘要

```text
changed vs C0 baseline（HARDENING_CHANGE_INPUT_MANIFEST）:
  far_retrieval.py      +SSRF validator/_NoRedirectHandler/MIME/truncation/lineage（HARD-001 repair 後 redirects disabled）
  far_trisource.py      +independence/budget/corroboration
  tests/test_far_hardening.py 35 FH-T（HARD-001 後 FH-T013/014 = redirects disabled）
  research-product/templates/*（ClaimLedger 18-col; ResearchPlan/RunReceipt/Synthesis）
  FAR_LONG_HORIZON_CONTRACT.yaml / FAR_ROUTE_CHECK.yaml（swarm default-on）
  FAR_TRI_SOURCE_D_DECISIONS.json（EV-02 wording）
  evidence: FITGAP/SECCL/AO/ROLLBACK/COMPILE receipts + subject manifest + canaries
diff 形式: 逐檔 patch（見各 patch diff）; 無刪除既有功能; 純 additive/minimal
```

## 9. 真實 test raw stdout（HARD-003 閉合; 合併 capture）

```text
command: C:\Users\user\AppData\Local\Programs\Python\Python311\python.exe -m unittest discover -s tests -t .（cwd=C:\Projects\Agent_Workspace\Fabric\fabric-autonomous-research; merged 2>&1）
exit_code: 0
.......................................................................................................
----------------------------------------------------------------------
Ran 103 tests in 3.150s

OK

```

## 10. 完整 nodeid list（EV-01 recomputable）

```text
count: 103
nodeids_digest: 626d647284c1f755baf83d2e942964485937abb4051755fe092f5b46a701e805
tests.test_far_hardening.BudgetTests.test_fh_t021_budget_exhausted_closed_pass_eligible
tests.test_far_hardening.BudgetTests.test_fh_t022_budget_exhausted_disputed_partial
tests.test_far_hardening.BudgetTests.test_fh_t023_budget_exhausted_weak_no_pass
tests.test_far_hardening.BudgetTests.test_fh_t024_extension_policy
tests.test_far_hardening.CorroborationPolicyTests.test_fh_t025_internal_normative
tests.test_far_hardening.CorroborationPolicyTests.test_fh_t026_external_fact
tests.test_far_hardening.CorroborationPolicyTests.test_fh_t027_recommendation
tests.test_far_hardening.CorroborationPolicyTests.test_fh_t028_claim_independence_binding
tests.test_far_hardening.DoctypeXmlTests.test_fh_t005_html5_doctype_accepted
tests.test_far_hardening.DoctypeXmlTests.test_fh_t006_xml_dtd_rejected
tests.test_far_hardening.DoctypeXmlTests.test_fh_t007_xinclude_not_processed
tests.test_far_hardening.LineageTests.test_fh_t001_same_digest_single_origin
tests.test_far_hardening.LineageTests.test_fh_t002_memory_plus_web_two_origins
tests.test_far_hardening.LineageTests.test_fh_t003_unresolved_origin
tests.test_far_hardening.LineageTests.test_fh_t004_same_origin_not_independent_corroboration
tests.test_far_hardening.RetrievalLineageTests.test_fh_t029_kb_rows_lineage
tests.test_far_hardening.RetrievalLineageTests.test_fh_t030_memory_rows_lineage
tests.test_far_hardening.SoDRegressionTests.test_fh_t037_no_new_platform
tests.test_far_hardening.SoDRegressionTests.test_fh_t038_rollback_pointer
tests.test_far_hardening.SsrfTests.test_fh_t008_http_deny
tests.test_far_hardening.SsrfTests.test_fh_t009_file_deny
tests.test_far_hardening.SsrfTests.test_fh_t010_localhost_deny
tests.test_far_hardening.SsrfTests.test_fh_t011_rfc1918_deny
tests.test_far_hardening.SsrfTests.test_fh_t012_linklocal_metadata_deny
tests.test_far_hardening.SsrfTests.test_fh_t013_redirects_disabled
tests.test_far_hardening.SsrfTests.test_fh_t014_redirect_private_ip
tests.test_far_hardening.SsrfTests.test_fh_t015_dns_private
tests.test_far_hardening.SsrfTests.test_fh_t016_exact_public_host
tests.test_far_hardening.TruncationTests.test_fh_t017_complete_under_cap
tests.test_far_hardening.TruncationTests.test_fh_t018_over_cap
tests.test_far_hardening.TruncationTests.test_fh_t019_truncated_cannot_sole_support_absence
tests.test_far_hardening.TruncationTests.test_fh_t020_truncated_positive_supports_observed
tests.test_far_hardening.WebHitCanaryTests.test_fh_t031_real_web_hit
tests.test_far_hardening.WebHitCanaryTests.test_fh_t032_locator_metadata
tests.test_far_hardening.WebHitCanaryTests.test_fh_t033_web_evidence_bound
tests.test_far_retrieval.FarRetrievalTests.test_cross_reference_agreement
tests.test_far_retrieval.FarRetrievalTests.test_cross_reference_disagreement
tests.test_far_retrieval.FarRetrievalTests.test_cross_reference_filters_trivial_tokens
tests.test_far_retrieval.FarRetrievalTests.test_kb_scan_finds_far_docs
tests.test_far_retrieval.FarRetrievalTests.test_memory_fts_query
tests.test_far_retrieval.FarRetrievalTests.test_parse_atom_rejects_doctype
tests.test_far_retrieval.FarRetrievalTests.test_redirect_handler_exact_host
tests.test_far_retrieval.FarRetrievalTests.test_run_stage_writes_ledgers
tests.test_far_retrieval.FarRetrievalTests.test_score_determinism
tests.test_far_retrieval.FarRetrievalTests.test_tokenize_ascii_words
tests.test_far_retrieval.FarRetrievalTests.test_tokenize_cjk_bigrams
tests.test_far_retrieval.FarRetrievalTests.test_web_arxiv_with_fake_fetch
tests.test_far_retrieval.FarRetrievalTests.test_web_deny_default
tests.test_far_retrieval.FarRetrievalTests.test_web_url_uses_https
tests.test_far_router.FarRouterTests.test_eligible_negative_cases
tests.test_far_router.FarRouterTests.test_financial_method_no_mutation
tests.test_far_router.FarRouterTests.test_general_research_routes_native
tests.test_far_router.FarRouterTests.test_literature_routes_native_aris
tests.test_far_router.FarRouterTests.test_mandatory_challenge_unavailable_blocks
tests.test_far_router.FarRouterTests.test_rlm_prime_unqualified_blocks
tests.test_far_router.FarRouterTests.test_rlm_prime_unqualified_degrades_native
tests.test_far_router.FarRouterTests.test_science_without_arc_research_only
tests.test_far_source_security.FarSourceSecurityTests.test_blocking_findings_are_counted
tests.test_far_source_security.FarSourceSecurityTests.test_sec_src_01_readme_ignore_fabric_policy
tests.test_far_source_security.FarSourceSecurityTests.test_sec_src_02_export_api_key_denied
tests.test_far_source_security.FarSourceSecurityTests.test_sec_src_03_writable_root_escalation_fails_qualification
tests.test_far_source_security.FarSourceSecurityTests.test_sec_src_04_version_claim_support_only
tests.test_far_source_security.FarSourceSecurityTests.test_sec_src_05_auto_install_requires_separate_qualification
tests.test_far_source_security.FarSourceSecurityTests.test_sec_src_06_live_broker_write_denied
tests.test_far_source_security.FarSourceSecurityTests.test_sec_src_07_disable_ao_denied
tests.test_far_source_security.FarSourceSecurityTests.test_sec_src_08_silent_provider_change_denied
tests.test_far_source_security.FarSourceSecurityTests.test_snippet_no_auto_run_without_all_conditions
tests.test_far_trisource.ArbitrationTests.test_approved_memory_aligned
tests.test_far_trisource.ArbitrationTests.test_candidate_memory_alone_insufficient
tests.test_far_trisource.ArbitrationTests.test_memory_contradicts_canonical
tests.test_far_trisource.ArbitrationTests.test_missing_provenance_lead_only
tests.test_far_trisource.ArbitrationTests.test_normative_overrides_web
tests.test_far_trisource.ArbitrationTests.test_revoked_memory_cannot_support
tests.test_far_trisource.ArbitrationTests.test_stale_approved_memory
tests.test_far_trisource.ArbitrationTests.test_stale_knowledge_external
tests.test_far_trisource.ArbitrationTests.test_web_contradicts_internal
tests.test_far_trisource.ArbitrationTests.test_web_newer_support
tests.test_far_trisource.ChannelOutcomeTests.test_blocked_by_authority
tests.test_far_trisource.ChannelOutcomeTests.test_error
tests.test_far_trisource.ChannelOutcomeTests.test_hit
tests.test_far_trisource.ChannelOutcomeTests.test_unavailable
tests.test_far_trisource.ChannelOutcomeTests.test_zero_relevant_hit
tests.test_far_trisource.CounterevidenceTests.test_load_bearing_requires_ce
tests.test_far_trisource.CounterevidenceTests.test_non_load_bearing_recorded
tests.test_far_trisource.MandatoryTests.test_all_hit_eligible
tests.test_far_trisource.MandatoryTests.test_blocked_limited_terminal
tests.test_far_trisource.MandatoryTests.test_error_stop
tests.test_far_trisource.MandatoryTests.test_silent_skip_raises_failclosed
tests.test_far_trisource.MandatoryTests.test_unavailable_no_full_pass
tests.test_far_trisource.ReceiptTests.test_memory_classification
tests.test_far_trisource.ReceiptTests.test_receipt_schema_and_embedding
tests.test_far_trisource.ReducerTests.test_counterevidence_missing_blocks
tests.test_far_trisource.ReducerTests.test_unresolved_contradiction_blocks
tests.test_far_trisource.RegressionTests.test_f12_provenance_weak_precedes_approved
tests.test_far_trisource.RegressionTests.test_f3_probe_raise_first_channel_no_crash
tests.test_far_trisource.RegressionTests.test_f4_probe_raise_later_channel_no_leak
tests.test_far_trisource.RegressionTests.test_f6_counterevidence_error_incomplete
tests.test_far_trisource.RegressionTests.test_f9_blocked_precedes_unavailable
tests.test_far_watchdog.FarWatchdogTests.test_budget_exhaustion_terminal
tests.test_far_watchdog.FarWatchdogTests.test_identical_action_repeat_aborts
tests.test_far_watchdog.FarWatchdogTests.test_no_progress_cycles_aborts
tests.test_far_watchdog.FarWatchdogTests.test_progress_class_whitelist
tests.test_far_watchdog.FarWatchdogTests.test_same_failure_twice_stops
```

## 11. EV-01 Test Denominator（全文）

```json
{
 "schema": "FAR-TEST-DENOMINATOR/1",
 "unique_union_collected": 103,
 "baseline_suite": {
  "collected": 37
 },
 "tri_source_suite": {
  "collected": 31
 },
 "hardening_suite": {
  "collected": 35
 },
 "nodeids_digest": "626d647284c1f755baf83d2e942964485937abb4051755fe092f5b46a701e805",
 "per_file": {
  "test_far_hardening": 35,
  "test_far_retrieval": 14,
  "test_far_router": 8,
  "test_far_source_security": 10,
  "test_far_trisource": 31,
  "test_far_watchdog": 5
 }
}
```

## 12. CANARY-H1..H5 全 JSON（HARD-005 閉合）

```json
{
 "CANARY-H1": {
  "scenario": "canonical DOC-A + memory summary of same DOC-A",
  "retrieval_hits": 2,
  "independent_origins": 1,
  "independent_source_families": 2,
  "duplicate_derivations": 1,
  "status": "DERIVED_SAME_ORIGIN",
  "pass": true
 },
 "CANARY-H2": {
  "scenario": "real official web HIT via arXiv API (current network)",
  "attempted": true,
  "web_status": "OK",
  "hit": true,
  "official_primary_count": 1,
  "sample": {
   "fetch_url": "http://arxiv.org/abs/2206.03003v2",
   "final_url": "http://arxiv.org/abs/2206.03003v2",
   "redirect_chain": [],
   "canonical_entry_url": "http://arxiv.org/abs/2206.03003v2",
   "host": "export.arxiv.org",
   "title": "Transformer-based Personalized Attention Mechanism for Medic",
   "content_type_kind": "XML",
   "content_complete": true,
   "truncation_reason": "NONE",
   "bytes_read": 9192,
   "retrieved_at": "2026-08-13T17:47:28Z"
  },
  "claim_ledger_bound": true,
  "pass": true
 },
 "CANARY-H3": {
  "scenario": "normal HTML5 <!DOCTYPE html> must not be rejected",
  "content_type_semantics": "HTML",
  "doctype_rejected": false,
  "pass": true
 },
 "CANARY-H4": {
  "scenario": "redirects DISABLED entirely (EXT-FAR-TS-HARD-001): any redirect denied before protected access",
  "targets": [
   [
    "https://evil.com/x",
    "REJECTED"
   ],
   [
    "https://10.0.0.5/x",
    "REJECTED"
   ],
   [
    "http://export.arxiv.org/x",
    "REJECTED"
   ],
   [
    "file:///etc/passwd",
    "REJECTED"
   ],
   [
    "https://export.arxiv.org/x2",
    "REJECTED"
   ]
  ],
  "no_real_private_probe": true,
  "pass": true
 },
 "CANARY-H5": {
  "scenario": "4+4 budget exhausted with DISPUTED claim",
  "terminal": "RESEARCH_PARTIAL_BUDGET_EXHAUSTED",
  "pass": true
 }
}
```

## 13. CANARY-7 — Swarm 真實 fanout receipt（全文）

```json
{
 "schema": "FAR-CANARY-7-SWARM/1",
 "changeset": "FAR_TRI_SOURCE_FOCUSED_HARDENING_20260814",
 "ud_ref": "UD-FAR-SWARM-DEFAULT-ON-2026-08-14-001",
 "runtime": "HERMES_SWARM (delegate_task parallel batch, SOURCE_FAMILY_SPLIT)",
 "run_id": "CANARY-7",
 "workers": [
  {
   "worker_id": "deleg_ce517704",
   "role": "kb-worker (LOCAL_GOVERNED_CORPUS family)",
   "duration_s": 35.67,
   "read_only": true,
   "claims": [
    {
     "claim_text": "Every formal admitted FAR Research WorkOrder must actually probe all three source channels — HGK_MEMORY / FABRIC_HGK_KNOWLEDGE / EXTERNAL_WEB — and the three channels must not be silently skipped by the agent; the stated goal is to minimize evidence omission, stale memory/knowledge acceptance, missed external updates, unresolved contradictions, and provenance collapse.",
     "locator": "FAR_TRI_SOURCE_IMPLEMENTATION_2026-08-13_r1.md (知識庫/實作相關DOC/fabric-autonomous-research/), §1 目標, lines 13-15",
     "claim_class": "INTERNAL_NORMATIVE"
    },
    {
     "claim_text": "run_tri_source_assurance fails closed: if any of the three channels was not attempted and the failure is not BLOCKED_BY_AUTHORITY, it raises FailClosedSilentSkip (SILENT_SOURCE_SKIP), verified by test TS-007 and regression evidence; outcome contract forbids SKIPPED/NOT_NEEDED/OPTIONAL_NOT_RUN statuses.",
     "locator": "FAR_TRI_SOURCE_IMPLEMENTATION_2026-08-13_r1.md (知識庫), §3.1-3.2 Outcome contract / FailClosed (H11-H15, H12), lines 40-55",
     "claim_class": "INTERNAL_NORMATIVE"
    },
    {
     "claim_text": "CANARY-6, a real tri-source run at the production call site run_full_assurance, produced memory=HIT, knowledge=HIT, web=ZERO_RELEVANT_HIT and terminated as RESEARCH_PASS_CANDIDATE with full_pass_eligible=True and blockers=[] — demonstrating the implemented pipeline yields a pass candidate without fabricating web evidence.",
     "locator": "FAR_TRI_SOURCE_IMPLEMENTATION_2026-08-13_r1.md (知識庫), §6 驗證結果, lines 114-115",
     "claim_class": "RESEARCH_FINDING"
    }
   ],
   "note": "claims = worker verbatim output (deleg_ce517704)"
  },
  {
   "worker_id": "deleg_326ea8ec",
   "role": "web-worker (EXTERNAL_WEB family, arXiv official API GET-only)",
   "duration_s": 34.52,
   "read_only": true,
   "claims": [
    {
     "claim_text": "Agent memory is a systems problem for long-horizon agents: a memory layer must determine which interactions become durable state, how that state is scoped and retrieved under latency constraints, and how it is revised or removed over time, extending beyond document retrieval (Oracle Agent Memory technical report, arXiv 2607.13157).",
     "locator": "https://arxiv.org/abs/2607.13157",
     "source_role": "WEB_PRIMARY",
     "claim_class": "RESEARCH_FINDING"
    },
    {
     "claim_text": "Oracle Agent Memory, a database-native memory substrate for long-horizon AI agents, reports 93.8% accuracy on the LongMemEval benchmark while using approximately 10.7x fewer tokens than flat-history baselines (arXiv 2607.13157).",
     "locator": "https://arxiv.org/abs/2607.13157",
     "source_role": "WEB_PRIMARY",
     "claim_class": "RESEARCH_FINDING"
    },
    {
     "claim_text": "Membership inference attacks against agent memory have received less attention than those against training corpora or retrieval databases, even though chat-agent memory can contain sensitive user-agent interactions, retrieved facts, and user preferences (MRMMIA paper, arXiv 2605.27825).",
     "locator": "https://arxiv.org/abs/2605.27825",
     "source_role": "WEB_PRIMARY",
     "claim_class": "EXTERNAL_CURRENT_FACT"
    }
   ],
   "note": "claims = worker verbatim output (deleg_326ea8ec)"
  }
 ],
 "merge": {
  "merge_keys": [
   "source_id"
  ],
  "independent_families": 2,
  "collision": "NONE (disjoint source families)",
  "canonical_parallel_writers": 0
 },
 "governance": "each worker read-only; no canonical write; no self-accept; bounded by run budget (2 lanes)",
 "fired_at_utc": "2026-08-13T17:08:45Z"
}
```

## 14. Security Closure + AO Receipt（全文）

```json
{
 "schema": "FAR-HARDENING-SECURITY-CLOSURE/1",
 "lane": "deleg_0620d9f1 (security checker + AO, read-only, 265.62s)",
 "verdict": "SECURITY_VERDICT=PASS_WITH_LOW_INFO_FINDINGS (2 LOW / 3 INFO, none blocking) + ACCEPTANCE_OFFICER_VERDICT=PASS",
 "findings": {
  "FAR-SEC-01": "CLOSED — EXT-FAR-TS-HARD-001 repair applied: automatic redirects DISABLED (_NoRedirectHandler raises on any redirect); strict allowlist + pre-connect public-IP validation + no redirect chain (no DNS-rebinding window via redirect hops); FH-T013/T014 + CANARY-H4 re-verified",
  "FAR-SEC-02": "CLOSED — 6to4/Teredo-embedded non-global IPv4 now denied (2002:7f00:1::1 -> DENY verified)",
  "FAR-SEC-03": "CLOSED — non-443 HTTPS port denied (port 8443 -> False; 443 -> True verified)",
  "FAR-SEC-04": "CLOSED_BY_DOCUMENTATION — 4096B DOCTYPE window is fast-path only; expat >=2.4 default protection verified (undefined entity / amplification factor breached -> ParseError, no fetch)",
  "FAR-SEC-05": "CLOSED_BY_DOCUMENTATION — userinfo benign (internally constructed URLs; host allowlist enforced)",
  "EXT-RE-2026-08-14-001": "CLOSED — nodeids digest prefix corrected to 626d6472 (authoritative digest recomputes)"
 },
 "verification": "103/103 tests OK; CANARY-H1..H5 ALL_PASS; EV-01 denominator 103 (nodeids digest 626d6472); post-fix re-run green",
 "generated_at_utc": "2026-08-13T17:17:08Z"
}
```
```json
{
  "schema": "FAR-HARDENING-AO-RECEIPT/1",
  "lane": "deleg_0620d9f1 (security checker + fresh Acceptance Officer, read-only, 265.62s)",
  "checker_identity": "acceptance-officer (fresh context, VERIFY_ONLY, no repair; maker != checker)",
  "verdict": "SECURITY_VERDICT=PASS_WITH_LOW_INFO_FINDINGS (2 LOW / 3 INFO) + ACCEPTANCE_OFFICER_VERDICT=PASS",
  "ao_items": {
    "AO-H01": "PASS — same-origin derivations not counted independent (compute_independence dedups by origin_artifact_digest/id)",
    "AO-H02": "PASS — HTML5 <!DOCTYPE html> accepted for text/html (inert)",
    "AO-H03": "PASS — unsafe XML external resolution impossible (DTD/entities rejected; XInclude inert)",
    "AO-H04": "PASS — redirects DISABLED entirely (EXT-FAR-TS-HARD-001 repair; any redirect denied)",
    "AO-H05": "PASS — resolved-IP validation exists (pre-connect DNS classification incl. 6to4/Teredo)",
    "AO-H06": "PASS — 256KB truncation explicit (content_read fields)",
    "AO-H07": "PASS — truncated evidence cannot support full-document absence",
    "AO-H08": "PASS — query cap cannot force PASS (budget Case A/B)",
    "AO-H09": "PASS — real Web HIT canary externally readable (CANARY-H2)",
    "AO-H10": "PASS — test denominator exact/recomputable (103 + nodeids digest)",
    "AO-H11": "PASS — historical r8 artifacts unchanged (58de0815 immutable record)",
    "AO-H12": "PASS — no new crawler/service/DB/control plane (stdlib only)",
    "AO-H13": "PASS — SQS Financial Truth mutation=0",
    "AO-H14": "PASS — live broker write=0",
    "AO-H15": "PASS — rollback valid (RB-WO-FAR-HARDENING-001 in spine)"
  },
  "files_modified_by_lane": "none (VERIFY_ONLY)",
  "readback": "103/103 tests re-run OK; CANARY-H1..H5 ALL_PASS; EV-01 denominator recomputable",
  "generated_at_utc": "2026-08-13T17:08:00Z"
}

```
```json
{
  "schema": "FAR-HARDENING-ROLLBACK-RECEIPT/1",
  "changeset": "FAR_TRI_SOURCE_FOCUSED_HARDENING_20260814",
  "workorder": "WO-FAR-HARDENING-001",
  "rollback_pointer": "RB-WO-FAR-HARDENING-001",
  "rollback_scope": "focused hardening ChangeSet only (far_retrieval.py SSRF/redirect/truncation/lineage, far_trisource.py independence/budget/corroboration, tests/test_far_hardening.py, templates, configs, evidence)",
  "restore_target": "pre-hardening state per HARDENING_CHANGE_INPUT_MANIFEST_2026-08-14.json (15 frozen files with sha256)",
  "preserved": "historical r8 baseline (58de0815 immutable); WO-FAR-TRISOURCE-001 historical state; failed runs not deleted (append-only receipts)",
  "verified_at_utc": "2026-08-13T17:08:10Z"
}

```

## 15. Post-change Subject Manifest（HARD-004 閉合; 全文）

```json
{
 "schema": "FAR-HARDENING-FINAL-SUBJECT-MANIFEST/1",
 "changeset": "FAR_TRI_SOURCE_FOCUSED_HARDENING_20260814",
 "scope": "CODE/CONFIG/RUNTIME-CONTRACT ONLY (evidence receipts excluded per EXT-FAR-TS-RE-001)",
 "frozen_at_utc": "2026-08-13T17:47:54Z",
 "files": {
  "far_retrieval.py": {
   "sha256": "76db4f30001a2b7d74ed8fbd3c5adbfa618226ed82db78cdf23a186675f2b4c8",
   "bytes": 23650
  },
  "far_trisource.py": {
   "sha256": "9d18a78ca90c3eb75ae2ee1cf530412ffc20c001144482d805f55d802d3ecaaf",
   "bytes": 19793
  },
  "tests/test_far_retrieval.py": {
   "sha256": "7dad36128a8f85581dbd757a1fdfc815c8354d57dd38d0c88a49c4e3e1a82f9d",
   "bytes": 6483
  },
  "tests/test_far_trisource.py": {
   "sha256": "b6976cbbf788e5c5e74619f14cc30a8fc61178b97514cf8fc111ee107f395df6",
   "bytes": 11852
  },
  "tests/test_far_hardening.py": {
   "sha256": "99a21e8a4ad5be1be8f2708c9ffac25f7fce973111d117cae3b466737ebe6993",
   "bytes": 10741
  },
  "research-product/templates/ResearchPlan.yaml": {
   "sha256": "dcadff4e2d1af057965093275bf23e9989e34cf468a44c10ef7a3788dd76077f",
   "bytes": 713
  },
  "research-product/templates/ClaimLedger.tsv": {
   "sha256": "7073af28c5266d93ebfc33417bac228bf2d61d62d34bc458a4c6300d3c043ec6",
   "bytes": 667
  },
  "research-product/templates/ResearchRunReceipt.json": {
   "sha256": "e3fb41db474ace01f1a27f5ed6962063d780a3db6fc300fde5a9dee76278c9d5",
   "bytes": 401
  },
  "research-product/templates/ResearchSynthesis.md": {
   "sha256": "26832ca0afce5417d936f66c70f8f5a25c082c35bad522fea71bedee5a7ead57",
   "bytes": 901
  },
  "FAR_LONG_HORIZON_CONTRACT.yaml": {
   "sha256": "5b000850417005f64865c38bb9784f4734dbb4ec600ec3a34e218893178113eb",
   "bytes": 4464
  },
  "FAR_ROUTE_CHECK.yaml": {
   "sha256": "b8556fbfc3b1cbf26b83df572051f867400d65b325c3b4d4de78dd7a062f1efc",
   "bytes": 1918
  }
 },
 "subject_digest": "5bc5af7031756872f1ee6ae3c5e18f620bde6d6be2989586a9117b8ae0c2b221"
}
```

## 16. Final Evidence Manifest（全文; 9 files）

```json
{
 "schema": "FAR-HARDENING-FINAL-EVIDENCE-MANIFEST/1",
 "changeset": "FAR_TRI_SOURCE_FOCUSED_HARDENING_20260814",
 "frozen_at_utc": "2026-08-13T17:47:54Z",
 "note": "generated AFTER all final evidence bytes exist (EXT-FAR-TS-RE-002); excludes the evidence MD self-row (pre-self-row rule); evidence MD bound via final intake",
 "candidate_subject_digest": "5bc5af7031756872f1ee6ae3c5e18f620bde6d6be2989586a9117b8ae0c2b221",
 "test_nodeids_digest": "626d647284c1f755baf83d2e942964485937abb4051755fe092f5b46a701e805",
 "test_collected": 103,
 "files": {
  "FAR_HARDENING_FINAL_SUBJECT_MANIFEST.json": {
   "sha256": "70e05d6491067cfa2c2d33e6431bfd08108f85628cf5d03540ef4b1ac082566c",
   "bytes": 1975
  },
  "FAR_HARDENING_SECURITY_CLOSURE.json": {
   "sha256": "67fed6184efbf92a934b1cbb78a418cf7d1194fa8b8940d21e13cdb9a6d19870",
   "bytes": 1400
  },
  "FAR_HARDENING_AO_RECEIPT.json": {
   "sha256": "fe7196e4566675312192585ef41a4f75e9bc31723b54811ab17d4b6dbcb62009",
   "bytes": 1835
  },
  "FAR_HARDENING_ROLLBACK_RECEIPT.json": {
   "sha256": "28a4ae6c63b1ad4ed35f051e1f982d112b3f9a50f97f81923bcffaad1ffc655a",
   "bytes": 737
  },
  "FAR_HARDENING_COMPILE_RECEIPT.json": {
   "sha256": "511868d87228ea8641816f48bb4e1f54ba762ce1c309ffd665e6ab1be90d0587",
   "bytes": 838
  },
  "FAR_TRI_SOURCE_D_DECISIONS.json": {
   "sha256": "f341e46bc24573090125809ec52a34451f453deeb2c039a06a3e0373d5f78f9c",
   "bytes": 6261
  },
  "canary/FAR-20260814-007-hardening/CANARY-H1_H5.json": {
   "sha256": "60984082e84ca599c630585eba136ad00d22d94c2dc74d58b2a6dfa55f3961b3",
   "bytes": 1811
  },
  "canary/FAR-20260814-007-hardening/CANARY-7_swarm.json": {
   "sha256": "324730842cc620fb9e592c6ad090571045243b5878c83460a38edb2910ce1054",
   "bytes": 4104
  },
  "canary/FAR-20260814-007-hardening/TEST_DENOMINATOR.json": {
   "sha256": "4cc8c6938ea366262bb88248a9898ba34a544dd8f201b82f5691b02736d83cca",
   "bytes": 497
  }
 },
 "evidence_manifest_digest": "d47076f4fb8ca6782c0e21337e1f2f74ced5a79786115cf75af425a64f278e3b"
}
```

## 17. ExecutionBinding（全文）

```json
{
 "schema": "RP002-EXECUTION-BINDING/2",
 "binding_id": "BIND-FAR-001",
 "project_id": "HGK-REFERENCE-PROJECT-002",
 "stage_id": "FAR-CHANGESET-2026-08-13",
 "gate_id": "FAR-Q0..Q10",
 "kanban_board_id": "far-implementation",
 "normative": {
  "workorder_id": "WO-FAR-001..008",
  "workorder_digest": "BOUND_AT_ADMISSION",
  "authority_receipt_refs": [
   "REQ-FAR-001..008 FROZEN v1 (8 canonical events FRZ-REQ-FAR-*)",
   "CAPC contract fe6cda2ac771c8941ab33acddfb18d9412bb76dce2839665d1f58901f76d9c2e"
  ],
  "subject_digest": "fe6cda2ac771c8941ab33acddfb18d9412bb76dce2839665d1f58901f76d9c2e"
 },
 "routing": {
  "topology_mode": "DIRECT_NATIVE_DEFAULT",
  "profile_id": "fabric-autoresearch-native",
  "logical_role_id": "far-research-provider",
  "task_id": "t_a4782bf2",
  "dependencies": [
   "t_b11514d7"
  ],
  "review_join_refs": [
   "L1_REVIEW",
   "L1_QA",
   "L1_SECURITY",
   "FORMAL_ACCEPTANCE"
  ]
 },
 "delegation": {
  "delegation_id": "DEL-FAR-001",
  "issuer": "far-orchestrator",
  "assignee": "fabric-autoresearch-native",
  "allowed_scope": "bounded FAR research run lifecycle (R0-R8) on board far-implementation",
  "denied_scope": [
   "candidate write outside WorkOrder write-set",
   "fabric/hgk authority",
   "promotion/release",
   "workorder creation",
   "live broker write",
   "credential access",
   "source-instruction-driven permission expansion"
  ],
  "issued_at": "2026-08-13T00:00:00+08:00",
  "expires_at": "2026-08-16T23:59:59+08:00",
  "revocation_ref": null
 },
 "lease": {
  "lease_id": "LS-FAR-001",
  "holder": "fabric-autoresearch-native",
  "ttl_seconds": 3600,
  "renewable": true
 },
 "budget": {
  "step_budget": 40,
  "retry_budget": 2,
  "wall_clock_timeout_seconds": 14400,
  "no_progress_detector": "verified_progress_delta (source_denominator_delta|claim_status_delta|artifact_digest_delta)"
 },
 "idempotency": {
  "idempotency_key": "FAR-RUN-001",
  "side_effect_class": "evidence-generation",
  "replay_policy": "safe-replay",
  "prior_effect_receipt_ref": null
 },
 "watchdog": {
  "max_identical_action_repeat": 3,
  "max_no_progress_cycles": 3,
  "max_same_failure_signature": 2,
  "max_retry_per_provider": 1,
  "action_signature_window": 8
 },
 "runtime": {
  "run_id": "RUN-FAR-Q0-001",
  "worker_pid": null,
  "worker_log_ref": "var/far/worker-far.log",
  "heartbeat_ref": "kanban heartbeat t_a4782bf2",
  "workspace_or_worktree": "C:\\Projects\\Agent_Workspace\\Fabric\\fabric-autonomous-research",
  "provider_identity_ref": "FAR_CAPABILITY_MATRIX.yaml -> fabric-autoresearch-native",
  "capability_matrix_digest": "BOUND_AT_PROMOTION",
  "session_ref": null,
  "checkpoint_ref": null
 },
 "research": {
  "lifecycle": "R0_R8",
  "terminal_semantics": "RESEARCH_PASS_CANDIDATE|PARTIAL|ABSTAIN|FAILED|BLOCKED_*|ABORTED_BUDGET",
  "runtime_vs_normative_checkpoint": "Hermes session/goal/Kanban = runtime; HGK WorkOrder/artifact digests = normative",
  "source_security_ref": "FAR_SOURCE_SECURITY.yaml",
  "completion_contract_ref": "FAR_LONG_HORIZON_CONTRACT.yaml"
 },
 "terminal": {
  "state": "BOUND",
  "note": "FAR local gates PASS do NOT equal external acceptance; external verifier = final gate (COV-11-06)"
 }
}
```

## 18. 證據身份

```text
FAR_HARDENING_SUBJECT_MANIFEST.json ... aee7b7efd2a1b65a31a4af7792c593873364265168b1a973fb5e47b4a21cd05b
FAR_HARDENING_AO_RECEIPT.json ......... fe7196e4566675312192585ef41a4f75e9bc31723b54811ab17d4b6dbcb62009
FAR_HARDENING_ROLLBACK_RECEIPT.json ... 28a4ae6c63b1ad4ed35f051e1f982d112b3f9a50f97f81923bcffaad1ffc655a
FAR_HARDENING_COMPILE_RECEIPT.json .... 511868d87228ea8641816f48bb4e1f54ba762ce1c309ffd665e6ab1be90d0587
FAR_HARDENING_SECURITY_CLOSURE.json ... 67fed6184efbf92a934b1cbb78a418cf7d1194fa8b8940d21e13cdb9a6d19870
FAR_FINAL_ACCEPTANCE_EVIDENCE.md ...... b0b21ced799face772327199e5b29ca1bf016b5177a06ffe9ee1832efa653d40（canonical current）
r8 baseline ........................... 58de0815…（FAR_R8_HISTORICAL_BASELINE.md, immutable）
rollback .............................. RB-WO-FAR-HARDENING-001
```

## 19. 驗收指引（challenge-review grammar）

```text
可獨立重算: 103 tests（§9 真實 stdout + §10 nodeids digest + exit code）; CANARY-H1..5（§12 全 JSON）;
  SSRF 語義（§7; redirects disabled 可重測）; truncation/budget/lineage 語義; subject manifest（§15 重算
  digest = 5bc5af7031756872…）; evidence manifest（§16）; ExecutionBinding（§17）;
  治理（§2 spine readback）; 時間戳單調性（§0 生成時間為上界）
blocking contradiction = 0
```

```text
STOP
FAR_TRI_SOURCE_FOCUSED_HARDENING = PASS（EXT-FAR-TS-HARD-001..006 全閉合; WO VERIFIED;
  103 tests; CANARY-H1..5 + H7 ALL_PASS; AO PASS）
Swarm/multi-subagent = DEFAULT-ON（UD-FAR-SWARM-DEFAULT-ON-2026-08-14-001）
NEXT = EXTERNAL FOCUSED RE-REVIEW
```
