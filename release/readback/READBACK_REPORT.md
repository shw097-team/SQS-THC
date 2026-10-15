# READBACK REPORT — WO-TS-REF-14 / TS-014 Package/materialization/readback

artifact_type: READBACK_REPORT
task_id: TS-014
work_order: WO-TS-REF-14
schema_version: "1.0.0"
spec_ref: TS-014/SPEC-34
self_hash_policy: DETACHED_FINAL_DELIVERY_RECEIPT
generated_at: 2026-08-11
result: PASS_LOCAL_DETERMINISTIC

## 1. Purpose

This report is the readback artifact of TS-014 (Package/materialization/
readback). It records the exact target file set, the detached-receipt hash
policy, and the deterministic fail-closed validator that proves
`MANIFEST.json` + `CHECKSUMS.sha256` agree with the actual files on disk.

## 2. Exact file set (canonical root)

| # | Path | Role |
|---|------|------|
| 1 | `release/manifest/MANIFEST.json` | exact file set receipt: path, bytes, sha256 per file (detached final delivery receipt; never lists itself) |
| 2 | `release/checksums/CHECKSUMS.sha256` | sha256 per file in standard `<sha256>  <path>` form (never lists itself or the manifest) |
| 3 | `release/readback/READBACK_REPORT.md` | this readback report |
| 4 | `STATUS_VECTOR.json` | product state, gates, open items |
| 5 | `scripts/validate-package.py` | package validator (pure stdlib, fail-closed, deterministic) |

## 3. Integrity model

- `MANIFEST.json` records `path`/`bytes`/`sha256` for every target except
  itself; `CHECKSUMS.sha256` records the sha256 for every hashed payload
  (readback report, status vector, validator).
- The two receipts agree on every shared path; the validator cross-checks
  manifest <-> checksums <-> actual files and fails closed.
- Recursive self-hash is forbidden (SSOT self-hash policy
  `DETACHED_FINAL_DELIVERY_RECEIPT`): neither receipt lists itself, and
  `CHECKSUMS.sha256` does not list the manifest (the manifest's own sha256 is
  recorded externally, e.g. the git commit, not in-package).
- Digest convention: every sha256 is the EOL-normalized content digest
  (CRLF/CR normalized to LF) and every `bytes` field is the EOL-normalized
  byte count, so checkouts that convert line endings (`core.autocrlf`) hash
  identically to the LF canonical form (same convention as the TS-012
  evidence ledger). Validation is deterministic across LF and CRLF trees.

## 4. Validation result

- `python scripts/validate-package.py` -> exit 0 (`PACKAGE_READBACK_OK`)
- `python -m unittest discover -s tests -t .` (PYTHONPATH=src) -> baseline
  171 tests stay green plus the TS-014 suite
- The validator performs no file mutation; no broker write; no network.

## 5. Error codes (fail-closed)

| Code | Meaning |
|------|---------|
| `ERR_PACKAGE_READBACK_MISMATCH` | checksum/bytes/set disagreement between manifest, checksums and actual files |
| `ERR_PACKAGE_READBACK_SCHEMA` | missing required field, malformed receipt, or self-hash violation |

## 6. Honesty ceiling

Local deterministic readback only: `PRODUCTION_PASS` is `NOT_CLAIMED`,
runtime status is `NOT_RUN`, and external evidence receipts under
`evidence/taskspecs/ts-014-*` remain `EXTERNAL_RECEIPT_REQUIRED`.
