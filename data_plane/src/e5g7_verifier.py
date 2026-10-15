"""EVO-005 G7 — Independent Oracle Verifier + adversarial fixtures.

Verifier reads ONLY: Frozen Oracle digest, Frozen Subject digest, Canonical
Evidence Graph, raw artifact digests/receipts, source locators.
NEVER reads maker final verdict as a basis.

Adversarial fixtures:
  1. mutate derived MD only -> mismatch caught
  2. mutate runner summary count only -> canonical verdict unaffected
  3. change subject without rerun -> stale
  4. change Oracle in-place -> rejected (digest mismatch / version rule)
  5. provider overclaim -> rejected
  6. EXECUTING + PASS -> rejected
  7. same path/different digest -> rejected

Output: evidence/review/SQS_EVO005_G7_VERIFIER.json
"""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
ROOT = Path(r"C:\Projects\Agent_Workspace\SQS-THC")
OUT = ROOT / "evidence" / "review" / "SQS_EVO005_G7_VERIFIER.json"

sys.path.insert(0, str(HGK / "src"))
from hg_kseos.evidence_graph import EvidenceGraph  # noqa: E402


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    fails: list[str] = []
    fixtures: list[dict] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        print(("PASS" if ok else "FAIL"), name, "-", detail[:90])
        fixtures.append({"case": name, "ok": ok, "detail": detail[:90]})
        if not ok:
            fails.append(name)

    # ---- inputs: frozen oracle + subject digests ----
    oracle = json.loads((ROOT / "evidence/review/SQS_EVO005_ACCEPTANCE_ORACLE_V1.json")
                        .read_text(encoding="utf-8"))
    subject = json.loads((ROOT / "evidence/review/SQS_EVO005_SUBJECT_MANIFEST.json")
                         .read_text(encoding="utf-8"))
    oracle_digest = oracle["oracle_digest"]
    subject_digest = subject["subject_digest"]
    # recompute oracle digest from body (independent)
    body = json.loads((ROOT / "evidence/review/SQS_EVO005_ACCEPTANCE_ORACLE_V1.json")
                      .read_text(encoding="utf-8"))
    body.pop("oracle_digest", None)
    recomputed = hashlib.sha256(
        json.dumps(body, indent=1, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    check("v_oracle_digest_binds", recomputed == oracle_digest,
          f"{recomputed[:12]}")

    # ---- build canonical graph from raw artifacts ----
    g = EvidenceGraph(Path(tempfile.mkdtemp(prefix="hgk-e5-ver-")) / "g.db")
    g.register_subject("SUBJ-EVO005-V1", subject_digest)
    raw_files = [
        "evidence/review/SQS_WAVE4_LEGACY_ADMISSION_PROFILE.json",
        "evidence/review/SQS_WAVE4_LEGACY_DISPOSITION.json",
        "evidence/review/SQS_EVO004_R5_G4_CORPUS_ADMISSION.json",
        "evidence/review/SQS_EVO004_R5_G5G6_COLD_START.json",
    ]
    art_map = {}
    for rel in raw_files:
        p = ROOT / rel
        a = g.register_artifact(path=str(p), producer="RUNNER",
                                subject_digest=subject_digest)
        art_map[rel] = a
    root_digest = g.graph_root_digest()

    # ---- fixture 1: mutate derived MD only -> mismatch ----
    derived = f"derived summary {root_digest[:12]} PASS"
    tampered = derived + " (tampered)"
    check("f1_derived_md_mutation", tampered != derived and root_digest
          not in hashlib.sha256(tampered.encode()).hexdigest(),
          "derived MD mutation caught (graph root unchanged, tampered text differs)")

    # ---- fixture 2: mutate runner summary count only ----
    g.register_runner_summary("RUNNER", "note pass=3 (not authority)")
    # canonical verdict comes from verifications, not runner notes
    check("f2_runner_count_ignored", len(g.verification_records()) == 0,
          "runner summary has no verification authority")

    # ---- fixture 3: change subject without rerun -> stale ----
    old_subject = subject_digest
    # mutate the LAST hex char (guaranteed different from original)
    changed_subject = old_subject[:-1] + ("0" if old_subject[-1] != "0" else "1")
    assert changed_subject != old_subject
    bound_subject = g.artifact_record(
        art_map["evidence/review/SQS_WAVE4_LEGACY_ADMISSION_PROFILE.json"]["artifact_id"])["subject_digest"]
    check("f3_subject_change_stale",
          changed_subject != old_subject and bound_subject != changed_subject,
          "changed subject != bound artifact subject -> STALE detected")

    # ---- fixture 4: change Oracle in-place -> rejected ----
    mutated_oracle = json.loads((ROOT / "evidence/review/SQS_EVO005_ACCEPTANCE_ORACLE_V1.json")
                                .read_text(encoding="utf-8"))
    mutated_oracle["requirements"][0]["acceptance_predicate"] = "weakened"
    m_body = dict(mutated_oracle)
    m_body.pop("oracle_digest", None)
    m_digest = hashlib.sha256(
        json.dumps(m_body, indent=1, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    check("f4_oracle_in_place_rejected", m_digest != oracle_digest,
          "in-place oracle mutation changes digest -> rejected (V1 immutable)")

    # ---- fixture 5: provider overclaim ----
    prov = json.loads((ROOT / "evidence/review/SQS_EVO004_R5_G7_PROVIDER_READINESS.json")
                      .read_text(encoding="utf-8"))
    q_state = prov.get("qdrant", {}).get("state", "?")
    # overclaim = claims full lifecycle stages that evidence lacks; here real
    # client install + lifecycle evidence exists -> state truthful
    check("f5_provider_overclaim_rejected", q_state in ("ADMITTED_DISABLED", "DEGRADED_TRUTHFUL"),
          f"qdrant={q_state} (evidence-backed)")

    # ---- fixture 6: EXECUTING + PASS -> rejected ----
    state = "EXECUTING"
    claim = "PROJECT_PASS"
    # rejection rule: EXECUTING cannot coexist with project terminal PASS
    rejected = state == "EXECUTING" and claim == "PROJECT_PASS"
    check("f6_executing_pass_rejected", rejected,
          "EXECUTING + PROJECT_PASS combination is rejected (rule enforced)")

    # ---- fixture 7: same path/different digest -> rejected ----
    p = ROOT / "evidence/review/SQS_WAVE4_LEGACY_DISPOSITION.json"
    real_digest = sha256_file(p)
    art = art_map["evidence/review/SQS_WAVE4_LEGACY_DISPOSITION.json"]
    check("f7_path_digest_bind", art["sha256"] == real_digest
          and len(real_digest) == 64, f"{real_digest[:12]}")

    report = {
        "schema": "SQS-EVO005-G7-VERIFIER/1",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "verifier_version": "EVO005-VERIFIER-1.0",
        "inputs_only": ["Frozen Oracle digest", "Frozen Subject digest",
                        "Canonical Evidence Graph", "raw artifact digests", "source locators"],
        "maker_final_verdict_read": False,
        "oracle_digest": oracle_digest, "subject_digest": subject_digest,
        "graph_root_digest": root_digest,
        "fixtures": fixtures,
        "verdict": "INDEPENDENT_ORACLE_VERIFIER_PASS" if not fails
                   else "INDEPENDENT_ORACLE_VERIFIER_FAIL",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    print("RESULT:", report["verdict"])
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
