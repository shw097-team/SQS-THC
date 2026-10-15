# TS-013 Legacy donor migration and regression acceptance tests (WO-TS-REF-13).
#
# Pure stdlib unittest - no third-party dependencies. Deterministic and
# fail-closed: any missing file, malformed artifact, duplicate donor mapping
# or unexpected construct raises and fails the suite. No broker write, no
# network.
#
# Positive: the donor matrix (migration/donor-matrix.yaml) maps each donor_id
# to exactly one target (single truth: donor_id, target, single_truth: true);
# the cutover plans (migration/cutover-plans/) are valid (each plan carries
# id, ordered steps and an explicit rollback); the legacy regression cases
# (tests/legacy-regression/) and deprecation records (deprecation/) are
# well-formed.
# Negative: ERR_SECOND_TRUTH_REINTRODUCED - reintroducing a second truth,
# e.g. the same donor_id mapped to two different targets (or a donor entry
# that is not single_truth), is rejected. A FRESH donor matrix is built per
# test case so there is no cross-case contamination; a rejected matrix never
# mutates the canonical artifact.
# Edge: an empty migration (no donors) is a valid deterministic state;
# a missing required field is rejected with a field-naming error (code None),
# distinct from ERR_SECOND_TRUTH_REINTRODUCED.
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DONOR_MATRIX_PATH = os.path.join(ROOT, "migration", "donor-matrix.yaml")
CUTOVER_PLANS_PATH = os.path.join(
    ROOT, "migration", "cutover-plans", "cutover-plans.yaml"
)
REGRESSION_CASES_PATH = os.path.join(
    ROOT, "tests", "legacy-regression", "regression-cases.yaml"
)
DEPRECATION_RECORDS_PATH = os.path.join(ROOT, "deprecation", "records.yaml")

ERR_SECOND_TRUTH_REINTRODUCED = "ERR_SECOND_TRUTH_REINTRODUCED"

REQUIRED_DONOR_FIELDS = ("donor_id", "target", "single_truth")
REQUIRED_PLAN_FIELDS = ("id", "steps", "rollback")
REQUIRED_REGRESSION_FIELDS = ("id", "test", "result")
REQUIRED_DEPRECATION_FIELDS = ("id", "artifact", "reason")


# ---------------------------------------------------------------------------
# Minimal deterministic YAML-subset parser (stdlib only, fail-closed).
# Supports the exact constructs used by the TS-013 artifacts:
#   - top-level 'key: value' scalars (plain, quoted, null, flow list)
#   - 'key:' followed by a block list
#   - block-list mapping items '- key: value' with flat 'key2: value2' pairs
#     and nested block lists under a mapping key
# Anything else raises ValueError.
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
                    "nested mapping not used by TS-013 artifacts: %r" % nxt
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


def load_donors():
    return load_yaml(DONOR_MATRIX_PATH)["donors"]


def load_plans():
    return load_yaml(CUTOVER_PLANS_PATH)["plans"]


def load_regression_cases():
    return load_yaml(REGRESSION_CASES_PATH)["cases"]


def load_deprecation_records():
    return load_yaml(DEPRECATION_RECORDS_PATH)["records"]


# ---------------------------------------------------------------------------
# Fail-closed TS-013 legacy donor migration semantics.
# ---------------------------------------------------------------------------
class TS013Error(Exception):
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
        raise TS013Error("%s must be a mapping" % label)
    missing = [f for f in fields if f not in record]
    if missing:
        raise TS013Error(
            "%s missing required field(s): %s" % (label, ", ".join(missing))
        )


class DonorMatrix(object):
    """Deterministic, fail-closed donor->target matrix (SPEC-31 / CH34).

    Single truth: each donor_id maps to exactly ONE target and every entry
    must declare single_truth: true. A duplicate donor_id - e.g. the same
    donor mapped to two targets - reintroduces a second truth and raises
    ERR_SECOND_TRUTH_REINTRODUCED. Instances are immutable tuples; a fresh
    matrix is built per test case so rejected data never leaks state.
    """

    def __init__(self, donors):
        if not isinstance(donors, list):
            raise TS013Error("donor matrix must be a list")
        seen = set()
        frozen = []
        for donor in donors:
            _require_fields(donor, REQUIRED_DONOR_FIELDS, "donor entry")
            for field in REQUIRED_DONOR_FIELDS:
                if not _nonempty(donor.get(field)):
                    raise TS013Error(
                        "donor entry field %r must be non-empty" % field
                    )
            if donor["donor_id"] in seen:
                raise TS013Error(
                    "donor %r mapped to more than one target "
                    "(%r) reintroduces a second truth"
                    % (donor["donor_id"], donor["target"]),
                    code=ERR_SECOND_TRUTH_REINTRODUCED,
                )
            seen.add(donor["donor_id"])
            if donor["single_truth"] is not True:
                raise TS013Error(
                    "donor %r must declare single_truth: true"
                    % donor["donor_id"],
                    code=ERR_SECOND_TRUTH_REINTRODUCED,
                )
            frozen.append(
                {
                    "donor_id": donor["donor_id"],
                    "target": donor["target"],
                    "single_truth": donor["single_truth"],
                }
            )
        self._donors = tuple(frozen)

    @property
    def donors(self):
        return tuple(dict(d) for d in self._donors)

    @property
    def donor_ids(self):
        return tuple(d["donor_id"] for d in self._donors)

    @property
    def targets(self):
        return tuple(d["target"] for d in self._donors)

    def target_for(self, donor_id):
        for donor in self._donors:
            if donor["donor_id"] == donor_id:
                return donor["target"]
        raise TS013Error("unknown donor_id %r" % donor_id)


class CutoverPlans(object):
    """Deterministic, fail-closed cutover plans (SPEC-31 / CH34).

    Each plan carries id, a non-empty ordered list of steps and an explicit
    rollback path; a plan missing any required field - especially rollback -
    is rejected (fail-closed).
    """

    def __init__(self, plans):
        if not isinstance(plans, list):
            raise TS013Error("cutover plans must be a list")
        seen = set()
        frozen = []
        for plan in plans:
            _require_fields(plan, REQUIRED_PLAN_FIELDS, "cutover plan")
            for field in REQUIRED_PLAN_FIELDS:
                if not _nonempty(plan.get(field)):
                    raise TS013Error(
                        "cutover plan field %r must be non-empty" % field
                    )
            if plan["id"] in seen:
                raise TS013Error(
                    "duplicate cutover plan id %r" % plan["id"]
                )
            seen.add(plan["id"])
            steps = plan["steps"]
            if not isinstance(steps, list) or not steps:
                raise TS013Error(
                    "cutover plan %r steps must be a non-empty list"
                    % plan["id"]
                )
            for step in steps:
                if not isinstance(step, str) or not step.strip():
                    raise TS013Error(
                        "cutover plan %r step must be a non-empty string"
                        % plan["id"]
                    )
            frozen.append(
                {
                    "id": plan["id"],
                    "steps": tuple(step.strip() for step in steps),
                    "rollback": plan["rollback"].strip(),
                }
            )
        self._plans = tuple(frozen)

    @property
    def plans(self):
        return tuple(dict(p) for p in self._plans)


class RegressionCases(object):
    """Legacy regression cases (LGR-13 / LGR-14): id, test, result."""

    def __init__(self, cases):
        if not isinstance(cases, list):
            raise TS013Error("legacy regression cases must be a list")
        seen = set()
        frozen = []
        for case in cases:
            _require_fields(case, REQUIRED_REGRESSION_FIELDS, "regression case")
            for field in REQUIRED_REGRESSION_FIELDS:
                if not _nonempty(case.get(field)):
                    raise TS013Error(
                        "regression case field %r must be non-empty" % field
                    )
            if case["id"] in seen:
                raise TS013Error(
                    "duplicate regression case id %r" % case["id"]
                )
            seen.add(case["id"])
            frozen.append(
                {
                    "id": case["id"],
                    "test": case["test"].strip(),
                    "result": case["result"].strip(),
                }
            )
        self._cases = tuple(frozen)

    @property
    def cases(self):
        return tuple(dict(c) for c in self._cases)


class DeprecationRecords(object):
    """Deprecation records (SPEC-31 / SPEC-33): id, artifact, reason."""

    def __init__(self, records):
        if not isinstance(records, list):
            raise TS013Error("deprecation records must be a list")
        seen = set()
        frozen = []
        for record in records:
            _require_fields(
                record, REQUIRED_DEPRECATION_FIELDS, "deprecation record"
            )
            for field in REQUIRED_DEPRECATION_FIELDS:
                if not _nonempty(record.get(field)):
                    raise TS013Error(
                        "deprecation record field %r must be non-empty"
                        % field
                    )
            if record["id"] in seen:
                raise TS013Error(
                    "duplicate deprecation record id %r" % record["id"]
                )
            seen.add(record["id"])
            frozen.append(
                {
                    "id": record["id"],
                    "artifact": record["artifact"].strip(),
                    "reason": record["reason"].strip(),
                }
            )
        self._records = tuple(frozen)

    @property
    def records(self):
        return tuple(dict(r) for r in self._records)


# ---------------------------------------------------------------------------
# Positive tests
# ---------------------------------------------------------------------------
class TS013PositiveTests(unittest.TestCase):
    def test_pos_001_all_target_files_exist(self):
        for path in (
            DONOR_MATRIX_PATH,
            CUTOVER_PLANS_PATH,
            REGRESSION_CASES_PATH,
            DEPRECATION_RECORDS_PATH,
        ):
            self.assertTrue(os.path.isfile(path), "missing target %s" % path)

    def test_pos_002_donor_matrix_maps_each_donor_once(self):
        data = load_yaml(DONOR_MATRIX_PATH)
        self.assertEqual(data["matrix_id"], "donor-matrix-ts013")
        self.assertEqual(data["spec_ref"], "TS-013/SPEC-31")
        matrix = DonorMatrix(load_donors())
        # single truth: every donor_id appears exactly once
        ids = matrix.donor_ids
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(ids)
        for donor in matrix.donors:
            self.assertEqual(donor["single_truth"], True)
            self.assertTrue(donor["target"].strip())
            # deterministic lookup returns exactly one target
            self.assertEqual(
                matrix.target_for(donor["donor_id"]), donor["target"]
            )

    def test_pos_003_cutover_plans_valid(self):
        data = load_yaml(CUTOVER_PLANS_PATH)
        self.assertEqual(data["cutover_id"], "cutover-plans-ts013")
        self.assertEqual(data["spec_ref"], "TS-013/SPEC-31")
        plans = CutoverPlans(load_plans())
        self.assertTrue(plans.plans)
        for plan in plans.plans:
            self.assertTrue(plan["id"].strip())
            self.assertIsInstance(plan["steps"], tuple)
            self.assertTrue(plan["steps"])
            self.assertTrue(plan["rollback"].strip())

    def test_pos_004_legacy_regression_cases_valid(self):
        data = load_yaml(REGRESSION_CASES_PATH)
        self.assertEqual(data["regression_id"], "legacy-regression-ts013")
        self.assertEqual(data["spec_ref"], "TS-013/LGR-13")
        cases = RegressionCases(load_regression_cases())
        self.assertTrue(cases.cases)
        for case in cases.cases:
            self.assertTrue(case["id"].strip())
            self.assertTrue(case["test"].strip())
            self.assertTrue(case["result"].strip())

    def test_pos_005_deprecation_records_valid(self):
        data = load_yaml(DEPRECATION_RECORDS_PATH)
        self.assertEqual(data["deprecation_id"], "deprecation-records-ts013")
        self.assertEqual(data["spec_ref"], "TS-013/SPEC-31")
        records = DeprecationRecords(load_deprecation_records())
        self.assertTrue(records.records)
        for record in records.records:
            self.assertTrue(record["id"].strip())
            self.assertTrue(record["artifact"].strip())
            self.assertTrue(record["reason"].strip())


# ---------------------------------------------------------------------------
# Negative tests
# ---------------------------------------------------------------------------
class TS013NegativeTests(unittest.TestCase):
    def setUp(self):
        # fresh state per case: the canonical on-disk matrix is loaded
        # independently for every test, and rejected matrices never mutate it
        self.canonical = DonorMatrix(load_donors())

    def test_neg_001_duplicate_donor_two_targets_rejected(self):
        # same donor_id mapped to two different targets reintroduces a
        # second truth
        donors = [dict(d) for d in self.canonical.donors]
        donors.append(
            {
                "donor_id": donors[0]["donor_id"],
                "target": "some-other-target",
                "single_truth": True,
            }
        )
        with self.assertRaises(TS013Error) as ctx:
            DonorMatrix(donors)
        self.assertEqual(ctx.exception.code, ERR_SECOND_TRUTH_REINTRODUCED)
        self.assertIn("second truth", str(ctx.exception))
        self.assertIn(donors[0]["donor_id"], str(ctx.exception))

    def test_neg_002_non_single_truth_entry_rejected(self):
        # a donor entry that is not single_truth also reintroduces a second
        # truth
        donors = [dict(d) for d in self.canonical.donors]
        donors[0]["single_truth"] = False
        with self.assertRaises(TS013Error) as ctx:
            DonorMatrix(donors)
        self.assertEqual(ctx.exception.code, ERR_SECOND_TRUTH_REINTRODUCED)

    def test_neg_003_rejected_matrix_never_mutates_canonical_state(self):
        before = self.canonical.donors
        donors = [dict(d) for d in before]
        donors.append(dict(donors[0]))
        with self.assertRaises(TS013Error):
            DonorMatrix(donors)
        # canonical artifact is untouched and still single truth
        self.assertEqual(self.canonical.donors, before)
        fresh = DonorMatrix(load_donors())
        self.assertEqual(fresh.donor_ids, tuple(d["donor_id"] for d in before))

    def test_neg_004_duplicate_plan_id_rejected(self):
        plans = [dict(p) for p in load_plans()]
        plans.append(dict(plans[0]))
        with self.assertRaises(TS013Error) as ctx:
            CutoverPlans(plans)
        self.assertIn("duplicate cutover plan id", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)


# ---------------------------------------------------------------------------
# Edge tests
# ---------------------------------------------------------------------------
class TS013EdgeTests(unittest.TestCase):
    def test_edge_001_empty_migration_allowed(self):
        # an empty donor matrix is a valid deterministic state: no donors
        # migrated yet, and lookups fail closed
        matrix = DonorMatrix([])
        self.assertEqual(matrix.donors, ())
        self.assertEqual(matrix.donor_ids, ())
        self.assertEqual(matrix.targets, ())
        with self.assertRaises(TS013Error) as ctx:
            matrix.target_for("legacy-provisional-ledger")
        self.assertIsNone(ctx.exception.code)

    def test_edge_002_missing_required_field_rejected(self):
        # donor entry missing target -> field-naming error (code None),
        # distinct from ERR_SECOND_TRUTH_REINTRODUCED
        donors = [dict(d) for d in load_donors()]
        del donors[0]["target"]
        with self.assertRaises(TS013Error) as ctx:
            DonorMatrix(donors)
        self.assertIn("target", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)

        # cutover plan missing rollback -> field-naming error (fail-closed)
        plans = [dict(p) for p in load_plans()]
        del plans[0]["rollback"]
        with self.assertRaises(TS013Error) as ctx:
            CutoverPlans(plans)
        self.assertIn("rollback", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)

        # regression case missing result -> field-naming error
        cases = [dict(c) for c in load_regression_cases()]
        del cases[0]["result"]
        with self.assertRaises(TS013Error) as ctx:
            RegressionCases(cases)
        self.assertIn("result", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)

        # deprecation record missing reason -> field-naming error
        records = [dict(r) for r in load_deprecation_records()]
        del records[0]["reason"]
        with self.assertRaises(TS013Error) as ctx:
            DeprecationRecords(records)
        self.assertIn("reason", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)

    def test_edge_003_empty_steps_rejected(self):
        # a cutover plan without any steps is not actionable (fail-closed)
        plans = [dict(p) for p in load_plans()]
        plans[0]["steps"] = []
        with self.assertRaises(TS013Error) as ctx:
            CutoverPlans(plans)
        self.assertIn("steps", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)

    def test_edge_004_unknown_donor_lookup_rejected(self):
        # fail-closed: a donor that is not in the matrix has no target
        matrix = DonorMatrix(load_donors())
        with self.assertRaises(TS013Error) as ctx:
            matrix.target_for("never-migrated-donor")
        self.assertIn("unknown donor_id", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)


if __name__ == "__main__":
    unittest.main()
