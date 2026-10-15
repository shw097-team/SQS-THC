"""EVO-005 G0 — Frozen Acceptance Oracle V1.

Versioned, frozen BEFORE any candidate mutation. In-place mutation forbidden:
any correction -> Oracle V2 (new version + reason + diff + GCF), V1 retained.

Oracle rows carry claim_scope + blocking, so optional tool readiness never
mistakenly blocks unrelated product claims.
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"C:\Projects\Agent_Workspace\SQS-THC")
OUT = ROOT / "evidence" / "review" / "SQS_EVO005_ACCEPTANCE_ORACLE_V1.json"

ORACLE_VERSION = "EVO005-ORACLE-V1"

REQUIREMENTS = [
    # (requirement_id, source_locator, claim_scope, required, blocking, applicability_rule,
    #  acceptance_predicate, evidence_depth, independent_checker_required, allowed_reuse, terminal_states)
    ("REQ-EVO005-ORACLE", "RESUME_..._EVO-005_r1.md#6/G0", "REFERENCE_PROJECT_EVOLUTION_COMPLETE",
     True, True, "always",
     "Oracle versioned+frozen before mutation; in-place mutation=0",
     "runtime+digest", True, "no", ["FROZEN"]),
    ("REQ-EVO005-SUBJECT", "RESUME_..._EVO-005_r1.md#6/G1", "REFERENCE_PROJECT_EVOLUTION_COMPLETE",
     True, True, "always",
     "Subject Manifest deterministic; Subject Digest bound; stale=0",
     "runtime+digest", True, "no", ["FROZEN"]),
    ("REQ-EVO005-GRAPH", "RESUME_..._EVO-005_r1.md#6/G2", "REFERENCE_PROJECT_EVOLUTION_COMPLETE",
     True, True, "always",
     "Canonical Evidence Graph; artifact full digest once; duplicate truth fields=0",
     "runtime", True, "no", ["PASS"]),
    ("REQ-EVO005-INTEGRITY", "RESUME_..._EVO-005_r1.md#6/G3", "REFERENCE_PROJECT_EVOLUTION_COMPLETE",
     True, True, "always",
     "cross-artifact semantic checks; r5 canaries all catch",
     "runtime", True, "no", ["PASS"]),
    ("REQ-EVO005-R5-TRUTH", "RESUME_..._EVO-005_r1.md#6/G4", "REFERENCE_PROJECT_EVOLUTION_COMPLETE",
     True, True, "always",
     "68/30/0 reconciled; project state terminal consistent",
     "runtime", True, "no", ["PASS"]),
    ("REQ-EVO005-RBWI", "RESUME_..._EVO-005_r1.md#6/G5", "PRODUCT_LOCAL_DELIVERY",
     True, True, "TW-ICT RBWI applicable",
     "current-subject full applicable RBWI acceptance",
     "runtime", True, "affected-only", ["PASS"]),
    ("REQ-EVO005-CALIBRATION", "RESUME_..._EVO-005_r1.md#6/G6", "KNOWLEDGE_BASELINE_READY",
     True, False, "claim-scope applicable",
     "provider/multi-agent truthful claim states; no overclaim",
     "runtime", True, "affected-only", ["PASS", "NOT_REQUIRED_FOR_CLAIM"]),
    ("REQ-EVO005-VERIFIER", "RESUME_..._EVO-005_r1.md#6/G7", "REFERENCE_PROJECT_EVOLUTION_COMPLETE",
     True, True, "always",
     "independent verifier reads Oracle+Subject+Graph+raw only; adversarial fixtures pass",
     "runtime", True, "no", ["PASS"]),
    ("REQ-EVO005-ATTESTATION", "RESUME_..._EVO-005_r1.md#6/G8", "REFERENCE_PROJECT_EVOLUTION_COMPLETE",
     True, True, "always",
     "Subject Attestation + derived views consistent with graph",
     "runtime", True, "no", ["PASS"]),
    ("REQ-EVO005-RELEASE", "RESUME_..._EVO-005_r1.md#6/G9", "REFERENCE_PROJECT_EVOLUTION_COMPLETE",
     True, True, "always",
     "package bound to subject digest; readback PASS; r6 rendered from graph",
     "runtime", True, "no", ["PASS"]),
    # product scope (revalidated on current subject)
    ("REQ-PROD-LOCAL-DELIVERY", "HGK-REFERENCE-PROJECT-001 r1-r5 lineage", "PRODUCT_LOCAL_DELIVERY",
     True, True, "always",
     "SQS full suite + HGK full suite + acceptance 161/161 + denominator all-0",
     "runtime", True, "affected-only", ["PASS"]),
    # knowledge baseline (revalidated on current subject)
    ("REQ-KNOWLEDGE-BASELINE", "RESUME_..._EVO-005_r1.md#6/G4", "KNOWLEDGE_BASELINE_READY",
     True, False, "five-family corpus required",
     "five-family projection semantic reconciliation; FTS actual rows>0; retrieval receipt",
     "runtime", True, "affected-only", ["PASS"]),
    # provider readiness (optional, non-blocking for product claim)
    ("REQ-QDRANT", "RESUME_..._EVO-005_r1.md#6/G6", "VECTOR_PROVIDER_READINESS",
     False, False, "benchmark/admission trigger",
     "truthful lifecycle state (ADMITTED_DISABLED only with full lifecycle)",
     "runtime", True, "affected-only", ["PASS", "DEGRADED_TRUTHFUL"]),
    ("REQ-NEO4J", "RESUME_..._EVO-005_r1.md#6/G6", "GRAPH_PROVIDER_READINESS",
     False, False, "relation-heavy trigger",
     "truthful install-profile state",
     "runtime", True, "affected-only", ["PASS", "INSTALL_PROFILE_READY"]),
]

CLAIM_SCOPES = [
    "PRODUCT_LOCAL_DELIVERY",
    "REFERENCE_PROJECT_EVOLUTION_COMPLETE",
    "KNOWLEDGE_BASELINE_READY",
    "VECTOR_PROVIDER_READINESS",
    "GRAPH_PROVIDER_READINESS",
    "PRODUCTION",
    "LIVE_TRADING",
]


def main() -> int:
    rows = []
    for (rid, src, scope, required, blocking, applicability, predicate,
         depth, indep, reuse, terminals) in REQUIREMENTS:
        rows.append({
            "requirement_id": rid, "source_locator": src, "claim_scope": scope,
            "required": required, "blocking": blocking, "applicability_rule": applicability,
            "acceptance_predicate": predicate, "evidence_depth": depth,
            "independent_checker_required": indep, "allowed_reuse": reuse,
            "terminal_states": terminals,
        })
    oracle = {
        "schema": "HGK-EVO005-ACCEPTANCE-ORACLE/1",
        "oracle_version": ORACLE_VERSION,
        "frozen_at_utc": datetime.now(timezone.utc).isoformat(),
        "claim_scopes": CLAIM_SCOPES,
        "requirements": rows,
        "mutation_policy": "in-place mutation forbidden; corrections -> new version + GCF",
    }
    # digest excludes timestamps so the frozen oracle is idempotent across re-runs
    digest_body = {k: v for k, v in oracle.items() if k not in ("frozen_at_utc", "oracle_digest")}
    body = json.dumps(digest_body, indent=1, ensure_ascii=False, sort_keys=True).encode("utf-8")
    digest = hashlib.sha256(body).hexdigest()
    oracle["oracle_digest"] = digest
    # FROZEN semantics: do not overwrite an existing frozen oracle (in-place
    # mutation forbidden; corrections require a new version)
    if OUT.exists():
        existing = json.loads(OUT.read_text(encoding="utf-8"))
        if existing.get("oracle_digest") == digest:
            print("REUSE_FROZEN")
            return 0
        print(f"WARN: existing frozen oracle digest {existing.get('oracle_digest')[:12]} "
              f"!= recomputed {digest[:12]}; keeping existing (frozen)")
        print("REUSE_FROZEN")
        return 0
    OUT.write_text(json.dumps(oracle, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"Oracle {ORACLE_VERSION} frozen: {len(rows)} requirements")
    print(f"digest: {digest}")
    print(f"path: {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
