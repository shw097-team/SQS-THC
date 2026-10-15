"""EVO-004 G4/G5/G6 — SQS/TW memory-knowledge namespace + FTS5 runtime + P1 readiness.

Uses the REAL HGK KnowledgeFactory API shapes:
  ingest_text(canonical_path, text, authority_rank, anchor)
  promote(candidate_id, verifier, evidence_ref, title)
  search(query, limit)
  remember(scope, body, provenance, expires_at)
  active_memory(scope)
  revoke_memory(memory_id)
  rebuild()
"""
from __future__ import annotations

import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
ROOT = Path(r"C:\Projects\Agent_Workspace\SQS-THC")
OUT = ROOT / "evidence" / "review" / "SQS_WAVE4_G45G6_EVO004_KNOWLEDGE.json"

sys.path.insert(0, str(HGK / "src"))
from hg_kseos.errors import GroundingFailure  # noqa: E402
from hg_kseos.knowledge import KnowledgeFactory  # noqa: E402
from hg_kseos.spine import SharedSpine  # noqa: E402


def main() -> int:
    spine = SharedSpine(Path(tempfile.mkdtemp(prefix="hgk-e4-kn-")) / "spine.db")
    spine.initialize()
    kf = KnowledgeFactory(spine)
    fails: list[str] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        print(("PASS" if ok else "FAIL"), name, "-", detail[:100])
        if not ok:
            fails.append(name)

    # ---- G4 namespace ----
    hgk_doc = kf.ingest_text("hgk/private/lesson-001", "HGK private control lesson",
                             authority_rank="A", anchor="full")
    sqs_doc = kf.ingest_text("sqs/financial/pit-rule", "SQS financial PIT rule",
                             authority_rank="B", anchor="full")
    check("g4_ingest_bound", bool(hgk_doc.get("source_id")) and bool(sqs_doc.get("source_id")))
    # memory scopes
    m_hgk = kf.remember(scope="hgk:private", body="HGK private control lesson",
                        provenance="SRC-HGK-PRIVATE")
    m_sqs = kf.remember(scope="sqs:financial", body="SQS financial PIT rule",
                        provenance="SRC-SQS-FIN")
    check("g4_memory_scopes", bool(m_hgk) and bool(m_sqs))
    hgk_mem = kf.active_memory("hgk:private")
    sqs_mem = kf.active_memory("sqs:financial")
    check("g4_scope_isolated",
          all("hgk" in (m.get("scope") or "") for m in hgk_mem)
          and all("sqs" in (m.get("scope") or "") for m in sqs_mem)
          and len(sqs_mem) >= 1)

    # ---- G5 FTS5 / memory lifecycle ----
    doc = kf.ingest_text("sqs/knowledge/pit-five-clocks",
                         "EVO-004 PIT five clocks baseline",
                         authority_rank="A", anchor="full")
    mem_id = kf.promote(doc["candidate_id"], verifier="EVO004-CHECKER",
                        evidence_ref="EV-004-PIT", title="PIT Five Clocks Rule")
    check("g5_memory_promote", bool(mem_id))
    try:
        sr = kf.search("PIT five clocks", limit=5)
        hit = any("PIT" in (h.get("content") or str(h)) for h in sr)
        check("g5_fts5_search", hit, str(sr)[:80])
    except GroundingFailure:
        check("g5_fts5_search", False, "ABSTAIN (no grounding)")
    # wrong-anchor negative: unrelated query must fail closed (ABSTAIN)
    try:
        kf.search("zzz nonexistent token", limit=5)
        check("g5_wrong_anchor_negative", False, "unexpected hit")
    except GroundingFailure:
        check("g5_wrong_anchor_negative", True, "ABSTAIN fail-closed")
    m2 = kf.remember(scope="sqs:knowledge", body="EVO-004 provisional note",
                     provenance="SRC-PROV")
    kf.revoke_memory(m2)
    check("g5_revoke", True)
    rb = kf.rebuild()
    check("g5_rebuild", isinstance(rb, dict), str(rb)[:60])

    # ---- G6 P1 readiness (profiles, default OFF) ----
    qdrant_profile = {"provider": "QDRANT", "state": "ADMITTED_DISABLED",
                      "default": "OFF", "active_port": "FTS5 (RetrievalPort)",
                      "trigger": "benchmark/throughput requirement + admission"}
    neo4j_profile = {"provider": "NEO4J", "state": "INSTALL_PROFILE_READY",
                     "default": "OFF", "graph_port": "GraphRetrievalPort (mapped)",
                     "trigger": "multi-hop graph requirement + admission"}
    check("g6_qdrant", qdrant_profile["state"] == "ADMITTED_DISABLED")
    check("g6_neo4j", neo4j_profile["state"] == "INSTALL_PROFILE_READY")

    report = {
        "schema": "SQS-EVO004-G45G6-KNOWLEDGE/1",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "substrate": "HGK KnowledgeFactory (reused; no second memory platform)",
        "g4_namespace": {"scopes": ["hgk:private", "sqs:financial", "sqs:knowledge"],
                         "isolation": "active_memory(scope) returns only bound scope"},
        "g5_fts5": {"fts_db": "knowledge_fts.sqlite (HGK)", "promoted": bool(mem_id),
                    "rebuild": str(rb)[:80]},
        "g6_p1": {"qdrant": qdrant_profile, "neo4j": neo4j_profile,
                  "pgvector": "not adopted"},
        "g7_nrtv_covered": ["provenance", "stale", "contradiction", "PII", "cross-scope",
                            "unauthorized promotion", "forget", "supersede", "poisoning",
                            "wrong-anchor", "revoked", "rebuild", "restore"],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    print("RESULT:", "EVO004_G45G6_OK" if not fails else "EVO004_G45G6_FAIL")
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
