"""G1 — Shioaji provider read-only login qualification.

Loads credentials from the local key file (never printed), logs in with
simulation=True (data lane), verifies:
  - login success (credential valid)
  - contracts accessible (symbols resolvable)
  - data permission works (kbars read is the only op attempted)
  - NO trading/account permission touched
Prints only booleans/counts — never credential material.
"""
from __future__ import annotations

import sys
from pathlib import Path

KEY_FILE = Path(r"C:\Projects\Agent_Workspace\SQS-THC\實作執行\Shioaji API\Shioaji API Key .txt")


def load_creds() -> tuple[str, str]:
    lines = [l.strip() for l in KEY_FILE.read_text(encoding="utf-8-sig", errors="replace").splitlines() if l.strip()]
    # format observed: "api key" / <key> / "secret key" / <secret>
    vals = [l for l in lines if " " not in l and ":" not in l and "=" not in l and len(l) > 20]
    assert len(vals) == 2, f"unexpected credential layout: {len(vals)} values"
    return vals[0], vals[1]


def main() -> int:
    try:
        import shioaji as sj
    except ImportError:
        print("RESULT: FAIL (shioaji not installed)")
        return 1
    api_key, sec_key = load_creds()
    api = sj.Shioaji(simulation=True)
    try:
        api.login(api_key=api_key, secret_key=sec_key)
    except Exception as exc:  # noqa: BLE001
        print(f"RESULT: FAIL (login) {type(exc).__name__}")
        return 1
    print("login: OK")
    # contracts resolvable (market data surface)
    stocks_view = api.Contracts.Stocks
    n_stocks = len(list(stocks_view))
    print(f"contracts_stocks: {n_stocks}")
    try:
        # attempt one tiny read-only kbars fetch to prove data permission
        c = api.Contracts.Stocks["2330"]
        kb = api.kbars(contract=c, start="2026-07-01", end="2026-07-03")
        rows = len(kb.ts) if kb.ts is not None else 0
        print(f"kbars_probe: OK rows={rows}")
    except Exception as exc:  # noqa: BLE001
        print(f"kbars_probe: FAIL ({type(exc).__name__})")
        api.logout()
        return 1
    api.logout()
    print("RESULT: SJ_DATA_READ_QUALIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
