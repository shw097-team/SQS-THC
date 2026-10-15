# TS-009 Validation/risk/survival veto acceptance tests (WO-TS-REF-09).
#
# Pure stdlib unittest - no third-party dependencies. Deterministic and
# fail-closed: any missing file, malformed artifact, or unexpected construct
# raises and fails the suite. No broker write, no network.
#
# Positive: hard limits validate (id/metric/max/hard:true present), survival
# guards present and valid, validation runs (id/spec_ref/result) valid, and
# a stress fixture runs to its expected SURVIVES outcome.
# Negative: ERR_VETO_BYPASS - bypassing a hard limit (forbidden bypass flag,
# hard demoted from true) or a guard (action SKIP or an action outside the
# allowlist) - a FRESH validator is created per case (setUp), so there is no
# cross-case contamination; rejected validations never mutate their input.
# Edge: empty limits allowed; missing required field rejected (field-naming
# error, distinct from ERR_VETO_BYPASS); exposure exactly at the limit is not
# a breach.
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DOC_09_PATH = os.path.join(ROOT, "docs", "DOC-09.md")
VALIDATION_DIR = os.path.join(ROOT, "validation")
RISK_LIMITS_PATH = os.path.join(ROOT, "risk", "limits.yaml")
SURVIVAL_GUARDS_PATH = os.path.join(ROOT, "survival", "guards.yaml")
STRESS_FIXTURES_DIR = os.path.join(ROOT, "fixtures", "stress")

ERR_VETO_BYPASS = "ERR_VETO_BYPASS"
CLAIM_CEILING_LOCAL_DELIVERY = "LOCAL_DELIVERY"

REQUIRED_LIMIT_FIELDS = ("id", "metric", "max", "hard")
REQUIRED_GUARD_FIELDS = ("id", "condition", "action")
REQUIRED_RUN_FIELDS = ("id", "spec_ref", "result")
REQUIRED_STRESS_FIELDS = ("id", "scenario", "portfolio", "limits", "expected")
ALLOWED_GUARD_ACTIONS = ("VETO", "BLOCK", "STOP_LINE", "ABSTAIN")
ALLOWED_RUN_RESULTS = ("PASS", "FAIL", "ABSTAIN", "BLOCKED")
BYPASS_FLAGS = ("bypass", "bypass_enabled", "skip")

EXPECTED_LIMIT_IDS = [
    "limit-gross-exposure",
    "limit-net-exposure",
    "limit-liquidity-usage",
    "limit-stress-loss",
    "limit-concentration",
]
EXPECTED_GUARD_IDS = [
    "guard-ruin-barrier",
    "guard-unknown-exposure",
    "guard-fragility-mandate",
    "guard-blast-radius",
    "guard-optionality",
]
EXPECTED_RUN_IDS = [
    "validation-run-ch24-001",
    "validation-run-ch25-001",
    "validation-run-ch26-001",
]
EXPECTED_STRESS_FIXTURES = [
    "stress_valid.yaml",
    "limits_empty.yaml",
    "limit_bypass.yaml",
    "guard_skip.yaml",
    "limit_missing_field.yaml",
]


# ---------------------------------------------------------------------------
# Minimal deterministic YAML-subset parser (stdlib only, fail-closed).
# Supports the exact constructs used by the TS-009 artifacts:
#   - top-level 'key: value' scalars (plain, quoted, null, flow list)
#   - 'key:' followed by a block list of scalars
#   - 'key:' followed by a block list of single-level mappings
#     ('- key: value' plus indented 'key: value' body lines)
#   - 'key:' followed by a nested single-level mapping
#     (indented 'key: value' body lines, e.g. portfolio)
# Anything else raises ValueError. Plain numeric scalars become int/float so
# the stress runner can compare exposures against limits deterministically.
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
                        raise ValueError(
                            "nested block under mapping item not supported: %r" % nxt
                        )
                    item[k2] = _scalar(r2)
                    i += 1
                else:
                    raise ValueError(
                        "unexpected indentation %d in mapping item: %r" % (nind, nxt)
                    )
            items.append(item)
        else:
            items.append(_scalar(rest))
            i += 1
    return items, i


def _parse_nested_mapping(lines, i, indent):
    data = {}
    n = len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        cur = _indent(line)
        if cur < indent:
            break
        if cur > indent:
            raise ValueError(
                "unexpected indentation %d in nested mapping: %r" % (cur, line)
            )
        if line.strip().startswith("- "):
            break
        key, rest = _split_key(line.strip())
        key = key.strip()
        rest = rest.strip()
        if rest == "":
            raise ValueError("nested mapping value must be scalar: %r" % line)
        data[key] = _scalar(rest)
        i += 1
    return data, i


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
                nested, i = _parse_nested_mapping(lines, i + 1, nindent)
                data[key] = nested
        else:
            data[key] = _scalar(rest)
            i += 1
    return data


def read_text(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def load_yaml(path):
    return parse_yaml_subset(read_text(path))


def load_yaml_dir(directory):
    """Load every *.yaml in *directory*, sorted by name (deterministic)."""
    items = []
    for name in sorted(os.listdir(directory)):
        if not name.endswith(".yaml"):
            continue
        items.append(load_yaml(os.path.join(directory, name)))
    return items


def load_limits():
    return load_yaml(RISK_LIMITS_PATH)["limits"]


def load_guards():
    return load_yaml(SURVIVAL_GUARDS_PATH)["guards"]


def load_validation_runs():
    return load_yaml_dir(VALIDATION_DIR)


# ---------------------------------------------------------------------------
# Fail-closed TS-009 validation/risk/survival semantics used by the
# negative/edge cases.
# ---------------------------------------------------------------------------
class VetoError(Exception):
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


def _truthy(value):
    if value is True:
        return True
    if isinstance(value, str) and value.strip().lower() == "true":
        return True
    if value == 1:
        return True
    return False


class ValidationRiskSurvivalValidator(object):
    """Deterministic, fail-closed validator for TS-009 artifacts.

    Semantics:
    - Missing required field  -> rejected with code None (field named in the
      message); a missing field is NOT a veto bypass.
    - Bypass attempt          -> ERR_VETO_BYPASS: a hard limit carrying a
      bypass flag, a hard limit whose `hard` is not true, a guard whose
      action is SKIP or outside the allowlist, or a stress run that would
      breach while claiming to survive.
    - Validation never mutates inputs; a failed validation is a no-op.
    """

    def validate_limits(self, limits):
        if limits is None or not isinstance(limits, list):
            raise VetoError("limits must be a list")
        for limit in limits:
            if not isinstance(limit, dict):
                raise VetoError("each limit must be a mapping: %r" % (limit,))
            missing = [f for f in REQUIRED_LIMIT_FIELDS if f not in limit]
            if missing:
                raise VetoError(
                    "limit missing required field(s): " + ", ".join(missing)
                )
            for field in ("id", "metric"):
                if not _nonempty(limit.get(field)):
                    raise VetoError("limit field %r must be non-empty" % field)
            if not _nonempty(limit.get("max")):
                raise VetoError("limit field 'max' must be non-empty")
            if limit.get("hard") is not True:
                raise VetoError(
                    "limit %r must be hard:true (hard limits are never "
                    "overridable)" % (limit.get("id"),),
                    code=ERR_VETO_BYPASS,
                )
            for flag in BYPASS_FLAGS:
                if _truthy(limit.get(flag)):
                    raise VetoError(
                        "hard limit %r carries forbidden bypass flag %r"
                        % (limit.get("id"), flag),
                        code=ERR_VETO_BYPASS,
                    )
        return True

    def validate_guards(self, guards):
        if guards is None or not isinstance(guards, list):
            raise VetoError("guards must be a list")
        for guard in guards:
            if not isinstance(guard, dict):
                raise VetoError("each guard must be a mapping: %r" % (guard,))
            missing = [f for f in REQUIRED_GUARD_FIELDS if f not in guard]
            if missing:
                raise VetoError(
                    "guard missing required field(s): " + ", ".join(missing)
                )
            for field in ("id", "condition"):
                if not _nonempty(guard.get(field)):
                    raise VetoError("guard field %r must be non-empty" % field)
            action = guard.get("action")
            if not _nonempty(action):
                raise VetoError("guard field 'action' must be non-empty")
            action_upper = None
            if isinstance(action, str):
                action_upper = action.strip().upper()
            if action_upper == "SKIP":
                raise VetoError(
                    "guard %r action SKIP is a veto bypass" % (guard.get("id"),),
                    code=ERR_VETO_BYPASS,
                )
            if action_upper not in ALLOWED_GUARD_ACTIONS:
                raise VetoError(
                    "guard %r action %r is not in allowlist %r"
                    % (guard.get("id"), action, ALLOWED_GUARD_ACTIONS),
                    code=ERR_VETO_BYPASS,
                )
        return True

    def validate_validation_run(self, run):
        if not isinstance(run, dict):
            raise VetoError("validation run must be a mapping")
        missing = [f for f in REQUIRED_RUN_FIELDS if f not in run]
        if missing:
            raise VetoError(
                "validation run missing required field(s): " + ", ".join(missing)
            )
        for field in ("id", "spec_ref", "result"):
            if not _nonempty(run.get(field)):
                raise VetoError("validation run field %r must be non-empty" % field)
        spec_ref = run.get("spec_ref")
        if not isinstance(spec_ref, str) or "TS-009" not in spec_ref:
            raise VetoError(
                "validation run spec_ref must anchor to TS-009: %r" % (spec_ref,)
            )
        result = run.get("result")
        if result not in ALLOWED_RUN_RESULTS:
            raise VetoError(
                "validation run result %r not in %r" % (result, ALLOWED_RUN_RESULTS)
            )
        return True

    def validate_validation_runs(self, runs):
        if runs is None or not isinstance(runs, list):
            raise VetoError("validation runs must be a list")
        for run in runs:
            self.validate_validation_run(run)
        return True

    def run_stress(self, fixture):
        """Deterministic, fail-closed stress run for a TS-009 fixture.

        Returns {"id", "result", "violations"} where result is SURVIVES or
        BREACH. Raises VetoError on schema violations (code None) or when
        the computed outcome would bypass the fixture's expected veto
        (code ERR_VETO_BYPASS). Never mutates the fixture.
        """
        if not isinstance(fixture, dict):
            raise VetoError("stress fixture must be a mapping")
        missing = [f for f in REQUIRED_STRESS_FIELDS if f not in fixture]
        if missing:
            raise VetoError(
                "stress fixture missing required field(s): " + ", ".join(missing)
            )
        for field in ("id", "scenario", "expected"):
            if not _nonempty(fixture.get(field)):
                raise VetoError("stress fixture field %r must be non-empty" % field)
        portfolio = fixture.get("portfolio")
        limits = fixture.get("limits")
        if not isinstance(portfolio, dict) or not portfolio:
            raise VetoError("stress fixture portfolio must be a non-empty mapping")
        if not isinstance(limits, list) or not limits:
            raise VetoError("stress fixture limits must be a non-empty list")
        limit_map = {}
        for item in limits:
            if not isinstance(item, dict):
                raise VetoError("each stress limit must be a mapping")
            if "metric" not in item or "max" not in item:
                raise VetoError("each stress limit must carry metric and max")
            limit_map[item["metric"]] = item["max"]
        violations = []
        for metric, value in portfolio.items():
            if metric in limit_map and value > limit_map[metric]:
                violations.append((metric, value, limit_map[metric]))
        result = "BREACH" if violations else "SURVIVES"
        if result != fixture.get("expected"):
            raise VetoError(
                "stress fixture %r expected %r but run produced %r (violations=%r)"
                % (fixture.get("id"), fixture.get("expected"), result, violations),
                code=ERR_VETO_BYPASS,
            )
        return {"id": fixture.get("id"), "result": result, "violations": violations}


# ---------------------------------------------------------------------------
# Positive tests
# ---------------------------------------------------------------------------
class TS009PositiveTests(unittest.TestCase):
    def test_pos_001_all_target_files_exist(self):
        self.assertTrue(os.path.isfile(DOC_09_PATH), "missing docs/DOC-09.md")
        self.assertTrue(os.path.isfile(RISK_LIMITS_PATH), "missing risk/limits.yaml")
        self.assertTrue(
            os.path.isfile(SURVIVAL_GUARDS_PATH), "missing survival/guards.yaml"
        )
        self.assertTrue(os.path.isdir(VALIDATION_DIR), "missing validation/")
        for name in EXPECTED_RUN_IDS:
            self.assertTrue(
                os.path.isfile(os.path.join(VALIDATION_DIR, name + ".yaml")),
                "missing validation run: %s" % name,
            )
        self.assertTrue(
            os.path.isdir(STRESS_FIXTURES_DIR), "missing fixtures/stress/"
        )
        for name in EXPECTED_STRESS_FIXTURES:
            self.assertTrue(
                os.path.isfile(os.path.join(STRESS_FIXTURES_DIR, name)),
                "missing stress fixture: %s" % name,
            )

    def test_pos_002_hard_limits_present_and_validate(self):
        limits = load_limits()
        validator = ValidationRiskSurvivalValidator()
        self.assertTrue(validator.validate_limits(limits))
        ids = [limit["id"] for limit in limits]
        self.assertEqual(sorted(ids), sorted(EXPECTED_LIMIT_IDS))
        for limit in limits:
            for field in ("id", "metric", "max", "hard"):
                self.assertIn(field, limit, "limit missing %r" % field)
                self.assertTrue(
                    limit[field],
                    "limit %r field %r empty" % (limit.get("id"), field),
                )
            self.assertIs(limit["hard"], True, "limit must be hard:true")

    def test_pos_003_survival_guards_present_and_validate(self):
        guards = load_guards()
        validator = ValidationRiskSurvivalValidator()
        self.assertTrue(validator.validate_guards(guards))
        ids = [guard["id"] for guard in guards]
        self.assertEqual(sorted(ids), sorted(EXPECTED_GUARD_IDS))
        for guard in guards:
            for field in ("id", "condition", "action"):
                self.assertIn(field, guard)
                self.assertTrue(guard[field])
            self.assertIn(guard["action"], ALLOWED_GUARD_ACTIONS)
            self.assertNotEqual(guard["action"], "SKIP")

    def test_pos_004_validation_runs_validate(self):
        runs = load_validation_runs()
        validator = ValidationRiskSurvivalValidator()
        self.assertTrue(validator.validate_validation_runs(runs))
        ids = [run["id"] for run in runs]
        self.assertEqual(sorted(ids), sorted(EXPECTED_RUN_IDS))
        for run in runs:
            for field in ("id", "spec_ref", "result"):
                self.assertIn(field, run)
                self.assertTrue(run[field])
            self.assertIn("TS-009", run["spec_ref"])
            self.assertIn(run["result"], ALLOWED_RUN_RESULTS)

    def test_pos_005_stress_fixture_runs(self):
        fixture = load_yaml(os.path.join(STRESS_FIXTURES_DIR, "stress_valid.yaml"))
        outcome = ValidationRiskSurvivalValidator().run_stress(fixture)
        self.assertEqual(outcome["result"], "SURVIVES")
        self.assertEqual(outcome["result"], fixture["expected"])
        self.assertEqual(outcome["violations"], [])
        self.assertEqual(outcome["id"], fixture["id"])

    def test_pos_006_doc09_validation_risk_document(self):
        text = read_text(DOC_09_PATH)
        for token in (
            "SQS-THC",
            "WO-TS-REF-09",
            "TS-009",
            "ART-09",
            "MC-21",
            "MC-22",
            "MC-23",
            "CH24",
            "CH25",
            "CH26",
            "validation/",
            "risk/limits.yaml",
            "survival/guards.yaml",
            "fixtures/stress/",
            "ERR_VETO_BYPASS",
            CLAIM_CEILING_LOCAL_DELIVERY,
        ):
            self.assertIn(token, text, "DOC-09 missing token %r" % token)


# ---------------------------------------------------------------------------
# Negative tests - a FRESH ValidationRiskSurvivalValidator is created per
# test case (setUp), so there is no cross-case contamination.
# ---------------------------------------------------------------------------
class TS009NegativeTests(unittest.TestCase):
    def setUp(self):
        self.validator = ValidationRiskSurvivalValidator()

    def test_neg_001_hard_limit_bypass_flag_raises_err_veto_bypass(self):
        data = load_yaml(
            os.path.join(STRESS_FIXTURES_DIR, "limit_bypass.yaml")
        )
        with self.assertRaises(VetoError) as ctx:
            self.validator.validate_limits(data["limits"])
        self.assertEqual(ctx.exception.code, ERR_VETO_BYPASS)
        self.assertIn("bypass", str(ctx.exception))

    def test_neg_002_guard_action_skip_raises_err_veto_bypass(self):
        data = load_yaml(os.path.join(STRESS_FIXTURES_DIR, "guard_skip.yaml"))
        with self.assertRaises(VetoError) as ctx:
            self.validator.validate_guards(data["guards"])
        self.assertEqual(ctx.exception.code, ERR_VETO_BYPASS)
        self.assertIn("SKIP", str(ctx.exception))

    def test_neg_003_hard_demoted_from_true_raises_err_veto_bypass(self):
        limits = load_limits()
        limits[0]["hard"] = False  # try to demote a hard limit to soft
        with self.assertRaises(VetoError) as ctx:
            self.validator.validate_limits(limits)
        self.assertEqual(ctx.exception.code, ERR_VETO_BYPASS)

    def test_neg_004_unknown_guard_action_raises_err_veto_bypass(self):
        guards = load_guards()
        guards[0]["action"] = "IGNORE"  # not in the allowlist
        with self.assertRaises(VetoError) as ctx:
            self.validator.validate_guards(guards)
        self.assertEqual(ctx.exception.code, ERR_VETO_BYPASS)

    def test_neg_005_failed_validation_does_not_mutate_input(self):
        data = load_yaml(
            os.path.join(STRESS_FIXTURES_DIR, "limit_bypass.yaml")
        )
        before = repr(data)
        with self.assertRaises(VetoError):
            self.validator.validate_limits(data["limits"])
        # fail-closed: no partial write from the rejected validation
        self.assertEqual(repr(data), before)

    def test_neg_006_fresh_validator_accepts_clean_artifacts(self):
        # fresh state per case: previous failures must not leak state
        fresh = ValidationRiskSurvivalValidator()
        self.assertTrue(fresh.validate_limits(load_limits()))
        self.assertTrue(fresh.validate_guards(load_guards()))
        self.assertTrue(fresh.validate_validation_runs(load_validation_runs()))

    def test_neg_007_stress_runner_rejects_smuggled_breach(self):
        # CH25 anti-case: aggregate risk passes while one hard limit breaches.
        # A fixture claiming SURVIVES while an exposure exceeds its limit is a
        # veto bypass and must be NACK'd with ERR_VETO_BYPASS.
        fixture = load_yaml(os.path.join(STRESS_FIXTURES_DIR, "stress_valid.yaml"))
        fixture["portfolio"]["gross_exposure"] = 1.60  # > limit 1.50
        with self.assertRaises(VetoError) as ctx:
            self.validator.run_stress(fixture)
        self.assertEqual(ctx.exception.code, ERR_VETO_BYPASS)
        self.assertIn("BREACH", str(ctx.exception))


# ---------------------------------------------------------------------------
# Edge tests
# ---------------------------------------------------------------------------
class TS009EdgeTests(unittest.TestCase):
    def test_edge_001_empty_limits_allowed(self):
        self.assertTrue(ValidationRiskSurvivalValidator().validate_limits([]))
        data = load_yaml(os.path.join(STRESS_FIXTURES_DIR, "limits_empty.yaml"))
        self.assertEqual(data["limits"], [])
        self.assertTrue(
            ValidationRiskSurvivalValidator().validate_limits(data["limits"])
        )

    def test_edge_002_missing_required_field_rejected(self):
        data = load_yaml(
            os.path.join(STRESS_FIXTURES_DIR, "limit_missing_field.yaml")
        )
        with self.assertRaises(VetoError) as ctx:
            ValidationRiskSurvivalValidator().validate_limits(data["limits"])
        self.assertIn("metric", str(ctx.exception))
        # missing field != veto bypass (distinct from ERR_VETO_BYPASS)
        self.assertIsNone(ctx.exception.code)

    def test_edge_003_missing_guard_action_rejected(self):
        guards = load_guards()
        del guards[0]["action"]
        with self.assertRaises(VetoError) as ctx:
            ValidationRiskSurvivalValidator().validate_guards(guards)
        self.assertIn("action", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)

    def test_edge_004_missing_run_result_rejected(self):
        runs = load_validation_runs()
        del runs[0]["result"]
        with self.assertRaises(VetoError) as ctx:
            ValidationRiskSurvivalValidator().validate_validation_runs(runs)
        self.assertIn("result", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)

    def test_edge_005_exposure_equal_to_limit_is_not_a_breach(self):
        fixture = load_yaml(os.path.join(STRESS_FIXTURES_DIR, "stress_valid.yaml"))
        fixture["portfolio"]["gross_exposure"] = 1.50  # exactly at the limit
        outcome = ValidationRiskSurvivalValidator().run_stress(fixture)
        self.assertEqual(outcome["result"], "SURVIVES")
        self.assertEqual(outcome["violations"], [])

    def test_edge_006_parser_fail_closed_on_unexpected_construct(self):
        with self.assertRaises(ValueError):
            parse_yaml_subset("top:\n  nested:\n    deep: 1\n")


if __name__ == "__main__":
    unittest.main()
