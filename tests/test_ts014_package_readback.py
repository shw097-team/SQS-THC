# TS-014 Package/materialization/readback acceptance tests (WO-TS-REF-14).
#
# Pure stdlib unittest - no third-party dependencies. Deterministic and
# fail-closed: any missing file, malformed receipt, checksum mismatch or
# unexpected construct raises and fails the suite. No broker write, no
# network.
#
# Positive: MANIFEST.json is the exact file set (path, bytes, sha256 per
# target, never listing itself) and CHECKSUMS.sha256 records sha256 per
# hashed payload; both agree with each other and with the actual files, and
# scripts/validate-package.py exits 0 (PACKAGE_READBACK_OK).
# Negative: ERR_PACKAGE_READBACK_MISMATCH - a checksum/bytes/set mismatch
# (e.g. file content differs from the recorded checksum, an undeclared
# checksum path, a manifest path missing from checksums, or a missing file)
# is rejected. A FRESH package is built in a temporary directory per test
# case (setUp) so there is no cross-case contamination; the canonical
# artifacts are never mutated.
# Edge: an empty package (empty manifest package list + empty checksums) is a
# valid deterministic state; a missing required field is rejected with
# ERR_PACKAGE_READBACK_SCHEMA (fail-closed), distinct from
# ERR_PACKAGE_READBACK_MISMATCH; recursive self-hash (a receipt listing
# itself, or checksums listing the manifest) is rejected.
#
# Digest convention (same as the TS-012 evidence ledger): every sha256 is the
# EOL-normalized content digest (CRLF/CR normalized to LF) and every 'bytes'
# field is the EOL-normalized byte count, so LF and CRLF checkouts hash
# identically and the package stays deterministic across core.autocrlf
# conversions.
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MANIFEST_PATH = os.path.join(ROOT, "release", "manifest", "MANIFEST.json")
CHECKSUMS_PATH = os.path.join(ROOT, "release", "checksums", "CHECKSUMS.sha256")
READBACK_PATH = os.path.join(ROOT, "release", "readback", "READBACK_REPORT.md")
STATUS_PATH = os.path.join(ROOT, "STATUS_VECTOR.json")
VALIDATOR_PATH = os.path.join(ROOT, "scripts", "validate-package.py")

ERR_PACKAGE_READBACK_MISMATCH = "ERR_PACKAGE_READBACK_MISMATCH"
ERR_PACKAGE_READBACK_SCHEMA = "ERR_PACKAGE_READBACK_SCHEMA"

# Canonical target set (exact).
TARGETS = (
    "release/manifest/MANIFEST.json",
    "release/checksums/CHECKSUMS.sha256",
    "release/readback/READBACK_REPORT.md",
    "STATUS_VECTOR.json",
    "scripts/validate-package.py",
)
# Detached receipt policy: MANIFEST.json lists every target except itself;
# CHECKSUMS.sha256 lists every hashed payload except itself and the manifest.
EXPECTED_MANIFEST_PATHS = frozenset(
    (
        "release/checksums/CHECKSUMS.sha256",
        "release/readback/READBACK_REPORT.md",
        "STATUS_VECTOR.json",
        "scripts/validate-package.py",
    )
)
EXPECTED_CHECKSUM_PATHS = frozenset(
    (
        "release/readback/READBACK_REPORT.md",
        "STATUS_VECTOR.json",
        "scripts/validate-package.py",
    )
)

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


# ---------------------------------------------------------------------------
# Helpers (pure stdlib, deterministic).
# ---------------------------------------------------------------------------
def load_validator():
    """Load scripts/validate-package.py as a module (no sys.path mutation)."""
    spec = importlib.util.spec_from_file_location(
        "validate_package_ts014", VALIDATOR_PATH
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalize_eol(data):
    return data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def sha256_bytes(data):
    return hashlib.sha256(normalize_eol(data)).hexdigest()


def sha256_file(path):
    with open(path, "rb") as fh:
        return sha256_bytes(fh.read())


def normalized_size(path):
    with open(path, "rb") as fh:
        return len(normalize_eol(fh.read()))


def write_bytes(path, data):
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)


def read_text(path):
    with open(path, "r", encoding="utf-8-sig") as fh:
        return fh.read()


def make_entry(path, data):
    return {
        "path": path,
        "bytes": len(normalize_eol(data)),
        "sha256": sha256_bytes(data),
    }


def default_manifest(entries):
    return {
        "manifest_id": "manifest-ts014-test",
        "schema_version": "1.0.0",
        "spec_ref": "TS-014/SPEC-34",
        "self_hash_policy": "DETACHED_FINAL_DELIVERY_RECEIPT",
        "package": entries,
    }


def checksums_text(lines):
    """lines: iterable of (sha256, path). Standard two-space separator."""
    return "".join("%s  %s\n" % (digest, path) for digest, path in lines)


def write_receipts(root, manifest, checksum_lines):
    write_bytes(
        os.path.join(root, "release/manifest/MANIFEST.json"),
        json.dumps(manifest, indent=2, ensure_ascii=False).encode("utf-8")
        + b"\n",
    )
    write_bytes(
        os.path.join(root, "release/checksums/CHECKSUMS.sha256"),
        checksums_text(checksum_lines).encode("utf-8"),
    )


def build_base_package(root):
    """Write a valid one-file package; returns (payload_rel, payload_bytes)."""
    rel = "payload-a.txt"
    payload = b"alpha\n"
    write_bytes(os.path.join(root, rel), payload)
    write_receipts(
        root,
        default_manifest([make_entry(rel, payload)]),
        [(sha256_bytes(payload), rel)],
    )
    return rel, payload


def run_validator(root=None):
    command = [sys.executable, VALIDATOR_PATH]
    if root is not None:
        command += ["--root", root]
    return subprocess.run(
        command, capture_output=True, text=True, cwd=ROOT
    )


# ---------------------------------------------------------------------------
# Positive tests
# ---------------------------------------------------------------------------
class TS014PositiveTests(unittest.TestCase):
    def test_pos_001_all_target_files_exist(self):
        for path in TARGETS:
            self.assertTrue(
                os.path.isfile(os.path.join(ROOT, path)),
                "missing target %s" % path,
            )

    def test_pos_002_manifest_exact_file_set(self):
        manifest = json.loads(read_text(MANIFEST_PATH))
        self.assertEqual(manifest["manifest_id"], "manifest-ts014")
        self.assertEqual(manifest["schema_version"], "1.0.0")
        self.assertEqual(manifest["spec_ref"], "TS-014/SPEC-34")
        self.assertEqual(
            manifest["self_hash_policy"],
            "DETACHED_FINAL_DELIVERY_RECEIPT",
        )
        entries = manifest["package"]
        self.assertIsInstance(entries, list)
        paths = [entry["path"] for entry in entries]
        self.assertEqual(
            set(paths), EXPECTED_MANIFEST_PATHS, "manifest is not the exact file set"
        )
        self.assertEqual(len(paths), len(set(paths)), "duplicate manifest path")
        for entry in entries:
            self.assertIn("path", entry)
            self.assertIn("bytes", entry)
            self.assertIn("sha256", entry)
            self.assertIsInstance(entry["bytes"], int)
            self.assertGreaterEqual(entry["bytes"], 0)
            self.assertIsInstance(entry["sha256"], str)
            self.assertTrue(SHA256_RE.match(entry["sha256"]))
            self.assertFalse(entry["path"].startswith("/"))
            self.assertNotIn("..", entry["path"])
        # the manifest never lists itself (detached final delivery receipt)
        self.assertNotIn("release/manifest/MANIFEST.json", paths)

    def test_pos_003_checksums_sha256_per_file(self):
        lines = [
            line for line in read_text(CHECKSUMS_PATH).splitlines() if line.strip()
        ]
        paths = []
        for line in lines:
            digest, _, path = line.partition("  ")
            self.assertTrue(SHA256_RE.match(digest), "bad checksum line %r" % line)
            self.assertTrue(path.strip(), "empty path in %r" % line)
            paths.append(path)
        self.assertEqual(
            set(paths), EXPECTED_CHECKSUM_PATHS, "checksums is not the exact set"
        )
        self.assertEqual(len(paths), len(set(paths)), "duplicate checksum path")
        # never itself, never the manifest
        self.assertNotIn("release/checksums/CHECKSUMS.sha256", paths)
        self.assertNotIn("release/manifest/MANIFEST.json", paths)

    def test_pos_004_receipts_cover_exact_target_set(self):
        manifest = json.loads(read_text(MANIFEST_PATH))
        manifest_paths = set(e["path"] for e in manifest["package"])
        checksum_paths = set(
            line.partition("  ")[2]
            for line in read_text(CHECKSUMS_PATH).splitlines()
            if line.strip()
        )
        # every shared path agrees between the two receipts
        manifest_by_path = {e["path"]: e["sha256"] for e in manifest["package"]}
        for digest, _, path in (
            line.partition("  ") for line in read_text(CHECKSUMS_PATH).splitlines()
            if line.strip()
        ):
            self.assertIn(path, manifest_by_path)
            self.assertEqual(manifest_by_path[path], digest)
        for entry in manifest["package"]:
            if entry["path"] == "release/checksums/CHECKSUMS.sha256":
                continue  # covered only by the manifest (detached receipt)
            self.assertIn(entry["path"], checksum_paths)
        # exact file set: receipts together cover all five targets, no extras
        covered = manifest_paths | checksum_paths
        self.assertEqual(covered, set(TARGETS) - {"release/manifest/MANIFEST.json"})
        self.assertEqual(
            set(TARGETS),
            covered | {"release/manifest/MANIFEST.json"},
            "target set not exactly covered",
        )

    def test_pos_005_manifest_matches_actual_files(self):
        manifest = json.loads(read_text(MANIFEST_PATH))
        for entry in manifest["package"]:
            full = os.path.join(ROOT, entry["path"])
            self.assertTrue(os.path.isfile(full), "missing %s" % entry["path"])
            self.assertEqual(normalized_size(full), entry["bytes"])
            self.assertEqual(sha256_file(full), entry["sha256"])

    def test_pos_006_checksums_match_actual_files(self):
        for line in read_text(CHECKSUMS_PATH).splitlines():
            if not line.strip():
                continue
            digest, _, path = line.partition("  ")
            self.assertEqual(
                sha256_file(os.path.join(ROOT, path)),
                digest,
                "checksum mismatch for %s" % path,
            )

    def test_pos_007_status_vector_valid(self):
        status = json.loads(read_text(STATUS_PATH))
        self.assertEqual(status["status_vector_id"], "status-vector-ts014")
        self.assertEqual(status["schema_version"], "1.0.0")
        self.assertEqual(status["spec_ref"], "TS-014/SPEC-34")
        state = status["product_state"]
        self.assertIsInstance(state, dict)
        self.assertEqual(state["production_pass"], "NOT_CLAIMED")
        self.assertEqual(state["runtime_status"], "NOT_RUN")
        gates = status["gates"]
        self.assertIsInstance(gates, list)
        self.assertTrue(gates)
        for gate in gates:
            for field in ("id", "gate", "status"):
                self.assertIn(field, gate)
                self.assertTrue(str(gate[field]).strip())
        open_items = status["open_items"]
        self.assertIsInstance(open_items, list)
        self.assertTrue(open_items)
        for item in open_items:
            for field in ("id", "title"):
                self.assertIn(field, item)
                self.assertTrue(str(item[field]).strip())

    def test_pos_008_readback_report_valid(self):
        report = read_text(READBACK_PATH)
        self.assertTrue(report.strip())
        for marker in (
            "TS-014",
            "WO-TS-REF-14",
            "PASS_LOCAL_DETERMINISTIC",
            "ERR_PACKAGE_READBACK_MISMATCH",
            "no broker write",
            "no network",
        ):
            self.assertIn(marker, report)
        for path in TARGETS:
            self.assertIn(path, report)

    def test_pos_009_validator_in_process_ok(self):
        module = load_validator()
        package = module.Package(
            ROOT,
            "release/manifest/MANIFEST.json",
            "release/checksums/CHECKSUMS.sha256",
        )
        self.assertEqual(package.issues(), [])
        self.assertIsNone(package.validate())

    def test_pos_010_validator_exit_zero(self):
        result = run_validator()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PACKAGE_READBACK_OK", result.stdout)


# ---------------------------------------------------------------------------
# Negative tests (fresh temp package per case; canonical artifacts untouched)
# ---------------------------------------------------------------------------
class TS014NegativeTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = self._tmp.name

    def test_neg_001_checksum_mismatch_content_differs(self):
        rel, payload = build_base_package(self.root)
        module = load_validator()
        package = module.Package(
            self.root,
            "release/manifest/MANIFEST.json",
            "release/checksums/CHECKSUMS.sha256",
        )
        package.validate()  # valid before the mutation
        # file content now differs from the recorded checksum
        write_bytes(os.path.join(self.root, rel), b"BETA\n")
        self.assertNotEqual(sha256_bytes(b"BETA\n"), sha256_bytes(payload))
        fresh = module.Package(
            self.root,
            "release/manifest/MANIFEST.json",
            "release/checksums/CHECKSUMS.sha256",
        )
        # the content change is detected as a sha256 mismatch (the recorded
        # checksum no longer matches the actual file bytes)
        self.assertTrue(
            any("sha256 mismatch" in problem for problem in fresh.issues())
        )
        with self.assertRaises(module.PackageReadbackError) as ctx:
            fresh.validate()
        self.assertEqual(ctx.exception.code, ERR_PACKAGE_READBACK_MISMATCH)
        self.assertIn("mismatch", str(ctx.exception))
        result = run_validator(self.root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(ERR_PACKAGE_READBACK_MISMATCH, result.stderr)
        # canonical artifacts are untouched: the canonical package still
        # validates and the validator still exits 0
        self.assertEqual(run_validator().returncode, 0)

    def test_neg_002_manifest_bytes_mismatch_detected(self):
        rel, payload = build_base_package(self.root)
        manifest = default_manifest([make_entry(rel, payload)])
        manifest["package"][0]["bytes"] = len(payload) + 7  # wrong byte count
        write_receipts(
            self.root,
            manifest,
            [(sha256_bytes(payload), rel)],
        )
        module = load_validator()
        with self.assertRaises(module.PackageReadbackError) as ctx:
            module.Package(
                self.root,
                "release/manifest/MANIFEST.json",
                "release/checksums/CHECKSUMS.sha256",
            ).validate()
        self.assertEqual(ctx.exception.code, ERR_PACKAGE_READBACK_MISMATCH)
        self.assertIn("size mismatch", str(ctx.exception))

    def test_neg_003_manifest_and_checksums_disagree(self):
        rel, payload = build_base_package(self.root)
        # checksums records a hash that matches disk, manifest records a
        # different (wrong) hash -> receipts disagree and fail closed
        manifest = default_manifest([make_entry(rel, payload)])
        manifest["package"][0]["sha256"] = "0" * 64
        write_receipts(
            self.root,
            manifest,
            [(sha256_bytes(payload), rel)],
        )
        module = load_validator()
        fresh = module.Package(
            self.root,
            "release/manifest/MANIFEST.json",
            "release/checksums/CHECKSUMS.sha256",
        )
        # the receipts disagree on the shared path (fail-closed)
        self.assertTrue(
            any("disagree" in problem for problem in fresh.issues())
        )
        with self.assertRaises(module.PackageReadbackError) as ctx:
            fresh.validate()
        self.assertEqual(ctx.exception.code, ERR_PACKAGE_READBACK_MISMATCH)
        self.assertIn("mismatch", str(ctx.exception))

    def test_neg_004_checksum_path_not_in_manifest(self):
        rel, payload = build_base_package(self.root)
        extra = b"ghost\n"
        write_bytes(os.path.join(self.root, "ghost.txt"), extra)
        write_receipts(
            self.root,
            default_manifest([make_entry(rel, payload)]),
            [
                (sha256_bytes(payload), rel),
                (sha256_bytes(extra), "ghost.txt"),
            ],
        )
        module = load_validator()
        with self.assertRaises(module.PackageReadbackError) as ctx:
            module.Package(
                self.root,
                "release/manifest/MANIFEST.json",
                "release/checksums/CHECKSUMS.sha256",
            ).validate()
        self.assertEqual(ctx.exception.code, ERR_PACKAGE_READBACK_MISMATCH)
        self.assertIn("not declared in manifest", str(ctx.exception))

    def test_neg_005_manifest_path_missing_from_checksums(self):
        rel, payload = build_base_package(self.root)
        orphan = b"orphan\n"
        write_bytes(os.path.join(self.root, "orphan.txt"), orphan)
        write_receipts(
            self.root,
            default_manifest(
                [make_entry(rel, payload), make_entry("orphan.txt", orphan)]
            ),
            [(sha256_bytes(payload), rel)],
        )
        module = load_validator()
        with self.assertRaises(module.PackageReadbackError) as ctx:
            module.Package(
                self.root,
                "release/manifest/MANIFEST.json",
                "release/checksums/CHECKSUMS.sha256",
            ).validate()
        self.assertEqual(ctx.exception.code, ERR_PACKAGE_READBACK_MISMATCH)
        self.assertIn("missing from checksums", str(ctx.exception))

    def test_neg_006_missing_file_rejected(self):
        rel, payload = build_base_package(self.root)
        # declared in the receipts but never written to disk
        missing = b"never-written\n"
        write_receipts(
            self.root,
            default_manifest(
                [make_entry(rel, payload), make_entry("missing.txt", missing)]
            ),
            [
                (sha256_bytes(payload), rel),
                (sha256_bytes(missing), "missing.txt"),
            ],
        )
        module = load_validator()
        with self.assertRaises(module.PackageReadbackError) as ctx:
            module.Package(
                self.root,
                "release/manifest/MANIFEST.json",
                "release/checksums/CHECKSUMS.sha256",
            ).validate()
        self.assertEqual(ctx.exception.code, ERR_PACKAGE_READBACK_MISMATCH)
        self.assertIn("file missing", str(ctx.exception))

    def test_neg_007_manifest_self_listing_rejected(self):
        rel, payload = build_base_package(self.root)
        manifest = default_manifest([make_entry(rel, payload)])
        manifest["package"].append(
            make_entry("release/manifest/MANIFEST.json", b"self")
        )
        write_receipts(
            self.root,
            manifest,
            [(sha256_bytes(payload), rel)],
        )
        module = load_validator()
        with self.assertRaises(module.PackageReadbackError) as ctx:
            module.Package(
                self.root,
                "release/manifest/MANIFEST.json",
                "release/checksums/CHECKSUMS.sha256",
            )
        self.assertEqual(ctx.exception.code, ERR_PACKAGE_READBACK_SCHEMA)
        self.assertIn("must not list itself", str(ctx.exception))

    def test_neg_008_checksums_self_listing_rejected(self):
        rel, payload = build_base_package(self.root)
        write_receipts(
            self.root,
            default_manifest([make_entry(rel, payload)]),
            [
                (sha256_bytes(payload), rel),
                ("0" * 64, "release/checksums/CHECKSUMS.sha256"),
            ],
        )
        module = load_validator()
        with self.assertRaises(module.PackageReadbackError) as ctx:
            module.Package(
                self.root,
                "release/manifest/MANIFEST.json",
                "release/checksums/CHECKSUMS.sha256",
            )
        self.assertEqual(ctx.exception.code, ERR_PACKAGE_READBACK_SCHEMA)
        self.assertIn("must not list itself", str(ctx.exception))

    def test_neg_009_checksums_listing_manifest_rejected(self):
        rel, payload = build_base_package(self.root)
        write_receipts(
            self.root,
            default_manifest([make_entry(rel, payload)]),
            [
                (sha256_bytes(payload), rel),
                ("0" * 64, "release/manifest/MANIFEST.json"),
            ],
        )
        module = load_validator()
        with self.assertRaises(module.PackageReadbackError) as ctx:
            module.Package(
                self.root,
                "release/manifest/MANIFEST.json",
                "release/checksums/CHECKSUMS.sha256",
            )
        self.assertEqual(ctx.exception.code, ERR_PACKAGE_READBACK_SCHEMA)
        self.assertIn("detached final delivery receipt", str(ctx.exception))


# ---------------------------------------------------------------------------
# Edge tests
# ---------------------------------------------------------------------------
class TS014EdgeTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.root = self._tmp.name

    def test_edge_001_empty_package_allowed(self):
        # empty manifest package list + empty checksums is a valid
        # deterministic state
        write_receipts(self.root, default_manifest([]), [])
        module = load_validator()
        package = module.Package(
            self.root,
            "release/manifest/MANIFEST.json",
            "release/checksums/CHECKSUMS.sha256",
        )
        self.assertEqual(package.manifest_entries, ())
        self.assertEqual(package.checksum_entries, ())
        self.assertEqual(package.issues(), [])
        self.assertIsNone(package.validate())
        result = run_validator(self.root)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PACKAGE_READBACK_OK", result.stdout)

    def test_edge_002_missing_required_field_rejected(self):
        rel, payload = build_base_package(self.root)
        manifest = default_manifest([make_entry(rel, payload)])
        del manifest["package"]  # required field removed
        write_receipts(self.root, manifest, [(sha256_bytes(payload), rel)])
        module = load_validator()
        with self.assertRaises(module.PackageReadbackError) as ctx:
            module.Package(
                self.root,
                "release/manifest/MANIFEST.json",
                "release/checksums/CHECKSUMS.sha256",
            )
        self.assertEqual(ctx.exception.code, ERR_PACKAGE_READBACK_SCHEMA)
        self.assertIn("package", str(ctx.exception))
        result = run_validator(self.root)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(ERR_PACKAGE_READBACK_SCHEMA, result.stderr)
        self.assertIn("package", result.stderr)

    def test_edge_003_entry_missing_sha256_rejected(self):
        rel, payload = build_base_package(self.root)
        entry = make_entry(rel, payload)
        del entry["sha256"]
        write_receipts(
            self.root,
            default_manifest([entry]),
            [(sha256_bytes(payload), rel)],
        )
        module = load_validator()
        with self.assertRaises(module.PackageReadbackError) as ctx:
            module.Package(
                self.root,
                "release/manifest/MANIFEST.json",
                "release/checksums/CHECKSUMS.sha256",
            )
        self.assertEqual(ctx.exception.code, ERR_PACKAGE_READBACK_SCHEMA)
        self.assertIn("sha256", str(ctx.exception))

    def test_edge_004_duplicate_path_rejected(self):
        rel, payload = build_base_package(self.root)
        write_receipts(
            self.root,
            default_manifest(
                [make_entry(rel, payload), make_entry(rel, payload)]
            ),
            [(sha256_bytes(payload), rel)],
        )
        module = load_validator()
        with self.assertRaises(module.PackageReadbackError) as ctx:
            module.Package(
                self.root,
                "release/manifest/MANIFEST.json",
                "release/checksums/CHECKSUMS.sha256",
            )
        self.assertEqual(ctx.exception.code, ERR_PACKAGE_READBACK_SCHEMA)
        self.assertIn("duplicate path", str(ctx.exception))

    def test_edge_005_malformed_checksum_line_rejected(self):
        rel, payload = build_base_package(self.root)
        write_bytes(
            os.path.join(self.root, "release/checksums/CHECKSUMS.sha256"),
            b"not-a-sha256  payload-a.txt\n",
        )
        module = load_validator()
        with self.assertRaises(module.PackageReadbackError) as ctx:
            module.Package(
                self.root,
                "release/manifest/MANIFEST.json",
                "release/checksums/CHECKSUMS.sha256",
            )
        self.assertEqual(ctx.exception.code, ERR_PACKAGE_READBACK_SCHEMA)
        self.assertIn("malformed", str(ctx.exception))

    def test_edge_006_absolute_path_rejected(self):
        rel, payload = build_base_package(self.root)
        entry = make_entry(rel, payload)
        entry["path"] = "C:/escaped.txt"
        write_receipts(
            self.root,
            default_manifest([entry]),
            [(sha256_bytes(payload), rel)],
        )
        module = load_validator()
        with self.assertRaises(module.PackageReadbackError) as ctx:
            module.Package(
                self.root,
                "release/manifest/MANIFEST.json",
                "release/checksums/CHECKSUMS.sha256",
            )
        self.assertEqual(ctx.exception.code, ERR_PACKAGE_READBACK_SCHEMA)
        self.assertIn("absolute path", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
