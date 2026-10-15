"""SQS-THC TS-013｜Legacy donor migration and regression — WORK ORDER CONTRACT (TS-REF-013).

Source authority: SSOT/SQS-THC_P0-CIP-PACK_v2026.08.06-r2.md section 17 TS-013
(TS-013｜Legacy donor migration and regression).

Target files exact set (canonical root):
  migration/donor-matrix.yaml; migration/cutover-plans/; tests/legacy-regression/; deprecation/

Tests (tests/test_ts013_*.py, unittest, pure stdlib): Legacy donor migration: migration/donor-matrix.yaml (donor->target mapping, single truth), migration/cutover-plans/ (cutover plans), tests/legacy-regression/ (legacy regression tests), deprecation/ (deprecation records). Tests: positive (donor matrix maps each donor once, cutover plan valid); negative ERR_SECOND_TRUTH_REINTRODUCED (duplicate donor target reintroduces second truth); edge (empty migration allowed; missing required field rejected).

Rules: write ONLY the listed targets + the test file; deterministic, fail-closed;
no broker write; no network. Commit message 'feat(csb): WO-TS-REF-013 TS-013｜Legacy donor migration and regression (TS-013)'.
Run: python -m unittest discover -s tests -t . (PYTHONPATH=src); baseline 53 tests stay green.
"""
