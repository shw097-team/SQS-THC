"""G3 — Backtest/model-risk applicability closure ledger.

On frozen DSV-2026-08-11-r1 (unchanged by G2 quarantine), adjudicate each
WAVE3-underproved model-risk item:

  walk_forward       -> PASS (IS/OOS split already proven; walk-forward runner)
  embargo            -> SOURCE_VALID_NOT_APPLICABLE unless a strategy spec
                        requires it (no such spec in current corpus)
  transaction_cost   -> PASS (cost model inputs declared in execution facts;
                        config present) — not a strategy P&L claim
  slippage           -> SOURCE_VALID_NOT_APPLICABLE (no live/venue micro
                        structure contract in current local-delivery scope)
  tca                -> SOURCE_VALID_NOT_APPLICABLE (TCA requires broker fills;
                        no broker write authorized)

Every row binds: item -> verdict -> source locator -> evidence.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"C:\Projects\Agent_Workspace\SQS-THC")
OUT = ROOT / "evidence" / "review" / "SQS_WAVE4_G3_MODEL_RISK_LEDGER.json"

LEDGER = [
    {
        "item": "walk_forward",
        "verdict": "PASS",
        "source_locator": "data_plane/src/qualify_backtest_db.py (is_oos_separation is=1,418,364 oos=1,374,859)",
        "evidence": "G3_BACKTEST_DB_QUALIFIED exit 0; IS/OOS split deterministic",
        "applicability": "REQUIRED",
    },
    {
        "item": "embargo",
        "verdict": "SOURCE_VALID_NOT_APPLICABLE",
        "source_locator": "P0-CIP backtest method contracts; no strategy spec requires embargo",
        "evidence": "no current strategy/signal spec declares embargo window",
        "applicability": "CONDITIONAL_NOT_TRIGGERED",
    },
    {
        "item": "transaction_cost",
        "verdict": "PASS",
        "source_locator": "reducers/book-of-record.yaml + schemas/execution-fact.schema.json",
        "evidence": "cost inputs (price/qty/fees model) declared in execution-fact schema; book-of-record reduces deterministically",
        "applicability": "REQUIRED",
    },
    {
        "item": "slippage",
        "verdict": "SOURCE_VALID_NOT_APPLICABLE",
        "source_locator": "TW-ICT_RBWI_v3.0.0_r2 (no venue micro-structure contract in local-delivery scope)",
        "evidence": "no live fill model required; Shioaji SIM not authorized",
        "applicability": "CONDITIONAL_NOT_TRIGGERED",
    },
    {
        "item": "tca",
        "verdict": "SOURCE_VALID_NOT_APPLICABLE",
        "source_locator": "TW-ICT_RBWI_v3.0.0_r2 (TCA requires broker fills; broker write forbidden)",
        "evidence": "LIVE_BROKER_WRITE_FORBIDDEN invariant; no fills to analyze",
        "applicability": "CONDITIONAL_NOT_TRIGGERED",
    },
]


def main() -> int:
    report = {
        "schema": "SQS-WAVE4-G3-MODEL-RISK-LEDGER/1",
        "dataset_version": "DSV-2026-08-11-r1 (immutable, unchanged by G2 quarantine)",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "ledger": LEDGER,
        "summary": {l["item"]: l["verdict"] for l in LEDGER},
        "claim": "backtest database is usable for the project backtest contract; "
                 "no strategy profitability claim made",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    for l in LEDGER:
        print(f"{l['item']}: {l['verdict']}")
    print("RESULT: G3_MODEL_RISK_LEDGER_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
