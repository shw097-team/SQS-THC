# WAVE3 G4 — Data quality analysis card (Codex bounded, read-heavy)

- Type: CODING_CARD (read-heavy analysis; sole writer = Codex main thread)
- Policy: DIRECT + bounded (atomic analysis, no swarm needed)
- Scope: analyze the G2/G3 backtest database in `C:\Projects\Agent_Workspace\SQS-THC\data_plane\data\`
- Read-only: DO NOT modify data files or source; produce a markdown report only
- Deliverable: `data_plane/reports/data_quality_report.md`
- Commit: `docs(csb): WAVE3 G4 data quality analysis report`

Analysis to cover:
1. Per-symbol row counts + trading-day coverage vs TWSE calendar (2025-08-11..2026-08-10)
2. Intraday bar count per session vs expected 300-minute session (09:00-13:30)
3. OHLC sanity (high>=low, positive prices) + any anomalies
4. Volume/amount distribution tails
5. Duplicate or gap patterns per symbol
6. Verdict: is the dataset usable for the project backtest contract? (PASS/FAIL with evidence)
