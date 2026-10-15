"""SQS-THC Investment mission and factor research — WORK ORDER CONTRACT (TS-REF-07).

Source authority: SSOT/SQS-THC_P0-CIP-PACK_v2026.08.06-r2.md section 17 TS-007
(Investment mission and factor research), owner F18-01.

Target files exact set (canonical root):
  docs/DOC-07.md              - investment mission & factor research document
  research/mission.yaml       - mission (mandate, non-goals, claim ceiling)
  research/universe.yaml      - tradable universe definition
  research/factors/           - factor definitions (at least: momentum, reversal,
                                liquidity — each with id/source/definition/guard)
  fixtures/research/          - fixtures for validation

Tests (tests/test_ts007_investment_research.py, unittest, pure stdlib):
  - positive: mission validates (mandate present, claim ceiling LOCAL), universe
    entries valid, factor IDs unique with source refs
  - negative: mandate violation raises ERR_MANDATE_VIOLATION (e.g. factor
    without source, universe entry without tradable flag)
  - edge: empty factors list allowed; missing required field rejected

Rules: write ONLY the listed targets + the test file; deterministic, fail-closed;
no broker write; no network. Commit message 'feat(csb): WO-TS-REF-07 investment
mission and factor research (TS-007)'. Run: python -m unittest discover -s tests -t .
"""
