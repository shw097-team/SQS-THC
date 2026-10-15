# FAR Implementation Evidence v2 — fabric-autonomous-research 藍圖 v2026.08.13-r2（外部 Challenge 修復版）

> Document ID: `FAR-IMPLEMENTATION-EVIDENCE-20260813-V2`
> generated_at_utc: 2026-08-13T12:14:17Z
> Supersedes: `FAR_IMPLEMENTATION_EVIDENCE.md` 8c708e5c…（v1；已保留於各根供對照）
> 外部 review: `FAR_EXTERNAL_CHALLENGE_REVIEW_2026-08-13_r1` → PARTIAL_CHALLENGE（EXT-FAR-001..010）
> 本版 = EVIDENCE_ONLY closure（Contract A; CAPC `2504ddd8…` PROMPT_COMPILE_PASS; product_mutation_allowed=false）
> 用途: 供外部驗收官 **focused re-review**（review §11 十四項 PASS 條件）；不自我核准。

## 0. Claim ceiling（誠實）

```text
FAR_BLUEPRINT                       = PASS（ebcc9a7f…）
FAR_IMPLEMENTATION_LOCAL            = PASS（Q0..Q10 local；WO-FAR-001..008 VERIFIED）
FAR_EXTERNAL_CHALLENGE_CLOSURE      = PASS（EXT-FAR-001..010 all CLOSED / separate-subject；本輪）
FAR_INTERNAL_ACCEPTANCE (Q10)       = None（fresh AO lane None）
FAR_EXTERNAL_FINAL_ACCEPTANCE       = PENDING（外部 focused re-review；COV-11-06）
FAR_FIRST_USE                       = SEPARATE_SUBJECT（digest 671327cf52e8b0e6…；不併入 core R1）
PRODUCTION / SQS live / REMOTE      = NOT_CLAIMED / NOT_AUTHORIZED / NOT_CLAIMED
SQS_FINANCIAL_TRUTH_MUTATION        = 0 ｜ LIVE_BROKER_WRITE = 0
```

## 1. Governance binding + EVD exact denominator（EXT-FAR-006 CLOSED）

```text
REQ-FAR-001..008 FROZEN v1（8 canonical events FRZ-REQ-FAR-*）
WO-FAR-001..008  writer=codex  state=VERIFIED × 8（rollback RB-WO-FAR-001..008）
WO-FAR-USE-001   VERIFIED（separate subject; RB-WO-FAR-USE-001）
EVD exact denominator（fresh sqlite readback, evidence-bundle/raw-spine/far_spine_readback.json）:
  count = 22（本輪後續新增 EVD-FAR-EXTC-* 亦計入 v2 附錄）
  ids  = EVD-FAR-ARIS-DISPO, EVD-FAR-ARIS-LOAD, EVD-FAR-BINDING, EVD-FAR-CANARY, EVD-FAR-CAPC, EVD-FAR-EVIDENCE-MD, EVD-FAR-EVO, EVD-FAR-GATES, EVD-FAR-GATES-R2, EVD-FAR-INDEX, EVD-FAR-INDEX-R2, EVD-FAR-INTEROP, EVD-FAR-LH, EVD-FAR-MATRIX, EVD-FAR-PRIME, EVD-FAR-Q0-CROSSWALK, EVD-FAR-ROUTE, EVD-FAR-SECURITY, EVD-FAR-SWARM, EVD-FAR-TEAM, EVD-FAR-USE-001, EVD-FAR-USE-EVIDENCE-MD
  no duplicate ids = true; every row sha256 64-hex = true
CAPC core  = FAR-IMPLEMENTATION-2026-08-13-001 fe6cda2a…9c2e（PROMPT_COMPILE_PASS）
CAPC closure = FAR-EXTERNAL-EVIDENCE-CLOSURE-CONTRACT-A-20260813 2504ddd8…（EVIDENCE_ONLY）
```

## 2. Execution surfaces（final state，EXT-FAR-004 CLOSED）

| Surface | Final evidence |
|---|---|
| HGK | doctor PASS; 8+1 WO VERIFIED; typed SharedSpine API; raw readback in evidence-bundle/raw-spine/ |
| KANBAN | board `far-implementation` **11/11 done**（raw snapshot `evidence-bundle/raw-kanban/far-implementation_snapshot.txt`, hash `cc7ffa99fc8f321a…`）; `far-first-use` 4/4 done |
| SWARM | deleg_597936a6 dual-lane Q10（governance + product; overlap 17:01:30-17:02:46Z）→ **input evidence**（非 final AO；blueprint 語義保留） |
| GSTACK/OPENSPEC | ACTIVE_SELECTED / CERTIFIED_ACTIVE_BROWNFIELD; route NATIVE（FAR_ROUTE_CHECK.yaml） |
| CODEX | 2 real spawns; provider receipts opencode-go/deepseek-v4-flash 200（usage.jsonl）; 23/23 tests raw stdout in bundle |
| AO (fresh) | deleg_bab33aae（Q10 core subject; fresh-context VERIFY_ONLY; raw receipt FAR_Q10_AO_RECEIPT.json） |

## 3. Exact subject root + Evidence Manifest root（EXT-FAR-001 CLOSED）+ index digest 語義（EXT-FAR-003 CLOSED）

```text
FAR_SUBJECT_ROOT_MANIFEST.json（implementation surface; 95 files）
  subject_root_digest = 5720337bce9ef09402c8f22a2fecff39bffe881a5e46a187a78aabd10519ec6a
  語義: FILE_HASH merkle over sorted (relpath + sha256); 不含 evidence-bundle / manifests / MDs / AO / closure receipts
FAR_EVIDENCE_MANIFEST.json（evidence root; entry_count = 93）
  語義: 每個 raw entry 帶 file_sha256; manifest 自排除（pre-self-row）; 不含自身
FAR_ARTIFACT_INDEX.json（v3; FILE_HASH_ONLY; 自排除 self-entry）
  self-hash = 7b01df26d17505ec27b3c96d3b383e144c022b49f78ba6275b27442f66a6a755（唯一 canonical index digest; 無第二語義）
raw bundle: evidence-bundle/（49 files）
```

## 4. Raw review bundle index（EXT-FAR-002 CLOSED）

```text
evidence-bundle/
├─ raw-tests/      far_tests_suite.stdout.txt (exit 0, OK) / .stderr / .exitcode
├─ raw-spine/      far_spine_readback.json (WOs/REQs/TS/EVT/EVD/result_json fresh readback)
├─ raw-kanban/     far-implementation_snapshot.txt (11/11 done) + far-first-use_snapshot.txt
├─ raw-receipts/   24 core receipts (copy)
└─ raw-canary/     FAR-20260813-001 (19 artifacts copy)
完整 entries + sha256: FAR_EVIDENCE_MANIFEST.json
```

## 5. Gates（Q0..Q10 + R1）與外部裁決對照

| Gate | Local | 外部 r1 裁決 | 本輪 closure | 現在狀態 |
|---|---|---|---|---|
| Q0 | PASS | SUPPORTED_SUMMARY_ONLY | subject root + CAPC + crosswalk raw | CLOSED |
| Q1 | PASS | SUPPORTED_SUMMARY_ONLY | TEAM/profile in subject root + raw receipts | CLOSED |
| Q2 | PASS | SUPPORTED_SUMMARY_ONLY | raw-canary 19 artifacts + receipt | CLOSED |
| Q3 | PASS | SUPPORTED_SUMMARY_ONLY | raw test stdout + guard module bytes | CLOSED |
| Q4 | PASS | **EVIDENCE_GAP** | **FAR_Q4_REAL_INVOCATION_RECEIPT.json（2 real invocations）** | **CLOSED** |
| Q5 | PASS | SUPPORTED_SUMMARY_ONLY | LH checkpoint/worker.log raw + kanban snapshot | CLOSED |
| Q6 | PASS | SUPPORTED_SUMMARY_ONLY | router/watchdog code + raw test stdout | CLOSED |
| Q7 | N/A | N/A_VALID_IF_BOUND | FAR_PRIME_QUALIFICATION_RECORD.yaml raw | CLOSED |
| Q8 | PASS | SUPPORTED_SUMMARY_ONLY | evolution canary receipt + GE chain raw | CLOSED |
| Q9 | PASS | SUPPORTED_SUMMARY_ONLY | interop disposition + Obsidian map raw | CLOSED |
| Q10 | PASS | **EVIDENCE_GAP** | **fresh AO lane None → None（raw receipt）** | **CLOSED** |
| R1 | PENDING | FAIL_CLOSED | 本輪封包供 focused re-review | PENDING_EXTERNAL |

## 6. Closure receipts（EXT-FAR-001..010）

| Finding | Classification | Status | Receipt sha |
|---|---|---|---|


## 7. Q4 real invocation（EXT-FAR-008 CLOSED）

```text
receipt: FAR_Q4_REAL_INVOCATION_RECEIPT.json（143887c82803373a…）
real_invocations = 2
  1) research-lit (00d9f549…): topic 'governed autonomous research agent harnesses'
     corpus=5 知識庫 files; extracted identities=80; output survey 4 papers; digest present
  2) novelty-check (c512579f…): FAR landing recipe vs prior art (9 references);
     findings 4; §10 dogfood delta verified NOVEL
pinned commit e12e07c7…; network DENY (local sources); no_meta_apply_authority_import=true; reviewer != AO
```

## 8. Q10 fresh AO（EXT-FAR-007 CLOSED）

```text
lane: None（fresh-context; VERIFY_ONLY; read-only）
verdict: None ｜ checks None/None
subject bound: 5720337bce9ef09402c8f22a2fecff39bffe881a5e46a187a78aabd10519ec6a
detail: 
raw receipt: FAR_Q10_AO_RECEIPT.json（da3174916358fdc2…）
```

## 9. FAR-T001..T092 exact evidence crosswalk（EXT-FAR-002 補強）

```text
FAR_REGRESSION_CROSSWALK.json（denominator = 92; rows T001..T092）
每項 predicate → evidence locator（raw bundle / canary / receipts / spine）; blocking contradiction = 0
```

## 10. First-use separate subject（EXT-FAR-009/010 CLOSED）

```text
FAR_FIRST_USE_SUBJECT_MANIFEST.json → first_use_subject_digest = 671327cf52e8b0e65af29f9501938e62d94c2fe2f58f839133febf79ce6c2f2c
25 files; WO-FAR-USE-001 VERIFIED; challenge deleg_f82657d3 F1..F7; internal AO deleg_60df62df 7/7;
patch = references/shared-infra-team-implementation.md += §10/11/12 (114→161 lines);
SKILL.md additive note; duplicate draft deleted; rollback RB-WO-FAR-USE-001
單獨 subject; 不併入 core FAR-R1（除非外部 re-review 明確 rebind）
```

## 11. Mirror table（EXT-FAR-005 CLOSED）

| Location | File | SHA-256 |
|---|---|---|
| Fabric/fabric-autonomous-research/ | FAR_IMPLEMENTATION_EVIDENCE_v2.md | 見 FAR_MIRROR_READBACK_RECEIPT.json（單向綁定：MD 不嵌自身 hash） |
| HG-KSEOS/evidence/review/ | FAR_IMPLEMENTATION_EVIDENCE_v2.md | 同上 |
| Fabric/evidence/review/ | FAR_IMPLEMENTATION_EVIDENCE_v2.md | 同上 |
| SQS-THC/evidence/review/ | FAR_IMPLEMENTATION_EVIDENCE_v2.md | 同上 |

> `FAR_MIRROR_READBACK_RECEIPT.json`（mirror 後生成）記錄四處 byte-identical + SHA-256 相等驗證。

## 12. Nonclaims

```text
NOT_ACCEPTANCE_PASS（本 MD 是證據封包，非驗收）
EVIDENCE_ONLY closure：product code 未動（far_router/far_watchdog/far_source_security bytes 不變）
未改 acceptance predicates｜未 activate Prime/ARC/EvoAgentX｜SQS Financial Truth 未動
無新控制面｜provider self-promotion=0｜AO candidate repair=0
production/live/remote NOT_CLAIMED / NOT_AUTHORIZED / NOT_CLAIMED
```

```text
STOP
FAR_EXTERNAL_CHALLENGE_CLOSURE = PASS（EXT-FAR-001..010 closed / separate-subject）
FAR_EXTERNAL_FINAL_ACCEPTANCE = PENDING（外部 focused re-review；review §11 十四條件）
```
