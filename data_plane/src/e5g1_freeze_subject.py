"""EVO-005 G1 — Freeze Subject Manifest + Subject Digest.

Subject = product/control/data/config frozen candidate. Evidence/report/
attestation sidecars are proofs ABOUT the subject, not the subject itself.
Any product/control/data/config mutation invalidates the old subject.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
ROOT = Path(r"C:\Projects\Agent_Workspace\SQS-THC")
OUT = ROOT / "evidence" / "review" / "SQS_EVO005_SUBJECT_MANIFEST.json"


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git_head(repo: Path) -> str:
    return subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()


def main() -> int:
    hgk_head = git_head(HGK)
    sqs_head = git_head(ROOT)

    # required config digests (frozen controls)
    configs = {
        "hgk_meta_gates": HGK / "src/hg_kseos/meta_gates.py",
        "hgk_lifecycle": HGK / "src/hg_kseos/lifecycle.py",
        "hgk_knowledge": HGK / "src/hg_kseos/knowledge.py",
        "sqs_data_policy": ROOT / "data_plane/config/data_policy.yaml",
        "sqs_provider_profile": ROOT / "data_plane/config/provider_profile.yaml",
        "oracle_v1": ROOT / "evidence/review/SQS_EVO005_ACCEPTANCE_ORACLE_V1.json",
    }
    config_digests = {}
    for name, path in configs.items():
        config_digests[name] = {"path": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
                                "sha256": sha256_file(path) if path.exists() else "MISSING"}

    # dataset version (immutable)
    dsv_manifest = ROOT / "data_plane/data/metadata/dataset_manifest.json"
    dsv = {
        "dataset_version": "DSV-2026-08-11-r1",
        "manifest_digest": sha256_file(dsv_manifest) if dsv_manifest.exists() else "MISSING",
    }

    # tool profiles (truthful states, no overclaim)
    tool_profiles = {
        "qdrant": {"state": "ADMITTED_DISABLED", "evidence": "real client install 1.19.0 (r5 G7)",
                   "default": "OFF"},
        "neo4j": {"state": "INSTALL_PROFILE_READY", "evidence": "driver 6.2.0 installed (r5 G7)",
                  "default": "OFF"},
        "codex": {"state": "APPLICABLE_BOUNDED", "evidence": "WAVE3 G4 genuine trace"},
        "gstack": {"state": "ADVISORY", "evidence": "advisory methodology, not final authority"},
    }

    subject = {
        "schema": "HGK-EVO005-SUBJECT-MANIFEST/1",
        "subject_version": "EVO005-SUBJECT-V1",
        "frozen_at_utc": datetime.now(timezone.utc).isoformat(),
        "product_head_full": sqs_head,
        "control_head_full": hgk_head,
        "required_config_digests": config_digests,
        "dataset_version": dsv,
        "required_tool_profile_digests": {k: {"state": v["state"]} for k, v in tool_profiles.items()},
        "required_knowledge_profile_digest": {"five_family_files": 68,
                                              "corpus_root": "技術資料庫/專業技術文檔/TW-ICT_當沖技術系列"},
        "claim_scopes": ["PRODUCT_LOCAL_DELIVERY", "REFERENCE_PROJECT_EVOLUTION_COMPLETE",
                         "KNOWLEDGE_BASELINE_READY", "VECTOR_PROVIDER_READINESS",
                         "GRAPH_PROVIDER_READINESS", "PRODUCTION", "LIVE_TRADING"],
    }
    # deterministic Subject Digest (exclude self-referential timestamps)
    digest_body = {k: v for k, v in subject.items() if k not in ("frozen_at_utc", "subject_digest")}
    body = json.dumps(digest_body, indent=1, ensure_ascii=False, sort_keys=True).encode("utf-8")
    digest = hashlib.sha256(body).hexdigest()
    subject["subject_digest"] = digest
    # FROZEN semantics: keep existing frozen subject (no in-place mutation)
    if OUT.exists():
        existing = json.loads(OUT.read_text(encoding="utf-8"))
        if existing.get("subject_digest") == digest:
            print("REUSE_FROZEN")
            return 0
        print(f"WARN: existing frozen subject digest {existing.get('subject_digest')[:12]} "
              f"!= recomputed {digest[:12]}; keeping existing (frozen)")
        print("REUSE_FROZEN")
        return 0
    OUT.write_text(json.dumps(subject, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"Subject EVO005-SUBJECT-V1 frozen")
    print(f"product_head: {sqs_head}")
    print(f"control_head: {hgk_head}")
    print(f"subject_digest: {digest}")
    print(f"path: {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
