"""SQS-THC TS-012｜Evidence/release/learning/NRTV — WORK ORDER CONTRACT (TS-REF-012).

Source authority: SSOT/SQS-THC_P0-CIP-PACK_v2026.08.06-r2.md section 17 TS-012
(TS-012｜Evidence/release/learning/NRTV).

Target files exact set (canonical root):
  docs/DOC-12.md; evidence/; release/; migration/; nrtv/; training/

Tests (tests/test_ts012_*.py, unittest, pure stdlib): Evidence/release/learning/NRTV: docs/DOC-12.md; evidence/ (evidence ledger), release/ (release gates), migration/ (migration plans), nrtv/ (NRTV config), training/ (training runs). Tests: positive (evidence ledger append-only, release gate validates, NRTV config valid); negative ERR_PRODUCTION_CLAIM_INFLATION (claiming production without NRTV/evidence); edge (empty evidence allowed; missing required field rejected).

Rules: write ONLY the listed targets + the test file; deterministic, fail-closed;
no broker write; no network. Commit message 'feat(csb): WO-TS-REF-012 TS-012｜Evidence/release/learning/NRTV (TS-012)'.
Run: python -m unittest discover -s tests -t . (PYTHONPATH=src); baseline 53 tests stay green.
"""
