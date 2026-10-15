"""SQS-THC TS-010｜Decision/XQ/reconciliation — WORK ORDER CONTRACT (TS-REF-010).

Source authority: SSOT/SQS-THC_P0-CIP-PACK_v2026.08.06-r2.md section 17 TS-010
(TS-010｜Decision/XQ/reconciliation).

Target files exact set (canonical root):
  docs/DOC-10.md; adapters/xq-read-watch.yaml; schemas/execution-fact.schema.json; reducers/book-of-record.yaml

Tests (tests/test_ts010_*.py, unittest, pure stdlib): Decision/XQ/reconciliation: docs/DOC-10.md; adapters/xq-read-watch.yaml (read-only watch adapter, no write); schemas/execution-fact.schema.json (execution fact schema); reducers/book-of-record.yaml (book-of-record reducer). Tests: positive (xq adapter read-only, execution-fact schema valid, book-of-record reduces); negative ERR_AUTONOMOUS_ORDER_PATH (any autonomous order write path must fail); edge (empty execution facts allowed; missing required field rejected).

Rules: write ONLY the listed targets + the test file; deterministic, fail-closed;
no broker write; no network. Commit message 'feat(csb): WO-TS-REF-010 TS-010｜Decision/XQ/reconciliation (TS-010)'.
Run: python -m unittest discover -s tests -t . (PYTHONPATH=src); baseline 53 tests stay green.
"""
