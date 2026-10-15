#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TS-014 package/materialization/readback validator (ART-14).

Deterministic, fail-closed, pure stdlib. No broker write, no network.

Validates a release package defined by two receipts:

  - MANIFEST.json    : exact file set; each entry is {path, bytes, sha256}
                       for every target EXCEPT the manifest itself (detached
                       final delivery receipt; recursive self-hash forbidden).
  - CHECKSUMS.sha256 : standard "<sha256>  <path>" lines for every hashed
                       payload (readback report, status vector, validator);
                       it never lists itself and never lists the manifest.

The validator cross-checks manifest <-> checksums <-> actual files on disk.
Any byte/hash/set disagreement fails closed with ERR_PACKAGE_READBACK_MISMATCH;
missing required fields, malformed receipts or self-hash violations fail
closed with ERR_PACKAGE_READBACK_SCHEMA. The validator never mutates files.

Digest convention: every sha256 is the EOL-normalized content digest (CRLF
and CR line endings are normalized to LF before hashing) and every ``bytes``
field is the EOL-normalized byte count, so a checkout that converts line
endings (core.autocrlf) hashes identically to the LF canonical form. This is
the same convention as the TS-012 evidence ledger.
"""

import argparse
import hashlib
import json
import os
import re
import sys

ERR_PACKAGE_READBACK_MISMATCH = "ERR_PACKAGE_READBACK_MISMATCH"
ERR_PACKAGE_READBACK_SCHEMA = "ERR_PACKAGE_READBACK_SCHEMA"
DETACHED_RECEIPT_POLICY = "DETACHED_FINAL_DELIVERY_RECEIPT"

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
CHECKSUM_LINE_RE = re.compile(r"^(?P<sha256>[0-9a-f]{64})  (?P<path>.+)$")

MANIFEST_REQUIRED_FIELDS = (
    "manifest_id",
    "schema_version",
    "spec_ref",
    "self_hash_policy",
    "package",
)
ENTRY_REQUIRED_FIELDS = ("path", "bytes", "sha256")


class PackageReadbackError(Exception):
    """Fail-closed package error; ``code`` carries the exact error code."""

    def __init__(self, message, code):
        super().__init__(message)
        self.code = code


def _schema(message):
    return PackageReadbackError(message, ERR_PACKAGE_READBACK_SCHEMA)


def _mismatch(message):
    return PackageReadbackError(message, ERR_PACKAGE_READBACK_MISMATCH)


def normalize_eol(data):
    """Normalize CRLF/CR line endings to LF (deterministic across checkouts)."""
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha256_bytes(data):
    """SHA-256 hex digest of EOL-normalized ``data``."""
    return hashlib.sha256(normalize_eol(data)).hexdigest()


def read_normalized(path):
    """Read ``path`` and return its EOL-normalized bytes."""
    with open(path, "rb") as fh:
        return normalize_eol(fh.read())


def sha256_file(path):
    """EOL-normalized SHA-256 hex digest of the file at ``path``."""
    return sha256_bytes(read_normalized(path))


def read_text(path):
    with open(path, "r", encoding="utf-8-sig") as fh:
        return fh.read()


def normalize_path(value):
    """Return a clean relative path with forward slashes; fail closed."""
    if not isinstance(value, str) or not value.strip():
        raise _schema("path must be a non-empty string")
    path = value.strip().replace("\\", "/")
    if path.startswith("/") or re.match(r"^[A-Za-z]:/", path):
        raise _schema("absolute path is not allowed: %r" % value)
    parts = path.split("/")
    if any(part in ("", ".", "..") for part in parts):
        raise _schema("path must be a clean relative path: %r" % value)
    return path


def _nonempty(value):
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple, dict)):
        return len(value) > 0
    return True


class Package(object):
    """Loads and validates a TS-014 package (manifest + checksums)."""

    def __init__(self, root, manifest_rel, checksums_rel):
        self.root = os.path.abspath(root)
        self.manifest_rel = normalize_path(manifest_rel)
        self.checksums_rel = normalize_path(checksums_rel)
        self._load_manifest()
        self._load_checksums()

    # ------------------------------------------------------------------
    # Loading / schema validation (fail-closed).
    # ------------------------------------------------------------------
    def _load_manifest(self):
        path = os.path.join(self.root, self.manifest_rel)
        if not os.path.isfile(path):
            raise _mismatch("manifest file missing: %s" % self.manifest_rel)
        try:
            data = json.loads(read_text(path))
        except ValueError as exc:
            raise _schema("manifest is not valid JSON: %s" % exc)
        if not isinstance(data, dict):
            raise _schema("manifest must be a JSON object")
        missing = [f for f in MANIFEST_REQUIRED_FIELDS if f not in data]
        if missing:
            raise _schema(
                "manifest missing required field(s): %s" % ", ".join(missing)
            )
        for field in (
            "manifest_id",
            "schema_version",
            "spec_ref",
            "self_hash_policy",
        ):
            if not _nonempty(data[field]):
                raise _schema("manifest field %r must be non-empty" % field)
        if data["self_hash_policy"] != DETACHED_RECEIPT_POLICY:
            raise _schema(
                "manifest self_hash_policy must be %r"
                % DETACHED_RECEIPT_POLICY
            )
        if not isinstance(data["package"], list):
            raise _schema("manifest field 'package' must be a list")
        entries = []
        seen = set()
        for index, entry in enumerate(data["package"]):
            label = "manifest package entry %d" % index
            if not isinstance(entry, dict):
                raise _schema("%s must be an object" % label)
            missing = [f for f in ENTRY_REQUIRED_FIELDS if f not in entry]
            if missing:
                raise _schema(
                    "%s missing required field(s): %s"
                    % (label, ", ".join(missing))
                )
            rel = normalize_path(entry["path"])
            size = entry["bytes"]
            if isinstance(size, bool) or not isinstance(size, int) or size < 0:
                raise _schema(
                    "%s 'bytes' must be a non-negative integer" % label
                )
            digest = entry["sha256"]
            if not isinstance(digest, str) or not SHA256_RE.match(digest):
                raise _schema(
                    "%s 'sha256' must be 64 lowercase hex digits" % label
                )
            if rel in seen:
                raise _schema("manifest duplicate path %r" % rel)
            seen.add(rel)
            entries.append({"path": rel, "bytes": size, "sha256": digest})
        if self.manifest_rel in seen:
            raise _schema(
                "manifest must not list itself "
                "(recursive self-hash forbidden)"
            )
        self._entries = tuple(entries)

    def _load_checksums(self):
        path = os.path.join(self.root, self.checksums_rel)
        if not os.path.isfile(path):
            raise _mismatch("checksums file missing: %s" % self.checksums_rel)
        try:
            text = read_text(path)
        except UnicodeDecodeError as exc:
            raise _schema("checksums not valid UTF-8: %s" % exc)
        lines = [line for line in text.splitlines() if line.strip()]
        entries = []
        seen = set()
        for lineno, line in enumerate(lines, 1):
            match = CHECKSUM_LINE_RE.match(line.strip())
            if not match:
                raise _schema(
                    "checksums line %d malformed "
                    "(expected '<sha256>  <path>'): %r" % (lineno, line)
                )
            digest = match.group("sha256")
            rel = normalize_path(match.group("path"))
            if rel in seen:
                raise _schema("checksums duplicate path %r" % rel)
            seen.add(rel)
            entries.append({"path": rel, "sha256": digest})
        if self.checksums_rel in seen:
            raise _schema(
                "checksums must not list itself "
                "(recursive self-hash forbidden)"
            )
        if self.manifest_rel in seen:
            raise _schema(
                "checksums must not list the manifest (manifest is the "
                "detached final delivery receipt; its hash is external)"
            )
        self._checksums = tuple(entries)

    # ------------------------------------------------------------------
    # Accessors.
    # ------------------------------------------------------------------
    @property
    def manifest_entries(self):
        return tuple(dict(e) for e in self._entries)

    @property
    def checksum_entries(self):
        return tuple(dict(c) for c in self._checksums)

    # ------------------------------------------------------------------
    # Integrity checks (deterministic, fail-closed).
    # ------------------------------------------------------------------
    def issues(self):
        """Return a deterministic list of problems; empty means valid."""
        problems = []
        for entry in self._entries:
            full = os.path.join(self.root, entry["path"])
            if not os.path.isfile(full):
                problems.append("file missing: %s" % entry["path"])
                continue
            normalized = read_normalized(full)
            actual_size = len(normalized)
            if actual_size != entry["bytes"]:
                problems.append(
                    "size mismatch for %s: manifest %d, actual %d"
                    % (entry["path"], entry["bytes"], actual_size)
                )
            actual_digest = sha256_bytes(normalized)
            if actual_digest != entry["sha256"]:
                problems.append(
                    "sha256 mismatch for %s: manifest %s, actual %s"
                    % (entry["path"], entry["sha256"], actual_digest)
                )
        for checksum in self._checksums:
            full = os.path.join(self.root, checksum["path"])
            if not os.path.isfile(full):
                problems.append("file missing: %s" % checksum["path"])
                continue
            actual_digest = sha256_bytes(read_normalized(full))
            if actual_digest != checksum["sha256"]:
                problems.append(
                    "sha256 mismatch for %s: checksums %s, actual %s"
                    % (checksum["path"], checksum["sha256"], actual_digest)
                )
        manifest_by_path = {e["path"]: e["sha256"] for e in self._entries}
        checksum_by_path = {c["path"]: c["sha256"] for c in self._checksums}
        for checksum in self._checksums:
            manifest_digest = manifest_by_path.get(checksum["path"])
            if manifest_digest is None:
                problems.append(
                    "checksum path %r not declared in manifest"
                    % checksum["path"]
                )
            elif manifest_digest != checksum["sha256"]:
                problems.append(
                    "manifest and checksums disagree on sha256 for %r"
                    % checksum["path"]
                )
        for entry in self._entries:
            if entry["path"] == self.checksums_rel:
                continue
            checksum_digest = checksum_by_path.get(entry["path"])
            if checksum_digest is None:
                problems.append(
                    "manifest path %r missing from checksums" % entry["path"]
                )
            elif checksum_digest != entry["sha256"]:
                problems.append(
                    "manifest and checksums disagree on sha256 for %r"
                    % entry["path"]
                )
        return problems

    def validate(self):
        """Fail closed: raise PackageReadbackError on the first problem."""
        problems = self.issues()
        if problems:
            raise _mismatch(problems[0])
        return None


def validate_package(root, manifest_rel, checksums_rel):
    """Convenience: build and validate; returns the Package on success."""
    package = Package(root, manifest_rel, checksums_rel)
    package.validate()
    return package


def _default_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="TS-014 package/materialization/readback validator."
    )
    parser.add_argument(
        "--root",
        default=_default_root(),
        help="package root directory (default: repository root)",
    )
    parser.add_argument(
        "--manifest",
        default="release/manifest/MANIFEST.json",
        help="manifest path relative to --root",
    )
    parser.add_argument(
        "--checksums",
        default="release/checksums/CHECKSUMS.sha256",
        help="checksums path relative to --root",
    )
    args = parser.parse_args(argv)
    try:
        package = Package(args.root, args.manifest, args.checksums)
    except PackageReadbackError as exc:
        print("ERROR: %s" % exc, file=sys.stderr)
        print(exc.code, file=sys.stderr)
        return 2
    problems = package.issues()
    if problems:
        for problem in problems:
            print("ERROR: %s" % problem, file=sys.stderr)
        print(ERR_PACKAGE_READBACK_MISMATCH, file=sys.stderr)
        return 2
    print("PACKAGE_READBACK_OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
