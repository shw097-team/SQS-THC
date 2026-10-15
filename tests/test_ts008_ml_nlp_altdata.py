# TS-008 ML/NLP/alternative data research acceptance tests (WO-TS-REF-08).
#
# Pure stdlib unittest - no third-party dependencies. Deterministic and
# fail-closed: any missing file, malformed artifact, or unexpected construct
# raises and fails the suite. No broker write, no network.
#
# Positive: model card validates (id + leakage_guard present), NLP asset
# valid, alt-data source has license.
# Negative: ERR_MODEL_LEAKAGE (training window leaks into test window -
# train_end > test_start, or alt-data without license) - a FRESH validator is
# created per case (setUp), so there is no cross-case contamination.
# Edge: empty model list allowed; missing required field rejected.
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DOC_08_PATH = os.path.join(ROOT, "docs", "DOC-08.md")
ML_DIR = os.path.join(ROOT, "research", "ml")
NLP_DIR = os.path.join(ROOT, "research", "nlp")
ALT_DATA_DIR = os.path.join(ROOT, "research", "alternative-data")
FIXTURES_MODELS_DIR = os.path.join(ROOT, "fixtures", "models")

ERR_MODEL_LEAKAGE = "ERR_MODEL_LEAKAGE"
CLAIM_CEILING_LOCAL_DELIVERY = "LOCAL_DELIVERY"

REQUIRED_MODEL_FIELDS = ("id", "leakage_guard", "metrics", "status")
LEAKAGE_GUARD_FIELDS = (
    "train_start",
    "train_end",
    "test_start",
    "test_end",
    "guard_kind",
)
REQUIRED_NLP_FIELDS = ("id", "source", "purpose")
REQUIRED_ALTDATA_FIELDS = ("id", "license", "source")
EXPECTED_MODEL_IDS = [
    "model-ml-rf-overnight",
    "model-dl-lstm-volume",
    "model-rl-trade-sizing",
]
EXPECTED_NLP_IDS = [
    "nlp-tone-lexicon",
    "nlp-llm-news-summary",
    "nlp-embedding-reports",
]
EXPECTED_ALTDATA_IDS = [
    "alt-satellite-plant-activity",
    "alt-web-pricing-feed",
    "alt-news-sentiment-feed",
]


# ---------------------------------------------------------------------------
# Minimal deterministic YAML-subset parser (stdlib only, fail-closed).
# Supports the exact constructs used by the TS-008 artifacts:
#   - top-level 'key: value' scalars (plain, quoted, null, flow list)
#   - 'key:' followed by a block list of scalars
#   - 'key:' followed by a block list of single-level mappings
#     ('- key: value' plus indented 'key: value' body lines)
#   - 'key:' followed by a nested single-level mapping
#     (indented 'key: value' body lines, e.g. leakage_guard)
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


def load_models(models_dir):
    return load_yaml_dir(models_dir)


# ---------------------------------------------------------------------------
# Fail-closed TS-008 validation semantics used by the negative/edge cases.
# ---------------------------------------------------------------------------
class ModelError(Exception):
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


class MlNlpAltDataValidator(object):
    """Deterministic, fail-closed validator for TS-008 artifacts.

    Semantics:
    - Missing required field  -> rejected with code None (field named in the
      message); a missing field is NOT a leakage violation.
    - Leakage violation       -> ERR_MODEL_LEAKAGE: training window leaks into
      the test window (train_end > test_start), or alternative data without a
      license.
    - Validation never mutates inputs; a failed validation is a no-op.
    """

    def validate_model_card(self, card):
        if not isinstance(card, dict):
            raise ModelError("model card must be a mapping")
        missing = [f for f in REQUIRED_MODEL_FIELDS if f not in card]
        if missing:
            raise ModelError(
                "model card missing required field(s): " + ", ".join(missing)
            )
        for field in ("id", "status"):
            if not _nonempty(card.get(field)):
                raise ModelError("model card field %r must be non-empty" % field)
        guard = card.get("leakage_guard")
        if not isinstance(guard, dict):
            raise ModelError(
                "leakage_guard must be a mapping",
                code=ERR_MODEL_LEAKAGE,
            )
        missing_guard = [f for f in LEAKAGE_GUARD_FIELDS if f not in guard]
        if missing_guard:
            raise ModelError(
                "leakage_guard missing required field(s): "
                + ", ".join(missing_guard)
            )
        for field in LEAKAGE_GUARD_FIELDS:
            if not _nonempty(guard.get(field)):
                raise ModelError(
                    "leakage_guard field %r must be non-empty" % field
                )
        if guard["train_end"] > guard["test_start"]:
            raise ModelError(
                "training window leaks into test window: train_end %r > "
                "test_start %r" % (guard["train_end"], guard["test_start"]),
                code=ERR_MODEL_LEAKAGE,
            )
        metrics = card.get("metrics")
        if not isinstance(metrics, list) or not metrics:
            raise ModelError("metrics must be a non-empty list")
        for metric in metrics:
            if not isinstance(metric, dict) or not _nonempty(
                metric.get("name")
            ) or not _nonempty(metric.get("value")):
                raise ModelError(
                    "each metric must carry non-empty name and value: %r"
                    % (metric,)
                )
        return True

    def validate_models(self, models):
        if not isinstance(models, list):
            raise ModelError("models must be a list")
        for card in models:
            self.validate_model_card(card)
        return True

    def validate_nlp_asset(self, asset):
        if not isinstance(asset, dict):
            raise ModelError("nlp asset must be a mapping")
        missing = [f for f in REQUIRED_NLP_FIELDS if f not in asset]
        if missing:
            raise ModelError(
                "nlp asset missing required field(s): " + ", ".join(missing)
            )
        for field in ("id", "source", "purpose"):
            if not _nonempty(asset.get(field)):
                raise ModelError("nlp asset field %r must be non-empty" % field)
        source = asset.get("source")
        if not isinstance(source, str) or "#" not in source:
            raise ModelError(
                "nlp asset source must be a resolvable anchored locator: %r"
                % (source,)
            )
        return True

    def validate_nlp_assets(self, assets):
        if not isinstance(assets, list):
            raise ModelError("nlp assets must be a list")
        for asset in assets:
            self.validate_nlp_asset(asset)
        return True

    def validate_altdata_source(self, source):
        if not isinstance(source, dict):
            raise ModelError("alt-data source must be a mapping")
        missing = [f for f in REQUIRED_ALTDATA_FIELDS if f not in source]
        if missing:
            if "license" in missing:
                raise ModelError(
                    "alt-data source missing license (unlicensed data is not "
                    "leakage/PIT-safe)",
                    code=ERR_MODEL_LEAKAGE,
                )
            raise ModelError(
                "alt-data source missing required field(s): "
                + ", ".join(missing)
            )
        if not _nonempty(source.get("license")):
            raise ModelError(
                "alt-data license must be non-empty",
                code=ERR_MODEL_LEAKAGE,
            )
        for field in ("id", "source"):
            if not _nonempty(source.get(field)):
                raise ModelError("alt-data field %r must be non-empty" % field)
        src = source.get("source")
        if not isinstance(src, str) or "#" not in src:
            raise ModelError(
                "alt-data source must be a resolvable anchored locator: %r"
                % (src,)
            )
        return True

    def validate_altdata_sources(self, sources):
        if not isinstance(sources, list):
            raise ModelError("alt-data sources must be a list")
        for source in sources:
            self.validate_altdata_source(source)
        return True

    def validate_research(self):
        """Validate the complete TS-008 research artifact set in place."""
        self.validate_models(load_models(ML_DIR))
        self.validate_nlp_assets(load_yaml_dir(NLP_DIR))
        self.validate_altdata_sources(load_yaml_dir(ALT_DATA_DIR))
        return True


# ---------------------------------------------------------------------------
# Positive tests
# ---------------------------------------------------------------------------
class TS008PositiveTests(unittest.TestCase):
    def test_pos_001_all_target_files_exist(self):
        self.assertTrue(os.path.isfile(DOC_08_PATH), "missing docs/DOC-08.md")
        for name in ("model-ml-rf-overnight.yaml", "model-dl-lstm-volume.yaml",
                     "model-rl-trade-sizing.yaml"):
            self.assertTrue(
                os.path.isfile(os.path.join(ML_DIR, name)),
                "missing model card: %s" % name,
            )
        for name in ("nlp-tone-lexicon.yaml", "nlp-llm-news-summary.yaml",
                     "nlp-embedding-reports.yaml"):
            self.assertTrue(
                os.path.isfile(os.path.join(NLP_DIR, name)),
                "missing nlp asset: %s" % name,
            )
        for name in ("alt-satellite-plant-activity.yaml",
                     "alt-web-pricing-feed.yaml",
                     "alt-news-sentiment-feed.yaml"):
            self.assertTrue(
                os.path.isfile(os.path.join(ALT_DATA_DIR, name)),
                "missing alt-data source: %s" % name,
            )
        self.assertTrue(
            os.path.isdir(os.path.join(FIXTURES_MODELS_DIR, "models_empty")),
            "missing empty models fixture directory",
        )

    def test_pos_002_model_cards_validate(self):
        models = load_models(ML_DIR)
        validator = MlNlpAltDataValidator()
        self.assertTrue(validator.validate_models(models))
        ids = [card["id"] for card in models]
        self.assertEqual(sorted(ids), sorted(EXPECTED_MODEL_IDS))
        for card in models:
            for field in ("id", "leakage_guard", "metrics", "status"):
                self.assertIn(field, card, "model card missing %r" % field)
                self.assertTrue(
                    card[field], "model card %r field %r empty"
                    % (card.get("id"), field)
                )
            guard = card["leakage_guard"]
            for field in ("train_start", "train_end", "test_start",
                          "test_end", "guard_kind"):
                self.assertIn(field, guard)
                self.assertTrue(guard[field], "guard %r empty" % field)
            self.assertLessEqual(
                guard["train_end"], guard["test_start"],
                "model %r train window leaks into test window"
                % card["id"],
            )
            self.assertEqual(guard["guard_kind"], "TEMPORAL_SPLIT")
            self.assertEqual(card["status"], "RESEARCH_ONLY")

    def test_pos_003_nlp_assets_valid(self):
        assets = load_yaml_dir(NLP_DIR)
        validator = MlNlpAltDataValidator()
        self.assertTrue(validator.validate_nlp_assets(assets))
        ids = [asset["id"] for asset in assets]
        self.assertEqual(sorted(ids), sorted(EXPECTED_NLP_IDS))
        for asset in assets:
            for field in ("id", "source", "purpose"):
                self.assertIn(field, asset)
                self.assertTrue(asset[field])
            self.assertIn("#", asset["source"], "nlp source must be anchored")

    def test_pos_004_altdata_has_license(self):
        sources = load_yaml_dir(ALT_DATA_DIR)
        validator = MlNlpAltDataValidator()
        self.assertTrue(validator.validate_altdata_sources(sources))
        ids = [source["id"] for source in sources]
        self.assertEqual(sorted(ids), sorted(EXPECTED_ALTDATA_IDS))
        for source in sources:
            for field in ("id", "license", "source"):
                self.assertIn(field, source)
                self.assertTrue(source[field])
            self.assertIn("#", source["source"], "alt-data source anchored")

    def test_pos_005_doc08_research_document(self):
        text = read_text(DOC_08_PATH)
        for token in (
            "SQS-THC",
            "WO-TS-REF-08",
            "TS-008",
            "ART-08",
            "MC-20",
            "CH21",
            "CH22",
            "CH23",
            "model",
            "NLP",
            "alternative data",
            "leakage_guard",
            "license",
            "LOCAL_DELIVERY",
            ERR_MODEL_LEAKAGE,
        ):
            self.assertIn(token, text, "DOC-08 missing token %r" % token)


# ---------------------------------------------------------------------------
# Negative tests - a FRESH MlNlpAltDataValidator is created per test case
# (setUp), so there is no cross-case contamination.
# ---------------------------------------------------------------------------
class TS008NegativeTests(unittest.TestCase):
    def setUp(self):
        self.validator = MlNlpAltDataValidator()

    def test_neg_001_model_leakage_raises_err_model_leakage(self):
        card = load_yaml(
            os.path.join(FIXTURES_MODELS_DIR, "model_leakage.yaml")
        )
        with self.assertRaises(ModelError) as ctx:
            self.validator.validate_model_card(card)
        self.assertEqual(ctx.exception.code, ERR_MODEL_LEAKAGE)
        self.assertIn("train_end", str(ctx.exception))

    def test_neg_002_altdata_without_license_raises_err_model_leakage(self):
        source = load_yaml(
            os.path.join(FIXTURES_MODELS_DIR, "altdata_no_license.yaml")
        )
        with self.assertRaises(ModelError) as ctx:
            self.validator.validate_altdata_source(source)
        self.assertEqual(ctx.exception.code, ERR_MODEL_LEAKAGE)

    def test_neg_003_failed_validation_does_not_mutate_input(self):
        card = load_yaml(
            os.path.join(FIXTURES_MODELS_DIR, "model_leakage.yaml")
        )
        before = repr(card)
        with self.assertRaises(ModelError):
            self.validator.validate_model_card(card)
        # fail-closed: no partial write from the rejected validation
        self.assertEqual(repr(card), before)

    def test_neg_004_fresh_validator_accepts_clean_artifacts(self):
        # fresh state per case: previous failures must not leak state
        fresh = MlNlpAltDataValidator()
        self.assertTrue(fresh.validate_models(load_models(ML_DIR)))
        self.assertTrue(fresh.validate_nlp_assets(load_yaml_dir(NLP_DIR)))
        self.assertTrue(
            fresh.validate_altdata_sources(load_yaml_dir(ALT_DATA_DIR))
        )

    def test_neg_005_window_overlap_rejected_on_clean_card(self):
        # a valid card is rejected the moment its train_end crosses test_start
        card = load_yaml(
            os.path.join(FIXTURES_MODELS_DIR, "model_valid.yaml")
        )
        card["leakage_guard"]["train_end"] = "2023-06-30"  # > test_start
        with self.assertRaises(ModelError) as ctx:
            self.validator.validate_model_card(card)
        self.assertEqual(ctx.exception.code, ERR_MODEL_LEAKAGE)


# ---------------------------------------------------------------------------
# Edge tests
# ---------------------------------------------------------------------------
class TS008EdgeTests(unittest.TestCase):
    def test_edge_001_empty_model_list_allowed(self):
        self.assertTrue(MlNlpAltDataValidator().validate_models([]))

    def test_edge_002_empty_models_directory_allowed(self):
        empty_dir = os.path.join(FIXTURES_MODELS_DIR, "models_empty")
        self.assertTrue(os.path.isdir(empty_dir))
        self.assertEqual(load_models(empty_dir), [])

    def test_edge_003_missing_required_field_rejected(self):
        card = load_yaml(
            os.path.join(FIXTURES_MODELS_DIR, "model_no_leakage_guard.yaml")
        )
        with self.assertRaises(ModelError) as ctx:
            MlNlpAltDataValidator().validate_model_card(card)
        self.assertIn("leakage_guard", str(ctx.exception))
        # missing field != leakage violation (distinct from ERR_MODEL_LEAKAGE)
        self.assertIsNone(ctx.exception.code)

    def test_edge_004_missing_altdata_id_rejected(self):
        source = load_yaml(
            os.path.join(ALT_DATA_DIR, "alt-satellite-plant-activity.yaml")
        )
        del source["id"]
        with self.assertRaises(ModelError) as ctx:
            MlNlpAltDataValidator().validate_altdata_source(source)
        self.assertIn("id", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)

    def test_edge_005_adjacent_windows_allowed(self):
        # train_end == test_start is not a leak (boundary is inclusive-free)
        card = load_yaml(
            os.path.join(FIXTURES_MODELS_DIR, "model_valid.yaml")
        )
        card["leakage_guard"]["test_start"] = card["leakage_guard"]["train_end"]
        self.assertTrue(MlNlpAltDataValidator().validate_model_card(card))

    def test_edge_006_parser_fail_closed_on_unexpected_construct(self):
        with self.assertRaises(ValueError):
            parse_yaml_subset("top:\n  nested:\n    deep: 1\n")


if __name__ == "__main__":
    unittest.main()
