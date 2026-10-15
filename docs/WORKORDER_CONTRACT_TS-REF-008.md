"""SQS-THC TS-008｜ML/NLP/alternative data research — WORK ORDER CONTRACT (TS-REF-008).

Source authority: SSOT/SQS-THC_P0-CIP-PACK_v2026.08.06-r2.md section 17 TS-008
(TS-008｜ML/NLP/alternative data research).

Target files exact set (canonical root):
  docs/DOC-08.md; research/ml/; research/nlp/; research/alternative-data/; fixtures/models/

Tests (tests/test_ts008_*.py, unittest, pure stdlib): ML/NLP/alternative-data research: docs/DOC-08.md; research/ml/ (model cards with id/leakage_guard), research/nlp/ (nlp assets), research/alternative-data/ (alt data sources with licensing), fixtures/models/. Tests: positive (model card validates, leakage_guard present, alt-data license present); negative ERR_MODEL_LEAKAGE (training window leaks into test window, or alt-data without license); edge (empty model list allowed; missing required field rejected).

Rules: write ONLY the listed targets + the test file; deterministic, fail-closed;
no broker write; no network. Commit message 'feat(csb): WO-TS-REF-008 TS-008｜ML/NLP/alternative data research (TS-008)'.
Run: python -m unittest discover -s tests -t . (PYTHONPATH=src); baseline 53 tests stay green.
"""
