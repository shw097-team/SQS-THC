# TS-001 product constitution acceptance tests (WO-TS-REF-01).
#
# Pure stdlib unittest - no third-party dependencies. Fail-closed: any
# missing file, malformed artifact, or unexpected construct raises and fails
# the suite. Positive: constitution validates, MC IDs unique, owner map
# complete. Negative: duplicate product namespace raises
# ERR_PRODUCT_ID_COLLISION (a FRESH registry is created per case, so there
# is no cross-case contamination). Edge: empty non_goals allowed; missing
# required field rejected.
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DOC_00_PATH = os.path.join(ROOT, "docs", "DOC-00.md")
DOC_01_PATH = os.path.join(ROOT, "docs", "DOC-01.md")
MC_REGISTRY_PATH = os.path.join(ROOT, "requirements", "MC_REGISTRY.yaml")
OWNER_MAP_PATH = os.path.join(ROOT, "architecture", "DOC_CH_OWNER_MAP.yaml")
CONSTITUTION_PATH = os.path.join(ROOT, "contracts", "product", "PRODUCT_CONSTITUTION.yaml")

ERR_PRODUCT_ID_COLLISION = "ERR_PRODUCT_ID_COLLISION"

REQUIRED_CONSTITUTION_FIELDS = (
    "product_id",
    "formal_name",
    "internal_name",
    "namespace",
    "version",
    "supersedes",
    "aliases",
    "non_goals",
)

EXPECTED_STATE_MODEL = [
    "PROPOSED",
    "IDENTITY_UNIQUE",
    "HUMAN_RATIFIED",
    "ACTIVE",
    "SUPERSEDED",
]

EXPECTED_MC_IDS = ["MC-%02d" % i for i in range(1, 28)]  # MC-01..MC-27

EXPECTED_CHAPTERS = ["CH%02d" % i for i in range(36)]  # CH00..CH35


# ---------------------------------------------------------------------------
# Minimal deterministic YAML-subset parser (stdlib only, fail-closed).
# Supports the exact constructs used by the TS-001 artifacts:
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


# ---------------------------------------------------------------------------
# SPEC-01 fail-closed identity registry used by the negative/edge cases.
# ---------------------------------------------------------------------------
class ConstitutionError(Exception):
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code


class ProductRegistry(object):
    """Namespace-keyed product identity registry (SPEC-01 semantics).

    Registering a second product whose namespace is already registered is a
    duplicate-namespace mutation and raises ConstitutionError with code
    ERR_PRODUCT_ID_COLLISION. Required SPEC-01 fields are enforced
    (fail-closed); a failed registration never mutates registry state.
    """

    REQUIRED_FIELDS = REQUIRED_CONSTITUTION_FIELDS
    IDENTITY_SCALAR_FIELDS = (
        "product_id",
        "formal_name",
        "internal_name",
        "namespace",
        "version",
    )

    def __init__(self):
        self._by_namespace = {}
        self._by_product_id = {}

    def register(self, constitution):
        if not isinstance(constitution, dict):
            raise ConstitutionError("constitution must be a mapping")
        missing = [f for f in self.REQUIRED_FIELDS if f not in constitution]
        if missing:
            raise ConstitutionError(
                "missing required field(s): " + ", ".join(missing)
            )
        for field in self.IDENTITY_SCALAR_FIELDS:
            value = constitution.get(field)
            if value is None or (
                isinstance(value, str) and not value.strip()
            ):
                raise ConstitutionError(
                    "required field %r must be non-empty" % field
                )
        namespace = constitution["namespace"]
        product_id = constitution["product_id"]
        if namespace in self._by_namespace:
            raise ConstitutionError(
                "duplicate product namespace: %r" % namespace,
                code=ERR_PRODUCT_ID_COLLISION,
            )
        if product_id in self._by_product_id:
            raise ConstitutionError(
                "duplicate product_id: %r" % product_id,
                code=ERR_PRODUCT_ID_COLLISION,
            )
        self._by_namespace[namespace] = constitution
        self._by_product_id[product_id] = constitution
        return True


def make_constitution(**overrides):
    base = {
        "product_id": "SQS-THC",
        "formal_name": "SQS-THC & TW-ICT FSDT Stack",
        "internal_name": "sqs_thc",
        "namespace": "sqs.ict.twhc",
        "version": "2026.08.10-r1",
        "supersedes": None,
        "aliases": [],
        "non_goals": [],
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------------------------
# Positive tests
# ---------------------------------------------------------------------------
class TS001PositiveTests(unittest.TestCase):
    def test_pos_001_all_target_files_exist(self):
        for path in (
            DOC_00_PATH,
            DOC_01_PATH,
            MC_REGISTRY_PATH,
            OWNER_MAP_PATH,
            CONSTITUTION_PATH,
        ):
            self.assertTrue(os.path.isfile(path), "missing target file: %s" % path)

    def test_pos_002_constitution_yaml_validates(self):
        doc = load_yaml(CONSTITUTION_PATH)
        for field in REQUIRED_CONSTITUTION_FIELDS:
            self.assertIn(field, doc, "missing SPEC-01 required field %r" % field)
        self.assertEqual(doc["product_id"], "SQS-THC")
        self.assertEqual(doc["formal_name"], "SQS-THC & TW-ICT FSDT Stack")
        self.assertEqual(doc["namespace"], "sqs.ict.twhc")
        self.assertEqual(doc["version"], "2026.08.10-r1")
        self.assertEqual(doc["exact_error"], ERR_PRODUCT_ID_COLLISION)
        self.assertEqual(doc["invalid_predicate"], "DUPLICATE_NAMESPACE_FAILS_G00")
        self.assertEqual(doc["state_model"], EXPECTED_STATE_MODEL)
        self.assertEqual(
            list(doc["required_fields"]), list(REQUIRED_CONSTITUTION_FIELDS)
        )
        self.assertEqual(doc["spec_id"], "SPEC-01")

    def test_pos_003_doc00_product_identity_and_invariant(self):
        text = read_text(DOC_00_PATH)
        self.assertIn("product_id", text)
        self.assertIn("SQS-THC", text)
        self.assertIn("SQS-THC & TW-ICT FSDT Stack", text)
        self.assertIn("sqs.ict.twhc", text)
        self.assertIn("2026.08.10-r1", text)
        self.assertIn("formal_name", text)
        self.assertIn("internal_name", text)
        self.assertIn("non_goals", text)
        self.assertIn(ERR_PRODUCT_ID_COLLISION, text)
        for state in EXPECTED_STATE_MODEL:
            self.assertIn(state, text)
        self.assertIn("->", text)  # PROPOSED->IDENTITY_UNIQUE->... notation

    def test_pos_004_doc01_intent_requirement_financial(self):
        text = read_text(DOC_01_PATH)
        self.assertIn("SQS-THC", text)
        self.assertIn("Intent", text)
        self.assertIn("Requirement", text)
        self.assertIn("Financial", text)
        self.assertIn("MC_REGISTRY", text)
        self.assertIn("TS-001", text)
        self.assertIn("ART-01", text)

    def test_pos_005_mc_registry_ids_unique_and_complete(self):
        registry = load_yaml(MC_REGISTRY_PATH)
        entries = registry["entries"]
        ids = [e["id"] for e in entries]
        self.assertEqual(len(ids), len(set(ids)), "MC ids must be unique")
        self.assertEqual(ids, EXPECTED_MC_IDS)
        for entry in entries:
            for field in (
                "id",
                "domain",
                "chapters",
                "specs",
                "ledgers",
                "task_specs",
                "tests",
                "gates",
                "artifacts",
                "status",
            ):
                self.assertIn(field, entry, "%s missing %r" % (entry["id"], field))
                self.assertTrue(
                    entry[field],
                    "%s field %r must be non-empty" % (entry["id"], field),
                )

    def test_pos_006_owner_map_complete(self):
        owner_map = load_yaml(OWNER_MAP_PATH)
        chapters = owner_map["chapters"]
        by_chapter = {c["chapter"]: c for c in chapters}
        self.assertEqual(sorted(by_chapter), EXPECTED_CHAPTERS)
        for chapter in EXPECTED_CHAPTERS:
            entry = by_chapter[chapter]
            self.assertRegex(entry["doc"], r"^DOC-\d{2}$")
            self.assertTrue(entry["owner"].strip(), "owner empty for %s" % chapter)
        # DOC-01 owns CH01..CH03 (product constitution / authority / modular)
        doc01 = sorted(c for c, e in by_chapter.items() if e["doc"] == "DOC-01")
        self.assertEqual(doc01, ["CH01", "CH02", "CH03"])
        # DOC-00 owns exactly CH00
        doc00 = sorted(c for c, e in by_chapter.items() if e["doc"] == "DOC-00")
        self.assertEqual(doc00, ["CH00"])


# ---------------------------------------------------------------------------
# Negative tests - a FRESH ProductRegistry is created per test case
# (setUp), so there is no cross-case contamination.
# ---------------------------------------------------------------------------
class TS001NegativeTests(unittest.TestCase):
    def setUp(self):
        self.registry = ProductRegistry()

    def test_neg_001_duplicate_namespace_raises_err_product_id_collision(self):
        self.registry.register(make_constitution())
        with self.assertRaises(ConstitutionError) as ctx:
            self.registry.register(make_constitution())
        self.assertEqual(ctx.exception.code, ERR_PRODUCT_ID_COLLISION)

    def test_neg_002_duplicate_namespace_different_product_id_still_collides(self):
        self.registry.register(make_constitution())
        with self.assertRaises(ConstitutionError) as ctx:
            self.registry.register(make_constitution(product_id="OTHER-PRODUCT"))
        self.assertEqual(ctx.exception.code, ERR_PRODUCT_ID_COLLISION)

    def test_neg_003_failed_duplicate_does_not_mutate_registry(self):
        self.registry.register(make_constitution())
        with self.assertRaises(ConstitutionError):
            self.registry.register(make_constitution())
        # fail-closed: no partial write from the rejected registration
        self.assertEqual(len(self.registry._by_namespace), 1)
        self.assertEqual(len(self.registry._by_product_id), 1)

    def test_neg_004_fresh_registry_accepts_clean_product(self):
        # fresh registry per case: the previous failure must not leak state
        fresh = ProductRegistry()
        self.assertTrue(fresh.register(make_constitution()))

    def test_neg_005_constitution_yaml_declares_exact_error(self):
        doc = load_yaml(CONSTITUTION_PATH)
        self.assertEqual(doc.get("exact_error"), ERR_PRODUCT_ID_COLLISION)


# ---------------------------------------------------------------------------
# Edge tests
# ---------------------------------------------------------------------------
class TS001EdgeTests(unittest.TestCase):
    def test_edge_001_empty_non_goals_allowed(self):
        registry = ProductRegistry()
        self.assertTrue(registry.register(make_constitution(non_goals=[])))

    def test_edge_002_empty_aliases_allowed(self):
        registry = ProductRegistry()
        self.assertTrue(registry.register(make_constitution(aliases=[])))

    def test_edge_003_missing_required_field_rejected(self):
        registry = ProductRegistry()
        incomplete = make_constitution()
        del incomplete["namespace"]
        with self.assertRaises(ConstitutionError) as ctx:
            registry.register(incomplete)
        self.assertIn("namespace", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)  # missing field != collision

    def test_edge_004_empty_identity_field_rejected(self):
        registry = ProductRegistry()
        with self.assertRaises(ConstitutionError) as ctx:
            registry.register(make_constitution(product_id="   "))
        self.assertIn("product_id", str(ctx.exception))

    def test_edge_005_parser_fail_closed_on_unexpected_construct(self):
        with self.assertRaises(ValueError):
            parse_yaml_subset("- orphan list item at top level\n")


if __name__ == "__main__":
    unittest.main()
