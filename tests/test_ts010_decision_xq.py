# TS-010 Decision/XQ/reconciliation acceptance tests (WO-TS-REF-10).
#
# Pure stdlib unittest - no third-party dependencies. Deterministic and
# fail-closed: any missing file, malformed artifact, or unexpected construct
# raises and fails the suite. No broker write, no network.
#
# Positive: the XQ adapter is READ-ONLY (watch_only:true, write:false, no
# order write operation), the execution-fact schema validates facts against
# its required fields (fact_id, ts, side, qty, price, status), the
# book-of-record reducer descriptor declares single truth / append-only /
# deterministic, and the pure fold reduces facts deterministically.
# Negative: ERR_AUTONOMOUS_ORDER_PATH - any autonomous order write path
# (adapter with write:true, a submit/cancel/modify/replace operation, an
# order_path other than HITL_ONLY, or the book of record accepting an order
# object / direct fact mutation) - a FRESH validator and FRESH BookOfRecord
# are created per case (setUp), so there is no cross-case contamination;
# rejected operations never mutate their state.
# Edge: empty execution facts allowed; missing required field rejected
# (field-naming error, distinct from ERR_AUTONOMOUS_ORDER_PATH); unknown
# fields and non-positive qty rejected; reduce is input-order independent.
import json
import os
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DOC_10_PATH = os.path.join(ROOT, "docs", "DOC-10.md")
XQ_ADAPTER_PATH = os.path.join(ROOT, "adapters", "xq-read-watch.yaml")
EXECUTION_FACT_SCHEMA_PATH = os.path.join(
    ROOT, "schemas", "execution-fact.schema.json"
)
BOOK_OF_RECORD_PATH = os.path.join(ROOT, "reducers", "book-of-record.yaml")

ERR_AUTONOMOUS_ORDER_PATH = "ERR_AUTONOMOUS_ORDER_PATH"
CLAIM_CEILING_LOCAL_DELIVERY = "LOCAL_DELIVERY"

REQUIRED_ADAPTER_FIELDS = (
    "adapter_id",
    "spec_ref",
    "kind",
    "watch_only",
    "write",
    "broker_write",
    "autonomous_order_submission",
    "order_path",
    "mode",
    "operations",
    "forbidden_operations",
)
ALLOWED_OPERATIONS = ("watch", "read", "compile", "radar")
FORBIDDEN_OPERATIONS = ("submit", "cancel", "modify", "replace")

REQUIRED_FACT_FIELDS = ("fact_id", "ts", "side", "qty", "price", "status")
ALLOWED_SIDES = ("BUY", "SELL")
ALLOWED_STATUSES = ("FILLED", "PARTIAL", "REJECTED", "CANCELLED", "UNKNOWN")

REQUIRED_REDUCER_FIELDS = (
    "reducer_id",
    "spec_ref",
    "kind",
    "single_truth",
    "append_only",
    "deterministic",
    "immutable",
    "source_schema",
    "correction_mode",
    "order_path",
    "broker_write",
)


# ---------------------------------------------------------------------------
# Minimal deterministic YAML-subset parser (stdlib only, fail-closed).
# Supports the exact constructs used by the TS-010 artifacts:
#   - top-level 'key: value' scalars (plain, quoted, null, flow list)
#   - 'key:' followed by a block list of scalars
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
                raise ValueError(
                    "nested mapping not used by TS-010 artifacts: %r" % nxt
                )
        else:
            data[key] = _scalar(rest)
            i += 1
    return data


def read_text(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def load_yaml(path):
    return parse_yaml_subset(read_text(path))


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def load_xq_adapter():
    return load_yaml(XQ_ADAPTER_PATH)


def load_execution_fact_schema():
    return load_json(EXECUTION_FACT_SCHEMA_PATH)


def load_book_of_record():
    return load_yaml(BOOK_OF_RECORD_PATH)


def sample_facts():
    """Deterministic sample fact set (schema-valid)."""
    return [
        {"fact_id": "F-1001", "ts": "2026-08-10T09:30:01+08:00",
         "side": "BUY", "qty": 1000, "price": 150.5, "status": "FILLED"},
        {"fact_id": "F-1002", "ts": "2026-08-10T09:30:02+08:00",
         "side": "SELL", "qty": 400, "price": 151.0, "status": "PARTIAL"},
        {"fact_id": "F-1003", "ts": "2026-08-10T09:30:03+08:00",
         "side": "SELL", "qty": 600, "price": 152.0, "status": "REJECTED"},
    ]


# ---------------------------------------------------------------------------
# Fail-closed TS-010 decision/XQ/reconciliation semantics used by the
# negative/edge cases.
# ---------------------------------------------------------------------------
class DecisionXQError(Exception):
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


def _is_number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool)


class XQAdapterValidator(object):
    """Deterministic, fail-closed validator for adapters/xq-read-watch.yaml.

    The XQ surface is a READ-ONLY watch adapter. Any autonomous order write
    path - write:true, watch_only demoted, broker_write:true,
    autonomous_order_submission:true, order_path other than HITL_ONLY, a
    forbidden operation (submit/cancel/modify/replace) present in
    operations, or a forbidden operation missing from forbidden_operations -
    is rejected with code ERR_AUTONOMOUS_ORDER_PATH. Missing required fields
    are rejected with code None (field-naming error). Validation never
    mutates inputs.
    """

    def validate_adapter(self, data):
        if not isinstance(data, dict):
            raise DecisionXQError("adapter must be a mapping")
        missing = [f for f in REQUIRED_ADAPTER_FIELDS if f not in data]
        if missing:
            raise DecisionXQError(
                "adapter missing required field(s): " + ", ".join(missing)
            )
        for field in ("adapter_id", "spec_ref", "kind", "order_path", "mode"):
            if not _nonempty(data.get(field)):
                raise DecisionXQError("adapter field %r must be non-empty" % field)
        if data.get("watch_only") is not True:
            raise DecisionXQError(
                "adapter %r must be watch_only:true (read-only watch adapter)"
                % (data.get("adapter_id"),),
                code=ERR_AUTONOMOUS_ORDER_PATH,
            )
        if data.get("write") is not False:
            raise DecisionXQError(
                "adapter %r must be write:false (no write path)"
                % (data.get("adapter_id"),),
                code=ERR_AUTONOMOUS_ORDER_PATH,
            )
        if data.get("broker_write") is not False:
            raise DecisionXQError(
                "adapter %r must be broker_write:false (no broker write)"
                % (data.get("adapter_id"),),
                code=ERR_AUTONOMOUS_ORDER_PATH,
            )
        if data.get("autonomous_order_submission") is not False:
            raise DecisionXQError(
                "adapter %r must have autonomous_order_submission:false"
                % (data.get("adapter_id"),),
                code=ERR_AUTONOMOUS_ORDER_PATH,
            )
        if data.get("order_path") != "HITL_ONLY":
            raise DecisionXQError(
                "adapter %r order_path must be HITL_ONLY (no autonomous "
                "order path)" % (data.get("adapter_id"),),
                code=ERR_AUTONOMOUS_ORDER_PATH,
            )
        operations = data.get("operations")
        if not isinstance(operations, list) or not operations:
            raise DecisionXQError("adapter operations must be a non-empty list")
        for op in operations:
            if op in FORBIDDEN_OPERATIONS:
                raise DecisionXQError(
                    "adapter %r carries forbidden order-write operation %r"
                    % (data.get("adapter_id"), op),
                    code=ERR_AUTONOMOUS_ORDER_PATH,
                )
            if op not in ALLOWED_OPERATIONS:
                raise DecisionXQError(
                    "adapter operation %r is not in allowlist %r"
                    % (op, ALLOWED_OPERATIONS)
                )
        forbidden = data.get("forbidden_operations")
        if not isinstance(forbidden, list):
            raise DecisionXQError("adapter forbidden_operations must be a list")
        for op in FORBIDDEN_OPERATIONS:
            if op not in forbidden:
                raise DecisionXQError(
                    "adapter %r does not forbid order-write operation %r "
                    "(write path not closed)" % (data.get("adapter_id"), op),
                    code=ERR_AUTONOMOUS_ORDER_PATH,
                )
        overlap = [op for op in operations if op in forbidden]
        if overlap:
            raise DecisionXQError(
                "adapter operation %r both allowed and forbidden" % (overlap[0],),
                code=ERR_AUTONOMOUS_ORDER_PATH,
            )
        return True


class ExecutionFactValidator(object):
    """Schema-driven, fail-closed validator for execution facts.

    The schema (schemas/execution-fact.schema.json) is the source of truth:
    required fields, per-field type/enum/min constraints and
    additionalProperties:false are enforced from the schema itself. A fact
    missing a required field, carrying an unknown field, or violating a
    constraint is rejected with code None (field-naming error). The schema
    itself must be well-formed (draft-07, object type, six required fields,
    additionalProperties:false, TS-010 meta anchor).
    """

    REQUIRED_PROPERTIES = ("fact_id", "ts", "side", "qty", "price", "status")

    def validate_schema(self, schema):
        if not isinstance(schema, dict):
            raise DecisionXQError("schema must be a mapping")
        if not isinstance(schema.get("$schema"), str) or "draft-07" not in schema.get(
            "$schema"
        ):
            raise DecisionXQError("schema $schema must anchor to draft-07")
        if schema.get("type") != "object":
            raise DecisionXQError("schema type must be object")
        properties = schema.get("properties")
        if not isinstance(properties, dict):
            raise DecisionXQError("schema properties must be a mapping")
        missing_props = [f for f in self.REQUIRED_PROPERTIES if f not in properties]
        if missing_props:
            raise DecisionXQError(
                "schema properties missing required field(s): "
                + ", ".join(missing_props)
            )
        required = schema.get("required")
        if not isinstance(required, list):
            raise DecisionXQError("schema required must be a list")
        missing_required = [f for f in self.REQUIRED_PROPERTIES if f not in required]
        if missing_required:
            raise DecisionXQError(
                "schema required missing field(s): " + ", ".join(missing_required)
            )
        if schema.get("additionalProperties") is not False:
            raise DecisionXQError(
                "schema additionalProperties must be false (fail-closed)"
            )
        meta = schema.get("meta")
        if not isinstance(meta, dict) or "TS-010" not in str(meta.get("spec_ref", "")):
            raise DecisionXQError("schema meta must anchor to TS-010")
        return True

    def validate_fact(self, schema, fact):
        self.validate_schema(schema)
        if not isinstance(fact, dict):
            raise DecisionXQError("execution fact must be a mapping")
        required = list(schema["required"])
        missing = [f for f in required if f not in fact]
        if missing:
            raise DecisionXQError(
                "execution fact missing required field(s): " + ", ".join(missing)
            )
        allowed_keys = set(schema["properties"].keys())
        extra = [k for k in fact if k not in allowed_keys]
        if extra:
            raise DecisionXQError(
                "execution fact has unknown field(s): " + ", ".join(extra)
            )
        props = schema["properties"]
        for field in required:
            value = fact[field]
            spec = props[field]
            if spec.get("type") == "string":
                if not isinstance(value, str) or not value.strip():
                    raise DecisionXQError(
                        "execution fact field %r must be a non-empty string" % field
                    )
            elif spec.get("type") == "number":
                if not _is_number(value):
                    raise DecisionXQError(
                        "execution fact field %r must be a number" % field
                    )
                if "exclusiveMinimum" in spec and value <= spec["exclusiveMinimum"]:
                    raise DecisionXQError(
                        "execution fact field %r must be > %r"
                        % (field, spec["exclusiveMinimum"])
                    )
            if "enum" in spec and value not in spec["enum"]:
                raise DecisionXQError(
                    "execution fact field %r value %r not in enum %r"
                    % (field, value, spec["enum"])
                )
        return True


def reduce_book_of_record(facts):
    """Pure, deterministic fold over execution facts (CH29 / MC-25).

    Facts are ordered by (ts, fact_id); only FILLED/PARTIAL facts move the
    position and notional (REJECTED/CANCELLED/UNKNOWN are recorded but do not
    trade). The input list is never mutated; the same facts always produce
    the same projection regardless of input order.
    """
    ordered = sorted(facts, key=lambda f: (f["ts"], f["fact_id"]))
    position = 0
    notional = 0.0
    for fact in ordered:
        if fact["status"] in ("FILLED", "PARTIAL"):
            signed = fact["qty"] if fact["side"] == "BUY" else -fact["qty"]
            position += signed
            notional += fact["qty"] * fact["price"]
    return {
        "fact_count": len(ordered),
        "position": position,
        "notional_executed": notional,
        "last_ts": ordered[-1]["ts"] if ordered else None,
    }


class BookOfRecord(object):
    """Append-only single-truth ledger over execution facts (CH29 / MC-25).

    Only schema-valid execution facts may be appended; there is no update,
    no delete and no order path. Any direct order mutation (an order object,
    or an update/delete of an existing fact) raises
    ERR_AUTONOMOUS_ORDER_PATH and performs no mutation. A fresh instance is
    created per test case so failed operations never leak state.
    """

    def __init__(self, schema):
        self.schema = schema
        ExecutionFactValidator().validate_schema(schema)
        self._facts = []

    @property
    def facts(self):
        return tuple(self._facts)

    def append(self, fact):
        ExecutionFactValidator().validate_fact(self.schema, fact)
        self._facts.append(fact)
        return self

    def reduce(self):
        return reduce_book_of_record(self.facts)

    def mutate(self, fact_id, changes):
        raise DecisionXQError(
            "direct mutation of fact %r is an order-path write (append-only "
            "book of record)" % (fact_id,),
            code=ERR_AUTONOMOUS_ORDER_PATH,
        )

    def delete(self, fact_id):
        raise DecisionXQError(
            "direct deletion of fact %r is an order-path write (append-only "
            "book of record)" % (fact_id,),
            code=ERR_AUTONOMOUS_ORDER_PATH,
        )

    def accept_order(self, order):
        raise DecisionXQError(
            "an order object is not an execution fact; autonomous order "
            "write path rejected",
            code=ERR_AUTONOMOUS_ORDER_PATH,
        )


# ---------------------------------------------------------------------------
# Positive tests
# ---------------------------------------------------------------------------
class TS010PositiveTests(unittest.TestCase):
    def test_pos_001_all_target_files_exist(self):
        self.assertTrue(os.path.isfile(DOC_10_PATH), "missing docs/DOC-10.md")
        self.assertTrue(
            os.path.isfile(XQ_ADAPTER_PATH), "missing adapters/xq-read-watch.yaml"
        )
        self.assertTrue(
            os.path.isfile(EXECUTION_FACT_SCHEMA_PATH),
            "missing schemas/execution-fact.schema.json",
        )
        self.assertTrue(
            os.path.isfile(BOOK_OF_RECORD_PATH),
            "missing reducers/book-of-record.yaml",
        )

    def test_pos_002_xq_adapter_is_read_only(self):
        data = load_xq_adapter()
        validator = XQAdapterValidator()
        self.assertTrue(validator.validate_adapter(data))
        for field in REQUIRED_ADAPTER_FIELDS:
            self.assertIn(field, data, "adapter missing %r" % field)
            self.assertTrue(
                _nonempty(data[field]), "adapter field %r empty" % field
            )
        self.assertIs(data["watch_only"], True, "adapter must be watch_only:true")
        self.assertIs(data["write"], False, "adapter must be write:false")
        self.assertIs(data["broker_write"], False, "no broker write")
        self.assertIs(data["autonomous_order_submission"], False)
        self.assertEqual(data["order_path"], "HITL_ONLY")
        self.assertEqual(data["mode"], "RADAR_ONLY")
        self.assertEqual(sorted(data["operations"]), sorted(ALLOWED_OPERATIONS))
        for op in FORBIDDEN_OPERATIONS:
            self.assertIn(op, data["forbidden_operations"])
            self.assertNotIn(op, data["operations"])

    def test_pos_003_execution_fact_schema_validates_facts(self):
        schema = load_execution_fact_schema()
        validator = ExecutionFactValidator()
        self.assertTrue(validator.validate_schema(schema))
        self.assertEqual(sorted(schema["required"]), sorted(REQUIRED_FACT_FIELDS))
        self.assertIs(schema["additionalProperties"], False)
        self.assertIn("TS-010", schema["meta"]["spec_ref"])
        for fact in sample_facts():
            self.assertTrue(validator.validate_fact(schema, fact))

    def test_pos_004_book_of_record_reducer_descriptor(self):
        reducer = load_book_of_record()
        for field in REQUIRED_REDUCER_FIELDS:
            self.assertIn(field, reducer, "reducer missing %r" % field)
            self.assertTrue(
                _nonempty(reducer[field]), "reducer field %r empty" % field
            )
        self.assertEqual(reducer["reducer_id"], "book-of-record")
        self.assertEqual(reducer["kind"], "pure_reducer")
        self.assertIs(reducer["single_truth"], True)
        self.assertIs(reducer["append_only"], True)
        self.assertIs(reducer["deterministic"], True)
        self.assertIs(reducer["immutable"], True)
        self.assertEqual(reducer["correction_mode"], "NEW_EVENT")
        self.assertEqual(reducer["order_path"], "HITL_ONLY")
        self.assertIs(reducer["broker_write"], False)
        self.assertEqual(
            reducer["source_schema"], "schemas/execution-fact.schema.json"
        )

    def test_pos_005_book_of_record_reduces_deterministically(self):
        facts = sample_facts()
        first = reduce_book_of_record(facts)
        second = reduce_book_of_record(facts)
        self.assertEqual(first, second)
        self.assertEqual(first["fact_count"], 3)
        self.assertEqual(first["position"], 600)
        self.assertEqual(first["notional_executed"], 210900.0)
        self.assertEqual(first["last_ts"], "2026-08-10T09:30:03+08:00")

    def test_pos_006_book_of_record_append_only(self):
        schema = load_execution_fact_schema()
        book = BookOfRecord(schema)
        facts = sample_facts()
        before = repr(facts)
        book.append(facts[0])
        self.assertEqual(len(book.facts), 1)
        self.assertEqual(book.facts[0]["fact_id"], "F-1001")
        # reduce never mutates its input
        self.assertEqual(repr(facts), before)

    def test_pos_007_doc10_decision_xq_document(self):
        text = read_text(DOC_10_PATH)
        for token in (
            "SQS-THC",
            "WO-TS-REF-10",
            "TS-010",
            "ART-10",
            "MC-24",
            "MC-25",
            "CH27",
            "CH28",
            "CH29",
            "adapters/xq-read-watch.yaml",
            "schemas/execution-fact.schema.json",
            "reducers/book-of-record.yaml",
            "ERR_AUTONOMOUS_ORDER_PATH",
            "HITL_ONLY",
            "RADAR_ONLY",
            "watch_only",
            "append-only",
            "fact_id",
            "status",
            CLAIM_CEILING_LOCAL_DELIVERY,
        ):
            self.assertIn(token, text, "DOC-10 missing token %r" % token)


# ---------------------------------------------------------------------------
# Negative tests - a FRESH validator and a FRESH BookOfRecord are created
# per test case (setUp), so there is no cross-case contamination.
# ---------------------------------------------------------------------------
class TS010NegativeTests(unittest.TestCase):
    def setUp(self):
        self.schema = load_execution_fact_schema()
        self.adapter = load_xq_adapter()
        self.validator = ExecutionFactValidator()
        self.book = BookOfRecord(self.schema)

    def test_neg_001_adapter_write_true_raises_err_autonomous_order_path(self):
        self.adapter["write"] = True  # enable a write path
        with self.assertRaises(DecisionXQError) as ctx:
            XQAdapterValidator().validate_adapter(self.adapter)
        self.assertEqual(ctx.exception.code, ERR_AUTONOMOUS_ORDER_PATH)

    def test_neg_002_adapter_submit_operation_raises_err_autonomous_order_path(self):
        self.adapter["operations"].append("submit")  # order write operation
        with self.assertRaises(DecisionXQError) as ctx:
            XQAdapterValidator().validate_adapter(self.adapter)
        self.assertEqual(ctx.exception.code, ERR_AUTONOMOUS_ORDER_PATH)
        self.assertIn("submit", str(ctx.exception))

    def test_neg_003_adapter_order_path_not_hitl_raises_err_autonomous_order_path(self):
        self.adapter["order_path"] = "AUTONOMOUS"
        with self.assertRaises(DecisionXQError) as ctx:
            XQAdapterValidator().validate_adapter(self.adapter)
        self.assertEqual(ctx.exception.code, ERR_AUTONOMOUS_ORDER_PATH)

    def test_neg_004_adapter_missing_forbidden_op_raises_err_autonomous_order_path(self):
        self.adapter["forbidden_operations"].remove("cancel")
        with self.assertRaises(DecisionXQError) as ctx:
            XQAdapterValidator().validate_adapter(self.adapter)
        self.assertEqual(ctx.exception.code, ERR_AUTONOMOUS_ORDER_PATH)

    def test_neg_005_book_rejects_order_object_raises_err_autonomous_order_path(self):
        order = {"order_id": "O-1", "action": "submit", "qty": 100}
        with self.assertRaises(DecisionXQError) as ctx:
            self.book.accept_order(order)
        self.assertEqual(ctx.exception.code, ERR_AUTONOMOUS_ORDER_PATH)
        self.assertEqual(self.book.facts, ())

    def test_neg_006_book_rejects_direct_mutation_raises_err_autonomous_order_path(self):
        self.book.append(sample_facts()[0])
        with self.assertRaises(DecisionXQError) as ctx:
            self.book.mutate("F-1001", {"qty": 9999})
        self.assertEqual(ctx.exception.code, ERR_AUTONOMOUS_ORDER_PATH)
        with self.assertRaises(DecisionXQError) as ctx:
            self.book.delete("F-1001")
        self.assertEqual(ctx.exception.code, ERR_AUTONOMOUS_ORDER_PATH)
        # append-only: the fact is unchanged
        self.assertEqual(self.book.facts[0]["qty"], 1000)

    def test_neg_007_failed_append_does_not_mutate_state(self):
        invalid = dict(sample_facts()[0])
        del invalid["fact_id"]
        before = self.book.facts
        with self.assertRaises(DecisionXQError):
            self.book.append(invalid)
        # fail-closed: no partial write
        self.assertEqual(self.book.facts, before)

    def test_neg_008_fresh_state_accepts_clean_artifacts(self):
        # fresh per case: previous failures must not leak state
        fresh = BookOfRecord(load_execution_fact_schema())
        self.assertTrue(XQAdapterValidator().validate_adapter(load_xq_adapter()))
        for fact in sample_facts():
            fresh.append(fact)
        self.assertEqual(fresh.reduce()["position"], 600)
        self.assertTrue(
            ExecutionFactValidator().validate_schema(load_execution_fact_schema())
        )


# ---------------------------------------------------------------------------
# Edge tests
# ---------------------------------------------------------------------------
class TS010EdgeTests(unittest.TestCase):
    def test_edge_001_empty_execution_facts_allowed(self):
        schema = load_execution_fact_schema()
        # schema validation over an empty fact set is vacuously valid
        projection = reduce_book_of_record([])
        self.assertEqual(projection["fact_count"], 0)
        self.assertEqual(projection["position"], 0)
        self.assertEqual(projection["notional_executed"], 0.0)
        self.assertIsNone(projection["last_ts"])
        self.assertEqual(BookOfRecord(schema).reduce(), projection)

    def test_edge_002_missing_required_field_rejected(self):
        fact = dict(sample_facts()[0])
        del fact["fact_id"]
        with self.assertRaises(DecisionXQError) as ctx:
            ExecutionFactValidator().validate_fact(
                load_execution_fact_schema(), fact
            )
        self.assertIn("fact_id", str(ctx.exception))
        # missing field != autonomous order path (distinct error)
        self.assertIsNone(ctx.exception.code)

    def test_edge_003_schema_missing_required_field_rejected(self):
        schema = load_execution_fact_schema()
        schema["required"] = [f for f in schema["required"] if f != "status"]
        with self.assertRaises(DecisionXQError) as ctx:
            ExecutionFactValidator().validate_schema(schema)
        self.assertIn("status", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)

    def test_edge_004_nonpositive_qty_rejected(self):
        fact = dict(sample_facts()[0])
        fact["qty"] = 0  # exclusiveMinimum: 0 -> must be strictly positive
        with self.assertRaises(DecisionXQError) as ctx:
            ExecutionFactValidator().validate_fact(
                load_execution_fact_schema(), fact
            )
        self.assertIn("qty", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)

    def test_edge_005_unknown_field_rejected(self):
        fact = dict(sample_facts()[0])
        fact["order_id"] = "O-1"  # additionalProperties: false
        with self.assertRaises(DecisionXQError) as ctx:
            ExecutionFactValidator().validate_fact(
                load_execution_fact_schema(), fact
            )
        self.assertIn("order_id", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)

    def test_edge_006_reduce_is_input_order_independent(self):
        facts = sample_facts()
        shuffled = [facts[2], facts[0], facts[1]]
        self.assertEqual(reduce_book_of_record(shuffled), reduce_book_of_record(facts))


if __name__ == "__main__":
    unittest.main()
