"""SQS-THC TS-014｜Package/materialization/readback — WORK ORDER CONTRACT (TS-REF-014).

Source authority: SSOT/SQS-THC_P0-CIP-PACK_v2026.08.06-r2.md section 17 TS-014
(TS-014｜Package/materialization/readback).

Target files exact set (canonical root):
  MANIFEST.json; CHECKSUMS.sha256; READBACK_REPORT.md; STATUS_VECTOR.json; scripts/validate-package.py

Tests (tests/test_ts014_*.py, unittest, pure stdlib): Package/materialization/readback: MANIFEST.json (exact file set), CHECKSUMS.sha256 (sha256 per file), READBACK_REPORT.md, STATUS_VECTOR.json (status vector), scripts/validate-package.py (validator). Tests: positive (manifest+checksums validate, validator exit 0); negative ERR_PACKAGE_READBACK_MISMATCH (checksum mismatch detected); edge (empty package allowed; missing required field rejected).

Rules: write ONLY the listed targets + the test file; deterministic, fail-closed;
no broker write; no network. Commit message 'feat(csb): WO-TS-REF-014 TS-014｜Package/materialization/readback (TS-014)'.
Run: python -m unittest discover -s tests -t . (PYTHONPATH=src); baseline 53 tests stay green.
"""
