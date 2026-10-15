# SQS-THC & TW-ICT FSDT-Stack — Final Evidence for Review r7 (EVO005 FINAL-GRAPH-FREEZE)

> Rendered ONLY from Final Attestation + Frozen Graph (EVO005 FINAL-GRAPH-FREEZE r1).
> Prior frozen lineage (read-only): r1-r6. **User uploads this r7 MD only.**

## A. Frozen Identities (single-root, exact full values)

| Item | Value |
|---|---|
| ACTIVE_ORACLE_VERSION | `EVO005-ORACLE-V1` |
| ACTIVE_ORACLE_DIGEST | `501732af709e3e789572c9edcba7b9fc01704c12cf743cdba081a613221d19ed` |
| ACTIVE_SUBJECT_VERSION | `EVO005-SUBJECT-V1` |
| ACTIVE_SUBJECT_DIGEST | `e546cc2c4eacf0cb4bbb259d717c1728b89ac6c579de94262db0f450f36eefc1` |
| SUBJECT_PRODUCT_HEAD | `c8b0f63d71b2eb7c961ca02e38a3ab8b673bef6e` |
| SUBJECT_CONTROL_HEAD | `c16c40ae633e1b2ba48c05a9b26b1672708d6066` |
| CURRENT_HGK_REPO_HEAD | `075475d2224984b3b6ae3d026d0c010587703d30` |
| CURRENT_SQS_REPO_HEAD | `67211068d21f4af2a873c1145e1a5ec3e110ed7e` |
| EVIDENCE_SIDECAR_HEAD | `67211068d21f4af2a873c1145e1a5ec3e110ed7e` (evidence commits are sidecars, not subject) |
| FINAL_GRAPH_GENERATION | `GEN-2f6a46fc3c56` |
| FINAL_GRAPH_ROOT_DIGEST | `6535d9cd214a8d3e33869c955c42450f92ed6e42b6c1581cca0cc971d1aad621` |
| FINAL_VERIFIER_VERSION | `EVO005-FINAL-VERIFIER-1.0` |
| FINAL_VERIFICATION_RECEIPT_SHA256 | `c3e31da9e2ca371e0e71e3c1bb78d9348d9fecef3a789feb3ddaf9ab639eb490` |
| FINAL_VERIFIER_RESULT | PASS |
| FINAL_ATTESTATION_VERSION | `EVO005-FINAL-ATTESTATION-1` |
| FINAL_ATTESTATION_RESULT | PASS |
| FINAL_PACKAGE | `C:\Projects\Agent_Workspace\SQS-THC\release\SQS-THC_EVO005F_LOCAL_DELIVERY.zip` |
| FINAL_PACKAGE_BYTES | 1655972692 |
| FINAL_PACKAGE_SHA256 | `3936aadf83c1fcec8bd537af30f50404487085df2e27db55138f448a68bc7501` |
| FINAL_PACKAGE_EXACT_SET | 955 |
| FINAL_PACKAGE_READBACK | PASS |
| DATASET_VERSION | `DSV-2026-08-11-r1` |

## B. Claim-Scope Verdicts

```text
PRODUCT_LOCAL_DELIVERY = SQS-THC_TW-ICT_FSDT_STACK_LOCAL_DELIVERY_PASS
REFERENCE_PROJECT_EVOLUTION_COMPLETE = HGK_REFERENCE_PROJECT_001_COMPLETE
KNOWLEDGE_BASELINE_READY = PASS
VECTOR_PROVIDER_READINESS = ADMITTED_DISABLED
GRAPH_PROVIDER_READINESS = INSTALL_PROFILE_READY
PRODUCTION = NOT_CLAIMED
LIVE_TRADING = NOT_AUTHORIZED
```

## C. Single-Root Consistency (from Final Attestation + Frozen Graph)

```text
r7.oracle_digest == attestation.oracle_digest: True
r7.subject_digest == attestation.subject_digest: True
r7.graph_root == attestation.graph_root: True
verifier.graph_root == attestation.graph_root: True
package.graph_root == attestation.graph_root: True
all_required_claims_terminal: true
project_state: DELIVERED (TERMINAL_ACCEPTED)
```

## D. Historical Roots Disposition (never final)

- `32bf12225372442a...` -> HISTORICAL_INTERMEDIATE (prior attestation/r6 root)
- `ec524f9e1db64097...` -> HISTORICAL_INTERMEDIATE (per-runner G3G4 graph)
- `3444451ccccdcfc9...` -> HISTORICAL_INTERMEDIATE (per-runner G7 graph)
- `37869f8789a1dd0c...` -> STALE (pre-fix r6 render root)

## E. Graph Lifecycle / Freeze Guards

```text
graph_lifecycle: FROZEN
final_graph_root_count: 1
append_after_freeze: 0 (rejected by freeze guard)
artifact_identity_conflicts: 0
cross_artifact_semantic_conflicts: 0
provenance_chronology: PASS (0 inversions, DAG acyclic)
attestation_before_dependency: 0 (attestation after verifier+package)
blocking_tt: 0
```

## F. Termination

```text
STATUS=HGK_REFERENCE_PROJECT_001_COMPLETE
PRODUCT_LOCAL_DELIVERY=SQS-THC_TW-ICT_FSDT_STACK_LOCAL_DELIVERY_PASS
PRODUCTION=NOT_CLAIMED
LIVE_TRADING=NOT_AUTHORIZED
```

---
*r7 rendered from Final Attestation + Frozen Graph only. r7's own SHA is
produced by independent raw-byte readback after freeze (no self-reference).
