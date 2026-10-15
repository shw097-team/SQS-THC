"""SQS-THC TS-015｜Closed-book handoff and consumer ACK — WORK ORDER CONTRACT (TS-REF-015).

Source authority: SSOT/SQS-THC_P0-CIP-PACK_v2026.08.06-r2.md section 17 TS-015
(TS-015｜Closed-book handoff and consumer ACK).

Target files exact set (canonical root):
  handoff/gpt-b-command-pack.yaml; handoff/orochi-execution-packet.yaml; handoff/consumer-ack.ndjson

Tests (tests/test_ts015_*.py, unittest, pure stdlib): Closed-book handoff: handoff/gpt-b-command-pack.yaml (command pack), handoff/orochi-execution-packet.yaml (execution packet), handoff/consumer-ack.ndjson (consumer ACK ledger). Tests: positive (command pack complete, execution packet valid, ACK append-only); negative ERR_RECEIVER_CONTEXT_MISSING (ACK without receiver context); edge (empty ACK ledger allowed; missing required field rejected).

Rules: write ONLY the listed targets + the test file; deterministic, fail-closed;
no broker write; no network. Commit message 'feat(csb): WO-TS-REF-015 TS-015｜Closed-book handoff and consumer ACK (TS-015)'.
Run: python -m unittest discover -s tests -t . (PYTHONPATH=src); baseline 53 tests stay green.
"""
