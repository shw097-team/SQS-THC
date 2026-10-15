# TS-007 investment mission & factor research acceptance tests (WO-TS-REF-07).
#
# Pure stdlib unittest - no third-party dependencies. Deterministic and
# fail-closed: any missing file, malformed artifact, or unexpected construct
# raises and fails the suite. No broker write, no network.
#
# Positive: mission validates (mandate present, claim ceiling LOCAL_DELIVERY),
# universe entries valid, factor IDs unique with source refs.
# Negative: mandate violation raises ERR_MANDATE_VIOLATION (factor without
# source, or universe entry without tradable flag) - a FRESH validator is
# created per case (setUp), so there is no cross-case contamination.
# Edge: empty factors list allowed; missing required field rejected.
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DOC_07_PATH = os.path.join(ROOT, "docs", "DOC-07.md")
MISSION_PATH = os.path.join(ROOT, "research", "mission.yaml")
UNIVERSE_PATH = os.path.join(ROOT, "research", "universe.yaml")
FACTORS_DIR = os.path.join(ROOT, "research", "factors")
FIXTURES_DIR = os.path.join(ROOT, "fixtures", "research")

ERR_MANDATE_VIOLATION = "ERR_MANDATE_VIOLATION"
CLAIM_CEILING_LOCAL_DELIVERY = "LOCAL_DELIVERY"

REQUIRED_MISSION_FIELDS = (
    "mission_id",
    "schema_version",
    "mandate",
    "non_goals",
    "claim_ceiling",
)
REQUIRED_UNIVERSE_ENTRY_FIELDS = ("id", "symbol", "tradable", "data_source")
REQUIRED_FACTOR_FIELDS = ("id", "source", "definition", "guard")
EXPECTED_FACTOR_IDS = ["factor-momentum", "factor-reversal", "factor-liquidity"]


# ---------------------------------------------------------------------------
# Minimal deterministic YAML-subset parser (stdlib only, fail-closed).
# Supports the exact constructs used by the TS-007 artifacts:
#   - top-level 'key: value' scalars (plain, quoted, null, flow list)
#   - 'key:' followed by a block list of scalars
#   - 'key:' followed by a block list of single-level mappings
#     ('- key: value' plus indented 'key: value' body lines)
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
                raise ValueError("nested mapping not supported: %r" % nxt)
        else:
            data[key] = _scalar(rest)
            i += 1
    return data


def read_text(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def load_yaml(path):
    return parse_yaml_subset(read_text(path))


def load_factors(factors_dir):
    """Load every *.yaml in *factors_dir*, sorted by name (deterministic)."""
    factors = []
    for name in sorted(os.listdir(factors_dir)):
        if not name.endswith(".yaml"):
            continue
        factors.append(load_yaml(os.path.join(factors_dir, name)))
    return factors


# ---------------------------------------------------------------------------
# Fail-closed TS-007 validation semantics used by the negative/edge cases.
# ---------------------------------------------------------------------------
class MandateError(Exception):
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


class InvestmentResearchValidator(object):
    """Deterministic, fail-closed validator for TS-007 artifacts.

    Semantics:
    - Missing required field  -> rejected with code None (field named in the
      message); a missing field is NOT a mandate violation.
    - Mandate violation       -> ERR_MANDATE_VIOLATION: factor without source,
      universe entry without tradable flag, duplicate factor/universe IDs, or
      mission claim ceiling above LOCAL_DELIVERY.
    - Validation never mutates inputs; a failed validation is a no-op.
    """

    def validate_mission(self, mission):
        if not isinstance(mission, dict):
            raise MandateError("mission must be a mapping")
        missing = [f for f in REQUIRED_MISSION_FIELDS if f not in mission]
        if missing:
            raise MandateError(
                "missing required field(s): " + ", ".join(missing)
            )
        for field in ("mission_id", "schema_version", "owner_id", "source_locator"):
            if not _nonempty(mission.get(field)):
                raise MandateError(
                    "required field %r must be non-empty" % field
                )
        if not _nonempty(mission.get("mandate")):
            raise MandateError("required field 'mandate' must be non-empty")
        source = mission.get("source_locator")
        if not isinstance(source, str) or "#" not in source:
            raise MandateError(
                "source_locator must be a resolvable anchored locator: %r"
                % (source,)
            )
        ceiling = mission.get("claim_ceiling")
        if ceiling != CLAIM_CEILING_LOCAL_DELIVERY:
            raise MandateError(
                "claim ceiling must be %r, got %r"
                % (CLAIM_CEILING_LOCAL_DELIVERY, ceiling),
                code=ERR_MANDATE_VIOLATION,
            )
        return True

    def validate_universe_entry(self, entry):
        if not isinstance(entry, dict):
            raise MandateError("universe entry must be a mapping")
        missing = [f for f in REQUIRED_UNIVERSE_ENTRY_FIELDS if f not in entry]
        if missing:
            raise MandateError(
                "universe entry missing required field(s): "
                + ", ".join(missing),
                code=ERR_MANDATE_VIOLATION,
            )
        for field in ("id", "symbol", "data_source"):
            if not _nonempty(entry.get(field)):
                raise MandateError(
                    "universe entry field %r must be non-empty" % field,
                    code=ERR_MANDATE_VIOLATION,
                )
        if entry.get("tradable") is not True:
            raise MandateError(
                "universe entry %r is not tradable (tradable must be True)"
                % entry.get("id"),
                code=ERR_MANDATE_VIOLATION,
            )
        return True

    def validate_universe(self, universe):
        if not isinstance(universe, dict):
            raise MandateError("universe must be a mapping")
        for field in ("universe_id", "schema_version", "universe_version"):
            if not _nonempty(universe.get(field)):
                raise MandateError(
                    "universe required field %r missing/empty" % field
                )
        entries = universe.get("entries", [])
        if not isinstance(entries, list):
            raise MandateError("universe entries must be a list")
        ids = []
        for entry in entries:
            self.validate_universe_entry(entry)
            ids.append(entry["id"])
        if len(ids) != len(set(ids)):
            raise MandateError(
                "universe entry ids must be unique: %r" % ids,
                code=ERR_MANDATE_VIOLATION,
            )
        return True

    def validate_factor(self, factor):
        if not isinstance(factor, dict):
            raise MandateError("factor must be a mapping")
        missing = [f for f in REQUIRED_FACTOR_FIELDS if f not in factor]
        if missing:
            raise MandateError(
                "factor missing required field(s): " + ", ".join(missing),
                code=ERR_MANDATE_VIOLATION,
            )
        for field in ("id", "source", "definition", "guard"):
            if not _nonempty(factor.get(field)):
                raise MandateError(
                    "factor field %r must be non-empty" % field,
                    code=ERR_MANDATE_VIOLATION,
                )
        source = factor.get("source")
        if not isinstance(source, str) or "#" not in source:
            raise MandateError(
                "factor source must be a resolvable anchored locator: %r"
                % (source,),
                code=ERR_MANDATE_VIOLATION,
            )
        return True

    def validate_factors(self, factors):
        if not isinstance(factors, list):
            raise MandateError("factors must be a list")
        ids = []
        for factor in factors:
            self.validate_factor(factor)
            ids.append(factor["id"])
        if len(ids) != len(set(ids)):
            raise MandateError(
                "factor ids must be unique: %r" % ids,
                code=ERR_MANDATE_VIOLATION,
            )
        return True


# ---------------------------------------------------------------------------
# Positive tests
# ---------------------------------------------------------------------------
class TS007PositiveTests(unittest.TestCase):
    def test_pos_001_all_target_files_exist(self):
        for path in (DOC_07_PATH, MISSION_PATH, UNIVERSE_PATH):
            self.assertTrue(os.path.isfile(path), "missing target file: %s" % path)
        for name in ("momentum.yaml", "reversal.yaml", "liquidity.yaml"):
            factor_path = os.path.join(FACTORS_DIR, name)
            self.assertTrue(
                os.path.isfile(factor_path), "missing factor file: %s" % factor_path
            )

    def test_pos_002_mission_validates(self):
        mission = load_yaml(MISSION_PATH)
        self.assertTrue(InvestmentResearchValidator().validate_mission(mission))
        self.assertIn("mandate", mission)
        self.assertTrue(mission["mandate"], "mandate must be non-empty")
        self.assertEqual(
            mission["claim_ceiling"], CLAIM_CEILING_LOCAL_DELIVERY
        )
        self.assertEqual(mission.get("exact_error"), ERR_MANDATE_VIOLATION)

    def test_pos_003_universe_entries_valid(self):
        universe = load_yaml(UNIVERSE_PATH)
        validator = InvestmentResearchValidator()
        self.assertTrue(validator.validate_universe(universe))
        entries = universe["entries"]
        self.assertTrue(entries, "universe must have entries")
        for entry in entries:
            self.assertIn("tradable", entry)
            self.assertTrue(entry["tradable"] is True)
            self.assertTrue(entry["data_source"])
            self.assertTrue(entry["id"])
            self.assertTrue(entry["symbol"])

    def test_pos_004_factor_ids_unique_with_source_refs(self):
        factors = load_factors(FACTORS_DIR)
        validator = InvestmentResearchValidator()
        self.assertTrue(validator.validate_factors(factors))
        ids = [f["id"] for f in factors]
        self.assertEqual(len(ids), len(set(ids)), "factor ids must be unique")
        self.assertEqual(sorted(ids), sorted(EXPECTED_FACTOR_IDS))
        for factor in factors:
            for field in ("id", "source", "definition", "guard"):
                self.assertIn(field, factor)
                self.assertTrue(
                    factor[field], "factor %r field %r must be non-empty"
                    % (factor.get("id"), field)
                )
            self.assertIn("#", factor["source"], "factor source must be anchored")

    def test_pos_005_doc07_investment_mission_document(self):
        text = read_text(DOC_07_PATH)
        for token in (
            "SQS-THC",
            "WO-TS-REF-07",
            "TS-007",
            "ART-07",
            "mission",
            "universe",
            "momentum",
            "reversal",
            "liquidity",
            "LOCAL_DELIVERY",
            ERR_MANDATE_VIOLATION,
        ):
            self.assertIn(token, text, "DOC-07 missing token %r" % token)


# ---------------------------------------------------------------------------
# Negative tests - a FRESH InvestmentResearchValidator is created per test
# case (setUp), so there is no cross-case contamination.
# ---------------------------------------------------------------------------
class TS007NegativeTests(unittest.TestCase):
    def setUp(self):
        self.validator = InvestmentResearchValidator()

    def test_neg_001_factor_without_source_raises_err_mandate_violation(self):
        factor = load_yaml(os.path.join(FIXTURES_DIR, "factor_no_source.yaml"))
        with self.assertRaises(MandateError) as ctx:
            self.validator.validate_factor(factor)
        self.assertEqual(ctx.exception.code, ERR_MANDATE_VIOLATION)

    def test_neg_002_universe_entry_without_tradable_raises_err_mandate_violation(self):
        universe = load_yaml(
            os.path.join(FIXTURES_DIR, "universe_no_tradable.yaml")
        )
        with self.assertRaises(MandateError) as ctx:
            self.validator.validate_universe(universe)
        self.assertEqual(ctx.exception.code, ERR_MANDATE_VIOLATION)

    def test_neg_003_failed_validation_does_not_mutate_input(self):
        universe = load_yaml(
            os.path.join(FIXTURES_DIR, "universe_no_tradable.yaml")
        )
        before = repr(universe)
        with self.assertRaises(MandateError):
            self.validator.validate_universe(universe)
        # fail-closed: no partial write from the rejected validation
        self.assertEqual(repr(universe), before)

    def test_neg_004_fresh_validator_accepts_clean_artifacts(self):
        # fresh state per case: previous failures must not leak state
        fresh = InvestmentResearchValidator()
        self.assertTrue(fresh.validate_mission(load_yaml(MISSION_PATH)))
        self.assertTrue(fresh.validate_universe(load_yaml(UNIVERSE_PATH)))
        self.assertTrue(fresh.validate_factors(load_factors(FACTORS_DIR)))

    def test_neg_005_claim_overreach_rejected(self):
        mission = load_yaml(MISSION_PATH)
        bad = dict(mission)
        bad["claim_ceiling"] = "PRODUCTION"
        with self.assertRaises(MandateError) as ctx:
            self.validator.validate_mission(bad)
        self.assertEqual(ctx.exception.code, ERR_MANDATE_VIOLATION)


# ---------------------------------------------------------------------------
# Edge tests
# ---------------------------------------------------------------------------
class TS007EdgeTests(unittest.TestCase):
    def test_edge_001_empty_factors_list_allowed(self):
        self.assertTrue(InvestmentResearchValidator().validate_factors([]))

    def test_edge_002_empty_factors_directory_allowed(self):
        empty_dir = os.path.join(FIXTURES_DIR, "factors_empty")
        self.assertTrue(os.path.isdir(empty_dir))
        self.assertEqual(load_factors(empty_dir), [])

    def test_edge_003_missing_required_field_rejected(self):
        mission = load_yaml(
            os.path.join(FIXTURES_DIR, "mission_missing_mandate.yaml")
        )
        with self.assertRaises(MandateError) as ctx:
            InvestmentResearchValidator().validate_mission(mission)
        self.assertIn("mandate", str(ctx.exception))
        # missing field != mandate violation (distinct from ERR_MANDATE_VIOLATION)
        self.assertIsNone(ctx.exception.code)

    def test_edge_004_empty_non_goals_allowed(self):
        mission = load_yaml(MISSION_PATH)
        relaxed = dict(mission)
        relaxed["non_goals"] = []
        self.assertTrue(InvestmentResearchValidator().validate_mission(relaxed))

    def test_edge_005_parser_fail_closed_on_unexpected_construct(self):
        with self.assertRaises(ValueError):
            parse_yaml_subset("- orphan list item at top level\n")


if __name__ == "__main__":
    unittest.main()