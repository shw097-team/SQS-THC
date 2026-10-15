# TS-012 Evidence/release/learning/NRTV acceptance tests (WO-TS-REF-12).
#
# Pure stdlib unittest - no third-party dependencies. Deterministic and
# fail-closed: any missing file, malformed artifact, or unexpected construct
# raises and fails the suite. No broker write, no network.
#
# Positive: the evidence ledger is append-only and hash-linked (each entry
# carries id, sha256, ref; every sha256 must equal the EOL-normalized
# content digest of the file at ref), release gates validate (every required
# evidence id resolves in the ledger and each claim level is supported by
# the full evidence set),
# NRTV config is valid, migration plans and training runs are well-formed,
# and docs/DOC-12.md anchors the whole domain.
# Negative: ERR_PRODUCTION_CLAIM_INFLATION - claiming PRODUCTION (or SHADOW)
# without the required NRTV/evidence, e.g. a release gate claiming PRODUCTION
# without required evidence. A FRESH ReleaseGates instance and a FRESH
# evidence set are created per test case (setUp), so there is no cross-case
# contamination; a rejected claim never mutates gate or ledger state.
# Edge: an empty evidence ledger is a valid state; a missing required field
# is rejected with a field-naming error (code None), distinct from
# ERR_PRODUCTION_CLAIM_INFLATION; a sha256 that does not match the referenced
# file is rejected with ERR_CHECKSUM_MISMATCH (fail-closed).
import hashlib
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DOC_12_PATH = os.path.join(ROOT, "docs", "DOC-12.md")
EVIDENCE_LEDGER_PATH = os.path.join(ROOT, "evidence", "ledger.yaml")
RELEASE_GATES_PATH = os.path.join(ROOT, "release", "gates.yaml")
MIGRATION_PLANS_PATH = os.path.join(ROOT, "migration", "plans.yaml")
NRTV_CONFIG_PATH = os.path.join(ROOT, "nrtv", "config.yaml")
TRAINING_RUNS_PATH = os.path.join(ROOT, "training", "runs.yaml")

ERR_PRODUCTION_CLAIM_INFLATION = "ERR_PRODUCTION_CLAIM_INFLATION"
ERR_CHECKSUM_MISMATCH = "ERR_CHECKSUM_MISMATCH"
CLAIM_CEILING_LOCAL_DELIVERY = "LOCAL_DELIVERY"

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")

REQUIRED_LEDGER_FIELDS = ("id", "sha256", "ref")
REQUIRED_GATE_FIELDS = ("id", "gate", "required")
REQUIRED_PLAN_FIELDS = ("id", "from", "to", "status")
REQUIRED_NRTV_FIELDS = ("id", "runtime_window", "condition")
REQUIRED_TRAINING_FIELDS = ("id", "model_ref", "status")

MIGRATION_STATUSES = (
    "PROPOSED",
    "COMPATIBILITY_ANALYZED",
    "DUAL_RUN",
    "CUTOVER",
    "SUNSET",
    "ROLLBACK",
)
TRAINING_STATUSES = (
    "NOT_RUN",
    "DESIGN_CLOSED_NOT_RUN",
    "RUNNING",
    "PASS",
    "FAIL",
    "QUARANTINED",
)

# A claim level is supported only when every gate in its list has all of its
# required evidence present in the ledger. PRODUCTION and SHADOW both require
# the NRTV gate (GATE-G18), so claiming them without NRTV evidence is claim
# inflation.
CLAIM_LEVELS = {
    "LOCAL_DELIVERY": ("GATE-G17",),
    "SHADOW": ("GATE-G17", "GATE-G18"),
    "PRODUCTION": ("GATE-G17", "GATE-G18"),
}


# ---------------------------------------------------------------------------
# Minimal deterministic YAML-subset parser (stdlib only, fail-closed).
# Supports the exact constructs used by the TS-012 artifacts:
#   - top-level 'key: value' scalars (plain, quoted, null, flow list)
#   - 'key:' followed by a block list
#   - block-list mapping items '- key: value' with flat 'key2: value2' pairs
#     and nested block lists under a mapping key
# Anything else raises ValueError. Plain numeric scalars become int/float so
# validators can compare deterministically.
# ---------------------------------------------------------------------------
def _indent(line):
    return len(line) - len(line.lstrip(" "))


def _strip_comment(line):
    in_quote = None
    for i, ch in enumerate(line):
        if in_quote:
            if ch == in_quote:
                in_quote = None
        elif ch in ("'", '"'):
            in_quote = ch
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
            return line[:i]
    return line


def _split_key(content):
    for idx in range(len(content)):
        if content[idx] == ":" and (
            idx + 1 == len(content) or content[idx + 1] in " \t"
        ):
            return content[:idx], content[idx + 1:]
    raise ValueError("expected 'key: value' in %r" % content)


def _split_flow(inner):
    parts = []
    buf = []
    in_quote = None
    for ch in inner:
        if in_quote:
            buf.append(ch)
            if ch == in_quote:
                in_quote = None
        elif ch in ("'", '"'):
            in_quote = ch
            buf.append(ch)
        elif ch == ",":
            parts.append("".join(buf))
            buf = []
        else:
            buf.append(ch)
    parts.append("".join(buf))
    return parts


def _number(text):
    try:
        return int(text)
    except ValueError:
        pass
    try:
        return float(text)
    except ValueError:
        pass
    return None


def _scalar(text):
    s = text.strip()
    if s == "":
        return ""
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        if not inner:
            return []
        return [_scalar(x) for x in _split_flow(inner)]
    if len(s) >= 2 and s[0] == "'" and s[-1] == "'":
        return s[1:-1]
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        return s[1:-1]
    if s in ("null", "~"):
        return None
    if s == "true":
        return True
    if s == "false":
        return False
    num = _number(s)
    if num is not None:
        return num
    return s


def _parse_block_list(lines, i, indent):
    items = []
    n = len(lines)
    while i < n:
        line = lines[i]
        cur = _indent(line)
        if cur < indent:
            break
        if cur > indent:
            raise ValueError("unexpected list indentation: %r" % line)
        content = line.strip()
        if not content.startswith("- "):
            break
        rest = content[2:].strip()
        if rest == "":
            raise ValueError("empty list item: %r" % line)
        if ":" in rest and not rest.startswith(("[", "{", "'", '"')):
            key, _, value = rest.partition(":")
            item = {key.strip(): _scalar(value)}
            body_indent = indent + 2
            i += 1
            while i < n:
                nxt = lines[i]
                nind = _indent(nxt)
                if not nxt.strip():
                    i += 1
                    continue
                if nind < indent:
                    break
                if nind == indent and nxt.strip().startswith("- "):
                    break
                if nind == body_indent:
                    k2, r2 = _split_key(nxt.strip())
                    r2 = r2.strip()
                    if r2 == "":
                        j = i + 1
                        if (
                            j >= n
                            or _indent(lines[j]) <= body_indent
                            or not lines[j].strip().startswith("- ")
                        ):
                            raise ValueError(
                                "expected nested block list under %r"
                                % (nxt.strip(),)
                            )
                        sub, i = _parse_block_list(lines, j, _indent(lines[j]))
                        item[k2.strip()] = sub
                    else:
                        item[k2.strip()] = _scalar(r2)
                        i += 1
                else:
                    raise ValueError(
                        "unexpected indentation %d in mapping item: %r"
                        % (nind, nxt)
                    )
            items.append(item)
        else:
            items.append(_scalar(rest))
            i += 1
    return items, i


def parse_yaml_subset(text):
    data = {}
    lines = [
        l
        for l in (_strip_comment(line).rstrip() for line in text.splitlines())
        if l.strip()
    ]
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if _indent(line) != 0:
            raise ValueError("unexpected top-level indentation: %r" % line)
        key, rest = _split_key(line.strip())
        key = key.strip()
        rest = rest.strip()
        if rest == "":
            j = i + 1
            if j >= n or _indent(lines[j]) <= 0:
                data[key] = None
                i += 1
                continue
            nxt = lines[j]
            nindent = _indent(nxt)
            if nxt.strip().startswith("- "):
                items, i = _parse_block_list(lines, i + 1, nindent)
                data[key] = items
            else:
                raise ValueError(
                    "nested mapping not used by TS-012 artifacts: %r" % nxt
                )
        else:
            data[key] = _scalar(rest)
            i += 1
    return data


def read_text(path):
    with open(path, "r", encoding="utf-8-sig") as fh:
        return fh.read()


def load_yaml(path):
    return parse_yaml_subset(read_text(path))


def sha256_file(path):
    with open(path, "rb") as fh:
        data = fh.read()
    # EOL-normalized content digest: CRLF working trees hash identically to
    # LF trees, so the ledger stays deterministic across checkouts.
    normalized = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(normalized).hexdigest()


def load_ledger_entries():
    return load_yaml(EVIDENCE_LEDGER_PATH)["entries"]


def load_gates():
    return load_yaml(RELEASE_GATES_PATH)["gates"]


def load_plans():
    return load_yaml(MIGRATION_PLANS_PATH)["plans"]


def load_nrtv():
    return load_yaml(NRTV_CONFIG_PATH)["configs"]


def load_training():
    return load_yaml(TRAINING_RUNS_PATH)["runs"]


def ledger_ids():
    return [entry["id"] for entry in load_ledger_entries()]


# ---------------------------------------------------------------------------
# Fail-closed TS-012 evidence/release/learning/NRTV semantics used by the
# negative/edge cases.
# ---------------------------------------------------------------------------
class TS012Error(Exception):
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code


def _nonempty(value):
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, tuple)):
        return len(value) > 0
    return True


def _require_fields(record, fields, label):
    if not isinstance(record, dict):
        raise TS012Error("%s must be a mapping" % label)
    missing = [f for f in fields if f not in record]
    if missing:
        raise TS012Error(
            "%s missing required field(s): %s" % (label, ", ".join(missing))
        )


def _resolve_ref(ref, label):
    """Resolve a repo-relative ref safely inside ROOT (fail-closed: a path
    that escapes the workspace is rejected before any read)."""
    if not isinstance(ref, str) or not ref.strip():
        raise TS012Error("%s ref must be a non-empty repo-relative path" % label)
    normalized = ref.replace("\\", "/").lstrip("/")
    parts = [p for p in normalized.split("/") if p not in ("", ".")]
    if any(p == ".." for p in parts):
        raise TS012Error(
            "%s ref must stay inside the repo; escape attempt: %r"
            % (label, ref)
        )
    path = os.path.realpath(os.path.join(ROOT, *parts))
    root_real = os.path.realpath(ROOT)
    if not (path == root_real or path.startswith(root_real + os.sep)):
        raise TS012Error("%s ref escapes the repo: %r" % (label, ref))
    return path


class EvidenceLedger(object):
    """Deterministic, fail-closed evidence ledger (SPEC-16 / CH33).

    Append-only and hash-linked: entries are exposed as an immutable tuple
    and the only mutation is append(), which returns a NEW ledger - there is
    no in-place edit or delete. verify() recomputes the SHA-256 digest of
    every referenced file and compares it with the recorded sha256; a drift
    raises ERR_CHECKSUM_MISMATCH. A fresh instance is created per test case
    so rejected operations never leak state.
    """

    def __init__(self, entries):
        if not isinstance(entries, list):
            raise TS012Error("evidence ledger entries must be a list")
        seen = set()
        frozen = []
        for entry in entries:
            _require_fields(entry, REQUIRED_LEDGER_FIELDS, "evidence entry")
            for field in REQUIRED_LEDGER_FIELDS:
                if not _nonempty(entry.get(field)):
                    raise TS012Error(
                        "evidence entry field %r must be non-empty" % field
                    )
            if not SHA256_RE.match(entry["sha256"]):
                raise TS012Error(
                    "evidence entry %r sha256 must be 64 hex chars"
                    % entry["id"]
                )
            if entry["id"] in seen:
                raise TS012Error(
                    "duplicate evidence entry id %r" % entry["id"]
                )
            seen.add(entry["id"])
            _resolve_ref(entry["ref"], "evidence entry %r" % entry["id"])
            frozen.append(
                {
                    "id": entry["id"],
                    "sha256": entry["sha256"],
                    "ref": entry["ref"],
                }
            )
        self._entries = tuple(frozen)

    @property
    def entries(self):
        return tuple(dict(e) for e in self._entries)

    def verify(self):
        """Recompute every referenced file digest. Raises
        ERR_CHECKSUM_MISMATCH on drift; a missing ref is a field-naming
        error. Returns True on an intact (possibly empty) ledger."""
        for entry in self._entries:
            path = _resolve_ref(entry["ref"], "evidence entry %r" % entry["id"])
            if not os.path.isfile(path):
                raise TS012Error(
                    "evidence entry %r ref does not resolve: %r"
                    % (entry["id"], entry["ref"])
                )
            actual = sha256_file(path)
            if actual != entry["sha256"]:
                raise TS012Error(
                    "evidence entry %r sha256 mismatch for %r"
                    % (entry["id"], entry["ref"]),
                    code=ERR_CHECKSUM_MISMATCH,
                )
        return True

    def append(self, entry):
        """Append-only: returns a NEW ledger with the entry appended. A
        duplicate id or a malformed entry is rejected; existing entries are
        never modified."""
        new_entries = [dict(e) for e in self._entries]
        new_entries.append(entry)
        return EvidenceLedger(new_entries)


class ReleaseGates(object):
    """Deterministic, fail-closed release gates (SPEC-34 / CH33).

    Each gate carries id, gate and required (exact evidence ids). A claim at
    a given level is honored only when every gate in CLAIM_LEVELS[level] has
    all of its required evidence present; otherwise the claim exceeds the
    evidence ceiling and raises ERR_PRODUCTION_CLAIM_INFLATION with no
    mutation (fail-closed).
    """

    def __init__(self, gates):
        if not isinstance(gates, list) or not gates:
            raise TS012Error("release gates must be a non-empty list")
        seen_ids = set()
        seen_names = set()
        self._gates = []
        for gate in gates:
            _require_fields(gate, REQUIRED_GATE_FIELDS, "release gate")
            if not _nonempty(gate.get("id")) or not _nonempty(gate.get("gate")):
                raise TS012Error(
                    "release gate id and gate must be non-empty"
                )
            required = gate.get("required")
            if not isinstance(required, list) or not required:
                raise TS012Error(
                    "release gate %r required must be a non-empty list"
                    % (gate.get("id"),)
                )
            for item in required:
                if not isinstance(item, str) or not item.strip():
                    raise TS012Error(
                        "release gate %r required evidence id must be a "
                        "non-empty string" % (gate.get("id"),)
                    )
            if gate["id"] in seen_ids:
                raise TS012Error(
                    "duplicate release gate id %r" % gate["id"]
                )
            if gate["gate"] in seen_names:
                raise TS012Error(
                    "duplicate release gate name %r" % gate["gate"]
                )
            seen_ids.add(gate["id"])
            seen_names.add(gate["gate"])
            self._gates.append(
                {
                    "id": gate["id"],
                    "gate": gate["gate"],
                    "required": tuple(gate["required"]),
                }
            )

    @property
    def gates(self):
        return tuple(dict(g) for g in self._gates)

    def by_name(self, gate_name):
        for gate in self._gates:
            if gate["gate"] == gate_name:
                return gate
        raise TS012Error("unknown release gate name %r" % gate_name)

    def required_evidence(self, gate_id):
        for gate in self._gates:
            if gate["id"] == gate_id:
                return gate["required"]
        raise TS012Error("unknown release gate id %r" % gate_id)

    def gates_for_claim(self, claim):
        if claim not in CLAIM_LEVELS:
            raise TS012Error("unknown claim level %r" % claim)
        return CLAIM_LEVELS[claim]

    def validate(self, ledger_ids):
        """Every gate's required evidence must resolve in the ledger."""
        evidence_set = set(ledger_ids)
        for gate in self._gates:
            missing = [e for e in gate["required"] if e not in evidence_set]
            if missing:
                raise TS012Error(
                    "release gate %s missing required evidence: %s"
                    % (gate["gate"], ", ".join(missing))
                )
        return True

    def claim(self, claim, ledger_ids):
        """Claim a status only when the evidence ceiling supports it. A claim
        without its required evidence - e.g. PRODUCTION without NRTV or
        evidence - raises ERR_PRODUCTION_CLAIM_INFLATION and performs no
        mutation."""
        evidence_set = set(ledger_ids)
        missing = []
        for gate_id in self.gates_for_claim(claim):
            for item in self.required_evidence(gate_id):
                if item not in evidence_set:
                    missing.append(item)
        if missing:
            raise TS012Error(
                "claiming %s without required evidence; missing: %s "
                "(release/NRTV evidence)" % (claim, ", ".join(missing)),
                code=ERR_PRODUCTION_CLAIM_INFLATION,
            )
        return True


class NrtvConfig(object):
    """NRTV configuration (SPEC-35 / CH35): each config carries id,
    runtime_window and condition; a missing field is a field-naming error."""

    def __init__(self, configs):
        if not isinstance(configs, list) or not configs:
            raise TS012Error("nrtv configs must be a non-empty list")
        seen = set()
        frozen = []
        for cfg in configs:
            _require_fields(cfg, REQUIRED_NRTV_FIELDS, "nrtv config")
            for field in REQUIRED_NRTV_FIELDS:
                if not _nonempty(cfg.get(field)):
                    raise TS012Error(
                        "nrtv config field %r must be non-empty" % field
                    )
            if cfg["id"] in seen:
                raise TS012Error("duplicate nrtv config id %r" % cfg["id"])
            seen.add(cfg["id"])
            frozen.append(
                {
                    "id": cfg["id"],
                    "runtime_window": cfg["runtime_window"],
                    "condition": cfg["condition"],
                }
            )
        self._configs = tuple(frozen)

    @property
    def configs(self):
        return tuple(dict(c) for c in self._configs)


class MigrationPlans(object):
    """Migration plans (SPEC-31 / CH34): each plan carries id, from, to and a
    valid status; a missing field or an unknown status is rejected."""

    def __init__(self, plans):
        if not isinstance(plans, list) or not plans:
            raise TS012Error("migration plans must be a non-empty list")
        seen = set()
        frozen = []
        for plan in plans:
            _require_fields(plan, REQUIRED_PLAN_FIELDS, "migration plan")
            for field in REQUIRED_PLAN_FIELDS:
                if not _nonempty(plan.get(field)):
                    raise TS012Error(
                        "migration plan field %r must be non-empty" % field
                    )
            if plan["id"] in seen:
                raise TS012Error("duplicate migration plan id %r" % plan["id"])
            seen.add(plan["id"])
            if plan["status"] not in MIGRATION_STATUSES:
                raise TS012Error(
                    "migration plan %r unknown status %r"
                    % (plan["id"], plan["status"])
                )
            frozen.append(
                {
                    "id": plan["id"],
                    "from": plan["from"],
                    "to": plan["to"],
                    "status": plan["status"],
                }
            )
        self._plans = tuple(frozen)

    @property
    def plans(self):
        return tuple(dict(p) for p in self._plans)


class TrainingRuns(object):
    """Training runs (CH35): each run carries id, model_ref and a valid
    status; a missing field or an unknown status is rejected."""

    def __init__(self, runs):
        if not isinstance(runs, list) or not runs:
            raise TS012Error("training runs must be a non-empty list")
        seen = set()
        frozen = []
        for run in runs:
            _require_fields(run, REQUIRED_TRAINING_FIELDS, "training run")
            for field in REQUIRED_TRAINING_FIELDS:
                if not _nonempty(run.get(field)):
                    raise TS012Error(
                        "training run field %r must be non-empty" % field
                    )
            if run["id"] in seen:
                raise TS012Error("duplicate training run id %r" % run["id"])
            seen.add(run["id"])
            if run["status"] not in TRAINING_STATUSES:
                raise TS012Error(
                    "training run %r unknown status %r"
                    % (run["id"], run["status"])
                )
            frozen.append(
                {
                    "id": run["id"],
                    "model_ref": run["model_ref"],
                    "status": run["status"],
                }
            )
        self._runs = tuple(frozen)

    @property
    def runs(self):
        return tuple(dict(r) for r in self._runs)


# ---------------------------------------------------------------------------
# Positive tests
# ---------------------------------------------------------------------------
class TS012PositiveTests(unittest.TestCase):
    def test_pos_001_all_target_files_exist(self):
        for path in (
            DOC_12_PATH,
            EVIDENCE_LEDGER_PATH,
            RELEASE_GATES_PATH,
            MIGRATION_PLANS_PATH,
            NRTV_CONFIG_PATH,
            TRAINING_RUNS_PATH,
        ):
            self.assertTrue(os.path.isfile(path), "missing target %s" % path)

    def test_pos_002_evidence_ledger_append_only_and_hash_linked(self):
        data = load_yaml(EVIDENCE_LEDGER_PATH)
        self.assertEqual(data["ledger_id"], "evidence-ledger-ts012")
        self.assertEqual(data["spec_ref"], "TS-012/SPEC-16")
        ledger = EvidenceLedger(load_ledger_entries())
        self.assertGreaterEqual(len(ledger.entries), 1)
        # every recorded sha256 matches the actual digest of its ref file
        self.assertTrue(ledger.verify())
        for entry in ledger.entries:
            self.assertIn("id", entry)
            self.assertIn("sha256", entry)
            self.assertIn("ref", entry)
            path = _resolve_ref(entry["ref"], "evidence entry %r" % entry["id"])
            self.assertTrue(os.path.isfile(path), "dangling ref %r" % entry["ref"])
        # append-only: append returns a NEW ledger, the original is untouched
        original = ledger.entries
        appended = ledger.append(
            {
                "id": "EV-012-006",
                "sha256": original[0]["sha256"],
                "ref": original[0]["ref"],
            }
        )
        self.assertEqual(len(appended.entries), len(original) + 1)
        self.assertEqual(appended.entries[: len(original)], original)
        self.assertEqual(ledger.entries, original)
        # duplicate id is rejected - existing entries cannot be rewritten
        with self.assertRaises(TS012Error):
            ledger.append(dict(original[0]))
        # entries are immutable views: mutating a returned copy is a no-op
        view = ledger.entries
        view[0]["id"] = "mutated-view"
        self.assertNotEqual(ledger.entries[0]["id"], "mutated-view")
        with self.assertRaises(AttributeError):
            ledger.entries = ()

    def test_pos_003_release_gate_validates(self):
        data = load_yaml(RELEASE_GATES_PATH)
        self.assertEqual(data["release_id"], "release-gates-ts012")
        self.assertEqual(data["spec_ref"], "TS-012/SPEC-34")
        gates = ReleaseGates(load_gates())
        self.assertGreaterEqual(len(gates.gates), 2)
        ids = ledger_ids()
        # every required evidence id resolves in the ledger
        self.assertTrue(gates.validate(ids))
        for gate in gates.gates:
            self.assertIn("id", gate)
            self.assertIn("gate", gate)
            self.assertTrue(_nonempty(gate["required"]))
            for req in gate["required"]:
                self.assertIn(req, ids, "gate %s needs %s" % (gate["id"], req))
        # G17 and G18 are the release plane
        self.assertEqual(gates.by_name("G17")["gate"], "G17")
        self.assertEqual(gates.by_name("G18")["gate"], "G18")
        # the full evidence set supports every claim level
        for claim in ("LOCAL_DELIVERY", "SHADOW", "PRODUCTION"):
            self.assertTrue(gates.claim(claim, ids), "claim %s failed" % claim)

    def test_pos_004_nrtv_config_valid(self):
        data = load_yaml(NRTV_CONFIG_PATH)
        self.assertEqual(data["nrtv_id"], "nrtv-config-ts012")
        self.assertEqual(data["spec_ref"], "TS-012/SPEC-35")
        configs = NrtvConfig(load_nrtv())
        self.assertGreaterEqual(len(configs.configs), 1)
        for cfg in configs.configs:
            self.assertIn("id", cfg)
            self.assertTrue(_nonempty(cfg["runtime_window"]))
            self.assertTrue(_nonempty(cfg["condition"]))
            self.assertIn("independent", cfg["condition"])
            self.assertIn("no-return-to-source", cfg["condition"])

    def test_pos_005_migration_plans_well_formed(self):
        data = load_yaml(MIGRATION_PLANS_PATH)
        self.assertEqual(data["migration_id"], "migration-plans-ts012")
        self.assertEqual(data["spec_ref"], "TS-012/SPEC-31")
        plans = MigrationPlans(load_plans())
        self.assertGreaterEqual(len(plans.plans), 1)
        for plan in plans.plans:
            self.assertIn("id", plan)
            self.assertIn("from", plan)
            self.assertIn("to", plan)
            self.assertTrue(_nonempty(plan["from"]))
            self.assertTrue(_nonempty(plan["to"]))
            self.assertIn(plan["status"], MIGRATION_STATUSES)

    def test_pos_006_training_runs_well_formed(self):
        data = load_yaml(TRAINING_RUNS_PATH)
        self.assertEqual(data["training_id"], "training-runs-ts012")
        self.assertEqual(data["spec_ref"], "TS-012/CH35")
        runs = TrainingRuns(load_training())
        self.assertGreaterEqual(len(runs.runs), 1)
        for run in runs.runs:
            self.assertIn("id", run)
            self.assertIn("model_ref", run)
            self.assertTrue(_nonempty(run["model_ref"]))
            self.assertIn("ch35-training-packet", run["model_ref"])
            self.assertIn(run["status"], TRAINING_STATUSES)
            # honest ceilings: no self-declared PASS in this work order
            self.assertIn(run["status"], ("NOT_RUN", "DESIGN_CLOSED_NOT_RUN"))

    def test_pos_007_doc12_evidence_release_learning_nrtv_document(self):
        text = read_text(DOC_12_PATH)
        for token in (
            "SQS-THC",
            "WO-TS-REF-12",
            "TS-012",
            "ART-12",
            "MC-27",
            "CH33",
            "CH34",
            "CH35",
            "evidence/ledger.yaml",
            "release/gates.yaml",
            "migration/plans.yaml",
            "nrtv/config.yaml",
            "training/runs.yaml",
            "ERR_PRODUCTION_CLAIM_INFLATION",
            "ERR_CHECKSUM_MISMATCH",
            CLAIM_CEILING_LOCAL_DELIVERY,
            "F34-01",
            "F35-01",
            "Independent Release Team",
            "EvidenceReceipt",
            "ProvenanceAttestation",
            "DriftSignal",
            "LearningCandidate",
            "NRTVRun",
            "TrainingPacket",
            "G17",
            "G18",
        ):
            self.assertIn(token, text, "DOC-12 missing token %r" % token)


# ---------------------------------------------------------------------------
# Negative tests - a FRESH ReleaseGates instance and a FRESH evidence set are
# created per test case (setUp), so there is no cross-case contamination.
# ---------------------------------------------------------------------------
class TS012NegativeTests(unittest.TestCase):
    def setUp(self):
        self.gates = ReleaseGates(load_gates())
        self.evidence = set()

    def test_neg_001_production_with_empty_evidence(self):
        with self.assertRaises(TS012Error) as ctx:
            self.gates.claim("PRODUCTION", self.evidence)
        self.assertEqual(ctx.exception.code, ERR_PRODUCTION_CLAIM_INFLATION)
        self.assertIn("PRODUCTION", str(ctx.exception))
        self.assertIn("EV-012-001", str(ctx.exception))

    def test_neg_002_production_without_nrtv_evidence(self):
        # release-plane evidence present, NRTV evidence absent
        self.evidence.update(["EV-012-001", "EV-012-002", "EV-012-003"])
        with self.assertRaises(TS012Error) as ctx:
            self.gates.claim("PRODUCTION", self.evidence)
        self.assertEqual(ctx.exception.code, ERR_PRODUCTION_CLAIM_INFLATION)
        self.assertIn("EV-012-004", str(ctx.exception))
        self.assertIn("EV-012-005", str(ctx.exception))

    def test_neg_003_shadow_without_nrtv_evidence(self):
        # SHADOW also requires the NRTV gate; release evidence alone is not
        # enough for a claim above LOCAL_DELIVERY
        self.evidence.update(["EV-012-001", "EV-012-002", "EV-012-003"])
        with self.assertRaises(TS012Error) as ctx:
            self.gates.claim("SHADOW", self.evidence)
        self.assertEqual(ctx.exception.code, ERR_PRODUCTION_CLAIM_INFLATION)
        self.assertIn("EV-012-004", str(ctx.exception))

    def test_neg_004_failed_claim_never_mutates_state(self):
        before_gates = self.gates.gates
        before_evidence = set(self.evidence)
        with self.assertRaises(TS012Error):
            self.gates.claim("PRODUCTION", {})
        self.assertEqual(self.gates.gates, before_gates)
        self.assertEqual(self.evidence, before_evidence)
        # a fresh instance with the full evidence set is not contaminated
        fresh = ReleaseGates(load_gates())
        self.assertTrue(fresh.claim("PRODUCTION", ledger_ids()))


# ---------------------------------------------------------------------------
# Edge tests
# ---------------------------------------------------------------------------
class TS012EdgeTests(unittest.TestCase):
    def test_edge_001_empty_evidence_allowed(self):
        # an empty evidence ledger is a valid state (no evidence collected
        # yet); verify() passes with nothing to check
        ledger = EvidenceLedger([])
        self.assertEqual(len(ledger.entries), 0)
        self.assertTrue(ledger.verify())
        # but an empty ledger cannot support any claim (fail-closed)
        gates = ReleaseGates(load_gates())
        with self.assertRaises(TS012Error) as ctx:
            gates.claim("LOCAL_DELIVERY", [])
        self.assertEqual(ctx.exception.code, ERR_PRODUCTION_CLAIM_INFLATION)

    def test_edge_002_missing_required_field_rejected(self):
        # evidence entry missing sha256 -> field-naming error (code None),
        # distinct from ERR_PRODUCTION_CLAIM_INFLATION
        entries = [dict(e) for e in load_ledger_entries()]
        del entries[0]["sha256"]
        with self.assertRaises(TS012Error) as ctx:
            EvidenceLedger(entries)
        self.assertIn("sha256", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)
        # release gate missing required -> field-naming error
        gates = [dict(g) for g in load_gates()]
        del gates[0]["required"]
        with self.assertRaises(TS012Error) as ctx:
            ReleaseGates(gates)
        self.assertIn("required", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)
        # nrtv config missing condition -> field-naming error
        configs = [dict(c) for c in load_nrtv()]
        del configs[0]["condition"]
        with self.assertRaises(TS012Error) as ctx:
            NrtvConfig(configs)
        self.assertIn("condition", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)

    def test_edge_003_malformed_sha256_rejected(self):
        entries = [dict(e) for e in load_ledger_entries()]
        entries[0]["sha256"] = "not-a-sha256"
        with self.assertRaises(TS012Error) as ctx:
            EvidenceLedger(entries)
        self.assertIn("sha256", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)

    def test_edge_004_checksum_mismatch_rejected(self):
        # well-formed but wrong digest -> ERR_CHECKSUM_MISMATCH (fail-closed)
        entries = [dict(e) for e in load_ledger_entries()]
        entries[0]["sha256"] = "0" * 64
        ledger = EvidenceLedger(entries)
        with self.assertRaises(TS012Error) as ctx:
            ledger.verify()
        self.assertEqual(ctx.exception.code, ERR_CHECKSUM_MISMATCH)
        self.assertIn("docs/DOC-12.md", str(ctx.exception))

    def test_edge_005_duplicate_id_and_escaping_ref_rejected(self):
        # duplicate evidence id is an append-only violation
        entries = [dict(e) for e in load_ledger_entries()]
        entries.append(dict(entries[0]))
        with self.assertRaises(TS012Error) as ctx:
            EvidenceLedger(entries)
        self.assertIn("duplicate", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)
        # a ref that escapes the repo is rejected (fail-closed)
        entries = [dict(e) for e in load_ledger_entries()]
        entries[0]["ref"] = "../../outside-repo.txt"
        with self.assertRaises(TS012Error) as ctx:
            EvidenceLedger(entries)
        self.assertIn("escape", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)


if __name__ == "__main__":
    unittest.main()
