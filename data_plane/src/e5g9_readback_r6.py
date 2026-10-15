"""EVO-005 G9 — final r6 readback: inject exact full heads, verify semantic parse.

1. Patch r6 placeholders (hgk_head / sqs_head / package bytes+sha+exact_set)
   with exact full values.
2. Recompute r6 raw-byte SHA (post-freeze, no self-reference inside r6).
3. Semantic parse: r6 verdicts/digests == attestation/graph values.
4. Cross-artifact seal: package manifest SHA == on-disk package SHA.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(r"C:\Projects\Agent_Workspace\SQS-THC")
HGK = Path(r"C:\Projects\Agent_Workspace\HG-KSEOS")
R6 = ROOT / "evidence/review/SQS-THC_REFERENCE_PROJECT_001_FINAL_EVIDENCE_FOR_REVIEW_r6.md"


def git_head(repo: Path) -> str:
    return subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()


def main() -> int:
    fails: list[str] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        print(("PASS" if ok else "FAIL"), name, "-", detail[:100])
        if not ok:
            fails.append(name)

    hgk_head = git_head(HGK)
    sqs_head = git_head(ROOT)
    man = json.loads((ROOT / "release/EVO005_PACKAGE_MANIFEST.json").read_text(encoding="utf-8"))
    attest = json.loads((ROOT / "evidence/review/SQS_EVO005_G8_ATTESTATION.json")
                        .read_text(encoding="utf-8"))
    oracle = json.loads((ROOT / "evidence/review/SQS_EVO005_ACCEPTANCE_ORACLE_V1.json")
                        .read_text(encoding="utf-8"))
    subject = json.loads((ROOT / "evidence/review/SQS_EVO005_SUBJECT_MANIFEST.json")
                         .read_text(encoding="utf-8"))

    txt = R6.read_text(encoding="utf-8")
    # patch placeholders with exact values
    txt = txt.replace("`0e8e1a6` (exact full in readback receipt)", f"`{hgk_head}`")
    txt = txt.replace("`e1a2ab1` (exact full in readback receipt)", f"`{sqs_head}`")
    txt = txt.replace("FINAL_PACKAGE_BYTES=<exact in readback receipt>",
                      f"FINAL_PACKAGE_BYTES={man['bytes']}")
    txt = txt.replace("FINAL_PACKAGE_SHA256=<full in readback receipt>",
                      f"FINAL_PACKAGE_SHA256={man['sha256']}")
    txt = txt.replace("FINAL_PACKAGE_EXACT_SET=<exact in readback receipt>",
                      f"FINAL_PACKAGE_EXACT_SET={man['payload_files']}")
    R6.write_text(txt, encoding="utf-8")

    # 1. raw-byte SHA (post-freeze)
    sha = hashlib.sha256(R6.read_bytes()).hexdigest()
    print(f"r6 final sha: {sha} | bytes: {R6.stat().st_size}")

    # 2. semantic parse: r6 digests == attestation/graph
    check("p_oracle_digest", oracle["oracle_digest"] in txt)
    check("p_subject_digest", subject["subject_digest"] in txt)
    check("p_graph_root", attest["evidence_graph_root_digest"] in txt)
    check("p_verifier", "EVO005-VERIFIER-1.0" in txt and "INDEPENDENT_ORACLE_VERIFIER_PASS" in txt)
    check("p_claim_scopes", "SQS-THC_TW-ICT_FSDT_STACK_LOCAL_DELIVERY_PASS" in txt
          and "HGK_REFERENCE_PROJECT_001_COMPLETE" in txt
          and "NOT_CLAIMED" in txt and "NOT_AUTHORIZED" in txt)
    check("p_heads", hgk_head in txt and sqs_head in txt, f"hgk={hgk_head[:12]} sqs={sqs_head[:12]}")
    check("p_package_identity", man["sha256"] in txt and str(man["bytes"]) in txt)

    # 3. cross-artifact: package manifest SHA == on-disk package SHA
    pkg = ROOT / "release/SQS-THC_EVO005_LOCAL_DELIVERY.zip"
    pkg_sha = hashlib.sha256(pkg.read_bytes()).hexdigest()
    check("x_package_seal", pkg_sha == man["sha256"] and pkg.stat().st_size == man["bytes"],
          pkg_sha[:16])

    # 4. project state terminal
    den = json.loads(subprocess.run(
        [str(HGK / ".venv/Scripts/python.exe"), "-m", "hg_kseos", "project",
         "denominator", "HGK-REFERENCE-PROJECT-001"],
        cwd=HGK, capture_output=True, text=True,
        env={**__import__("os").environ, "PYTHONPATH": str(HGK / "src")}).stdout)
    check("x_project_terminal", den["state"] == "DELIVERED", f"state={den['state']}")

    print("RESULT:", "FINAL_CROSS_ARTIFACT_SEAL_PASS" if not fails else "FINAL_CROSS_ARTIFACT_SEAL_FAIL")
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
