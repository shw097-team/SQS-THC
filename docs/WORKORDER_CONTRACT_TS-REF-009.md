"""SQS-THC TS-009｜Validation/risk/survival veto — WORK ORDER CONTRACT (TS-REF-009).

Source authority: SSOT/SQS-THC_P0-CIP-PACK_v2026.08.06-r2.md section 17 TS-009
(TS-009｜Validation/risk/survival veto).

Target files exact set (canonical root):
  docs/DOC-09.md; validation/; risk/limits.yaml; survival/guards.yaml; fixtures/stress/

Tests (tests/test_ts009_*.py, unittest, pure stdlib): Validation/risk/survival veto: docs/DOC-09.md; validation/ (validation runs), risk/limits.yaml (hard limits), survival/guards.yaml (survival guards), fixtures/stress/ (stress fixtures). Tests: positive (limits validate, guards present, stress fixture runs); negative ERR_VETO_BYPASS (trying to bypass a hard limit or guard); edge (empty limits allowed; missing required field rejected).

Rules: write ONLY the listed targets + the test file; deterministic, fail-closed;
no broker write; no network. Commit message 'feat(csb): WO-TS-REF-009 TS-009｜Validation/risk/survival veto (TS-009)'.
Run: python -m unittest discover -s tests -t . (PYTHONPATH=src); baseline 53 tests stay green.
"""
