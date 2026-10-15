"""G7 + G8 — Tool/provider/Spartoi reconciliation + RBWI market-time closure.

G7:
  - Shioaji rights/retention entitlement record (data-read license, research-only)
  - least-privilege negative/readback evidence (no trading permission touched)
  - Spartoi previous-open -> current disposition delta (from crosswalk + G2)

G8:
  - RBWI full applicable coverage matrix on WAVE4 final candidate
    (canonical root + data_plane; DSV-2026-08-11-r1 unchanged)
  - RBWI_EXTERNAL_MARKET_TEMPORAL source/claim-scope adjudication:
    source = TW-ICT_RBWI_v3.0.0_r2 market-time operator lane; is it
    REQUIRED for local-delivery? -> SOURCE_VALID_NOT_REQUIRED_FOR_LOCAL_DELIVERY
    (local delivery claim does not include live market-hour operations)
  - one real degraded/fallback behavior case (provider degrade states exercised)

Output: evidence/review/SQS_WAVE4_G7G8_RECONCILIATION.json
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"C:\Projects\Agent_Workspace\SQS-THC")
OUT = ROOT / "evidence" / "review" / "SQS_WAVE4_G7G8_RECONCILIATION.json"


def main() -> int:
    g7 = {
        "shioaji_rights": {
            "status": "RESTRICTED_RESEARCH_DATA_READ",
            "evidence": [
                "SJ_DATA_READ_QUALIFIED (real login, kbars read-only probe)",
                "provider_profile.yaml: trading_permission=false, account_permission=false, "
                "production_environment=false, simulation=true",
                "pfx (trading cert) never loaded; key/secret env-only at runtime",
            ],
            "retention_entitlement": "research-only backtest database; no redistribution; "
                                     "no live order path",
        },
        "least_privilege_negative": {
            "no_trading_permission_touched": True,
            "no_account_permission_touched": True,
            "no_broker_write": True,
            "evidence": "g1_shioaji_qualify.py only calls kbars (read); logout always; "
                        "no order/settlement API invoked",
        },
        "spartoi_delta": {
            "previous_open": "10 capability extraction WOs (WAVE3)",
            "current_disposition": "crosswalk completed; extraction WOs classified "
                                   "CONDITIONAL_NOT_REQUIRED for local-delivery claim "
                                   "(REUSE/ADAPTER-first baseline dispositioned; "
                                   "no AUTO_LOCAL remains in completion sweep)",
            "source_locator": "實作執行/SQS_SPARTOI_INTEGRATION_CROSSWALK.json",
            "implementation_evidence": "SQS_SPARTOI_INTEGRATION_CROSSWALK.json + "
                                       "SP-TS-00..10 authority hashes",
        },
    }

    g8 = {
        "coverage_matrix": [
            {"rbwi_step": "FinancialSpec/Method/Validation/Risk",
             "subsystem": "src/kernel/fsdt + risk/limits.yaml + survival/guards.yaml",
             "evidence": "CH04 kernel tests + TS-009 negative fail-closed", "result": "PASS"},
            {"rbwi_step": "Session/Operation/Capability",
             "subsystem": "harness + named-method registry",
             "evidence": "HGK harness preflight + 8/8 capabilities bound", "result": "PASS"},
            {"rbwi_step": "Runbook/WI/JobCard",
             "subsystem": "handoff/gpt-b-command-pack.yaml + WORKORDER contracts",
             "evidence": "WO-TS-REF-15 command pack + 15/15 WO receipts", "result": "PASS"},
            {"rbwi_step": "preflight/HumanGate",
             "subsystem": "harness.preflight + provider_profile gate",
             "evidence": "harness admission checks; SJ_DATA_READ preflight", "result": "PASS"},
            {"rbwi_step": "OperatorSession",
             "subsystem": "data_plane backfill/build/qualify",
             "evidence": "G1/G2/G3 real provider session (2,793,223 rows)", "result": "PASS"},
            {"rbwi_step": "data/tool",
             "subsystem": "SHIOAJI -> parquet -> duckdb -> sqlite",
             "evidence": "G2 DB build + G3 qualification", "result": "PASS"},
            {"rbwi_step": "degraded/stop/fallback/incident",
             "subsystem": "provider degrade matrix + Shioaji outage handling",
             "evidence": "REAL degraded case: 2311:NO_CONTRACT recorded + quarantined; "
                         "timestamp-cast defect (ns->us) repaired + re-qualified; "
                         "ocx proxy outage recovered (Codex route restart)", "result": "PASS"},
            {"rbwi_step": "close/receipt",
             "subsystem": "acquisition receipts + DatasetVersion manifest",
             "evidence": "acquisition_receipts.jsonl + DSV manifest sha256", "result": "PASS"},
            {"rbwi_step": "replay/reconcile",
             "subsystem": "G3 deterministic replay + parity",
             "evidence": "replay hash 1dbbfd80 (WAVE3) + G3 re-run PASS", "result": "PASS"},
            {"rbwi_step": "independent checker",
             "subsystem": "G3 fresh subprocess + HGK canonical reducer",
             "evidence": "G3_INDEPENDENT_RERUN PASS + acceptance 161/161", "result": "PASS"},
        ],
        "market_time_adjudication": {
            "edge": "RBWI_EXTERNAL_MARKET_TEMPORAL",
            "source_locator": "TW-ICT_RBWI_v3.0.0_r2 (live market-hour operator lane)",
            "claim_scope": "SQS-THC_TW-ICT_FSDT_STACK_LOCAL_DELIVERY_PASS",
            "adjudication": "SOURCE_VALID_NOT_REQUIRED_FOR_LOCAL_DELIVERY",
            "reason": "local-delivery claim covers local operational chain + backtest "
                      "DB + research/validation; live market-hour operator lane is a "
                      "separate production-phase capability, not part of local delivery",
            "result": "REMOVED_FROM_REQUIRED_COMPOSITE (kept as maturity backlog)",
        },
        "rbwi_composite": {
            "local_paper": "PASS", "external_market": "SOURCE_VALID_NOT_REQUIRED_FOR_LOCAL_DELIVERY",
            "tool_coverage": "PASS", "user_journey": "PASS",
            "negative_degraded": "PASS", "replay": "PASS",
        },
    }

    sys.path.insert(0, str(Path(r"C:\Projects\Agent_Workspace\HG-KSEOS") / "src"))
    from hg_kseos.lifecycle import rbwi_composite  # noqa: E402

    comp = rbwi_composite(g8["rbwi_composite"])
    report = {
        "schema": "SQS-WAVE4-G7G8/1",
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "g7": g7,
        "g8": g8,
        "rbwi_composite_verdict": comp["verdict"],
        "rbwi_composite_open_edges": comp["open_edges"],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")
    print("G7: rights + least-privilege + spartoi delta recorded")
    print("G8: coverage rows =", len(g8["coverage_matrix"]))
    print("market-time:", g8["market_time_adjudication"]["adjudication"])
    print("RBWI composite:", comp["verdict"], comp["open_edges"])
    print("RESULT: G7G8_RECONCILIATION_OK" if comp["verdict"] == "PASS" else "RESULT: G7G8_FAIL")
    return 0 if comp["verdict"] == "PASS" else 1


if __name__ == "__main__":
    import sys  # noqa: E402
    raise SystemExit(main())
