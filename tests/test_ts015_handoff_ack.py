# TS-015 Closed-book handoff and consumer ACK acceptance tests (WO-TS-REF-15).
#
# Pure stdlib unittest - no third-party dependencies. Deterministic and
# fail-closed: any missing file, malformed artifact, or unexpected construct
# raises and fails the suite. No broker write, no network; validation never
# mutates the canonical handoff artifacts.
#
# Positive: the GPT B command pack is complete (each entry: task_id,
# commands, allowlist), the OROCHI execution packet is valid (each entry:
# task_id, context, contract), and the consumer ACK ledger is append-only.
# Negative: ERR_RECEIVER_CONTEXT_MISSING - an ACK entry without receiver
# context (missing or blank receiver) is rejected; a FRESH ledger is created
# per case (setUp), so there is no cross-case contamination.
# Edge: an empty ACK ledger is a valid deterministic state; a missing
# required field is rejected with a field-naming error (code None), distinct
# from ERR_RECEIVER_CONTEXT_MISSING.
import json
import os
import unittest
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

COMMAND_PACK_PATH = os.path.join(ROOT, "handoff", "gpt-b-command-pack.yaml")
EXECUTION_PACKET_PATH = os.path.join(
    ROOT, "handoff", "orochi-execution-packet.yaml"
)
ACK_LEDGER_PATH = os.path.join(ROOT, "handoff", "consumer-ack.ndjson")

ERR_RECEIVER_CONTEXT_MISSING = "ERR_RECEIVER_CONTEXT_MISSING"

EXPECTED_TARGETS_REL = (
    "handoff/gpt-b-command-pack.yaml",
    "handoff/orochi-execution-packet.yaml",
    "handoff/consumer-ack.ndjson",
)

REQUIRED_ACK_FIELDS = ("task_id", "receiver", "decision", "timestamp")
ALLOWED_DECISIONS = ("ACK", "NACK")

REQUIRED_PACK_ENTRY_FIELDS = ("task_id", "commands", "allowlist")
REQUIRED_PACKET_ENTRY_FIELDS = ("task_id", "context", "contract")
REQUIRED_CONTEXT_FIELDS = (
    "work_order",
    "receiver",
    "workspace_policy",
    "path_status",
    "runtime_status",
    "closed_book",
)
REQUIRED_CONTRACT_FIELDS = (
    "target_files_exact_set",
    "required_pack_fields",
    "required_packet_fields",
    "required_ack_fields",
    "error_receiver_context_missing",
    "fail_closed",
    "no_broker_write",
    "no_network",
    "rollback",
)


# ---------------------------------------------------------------------------
# Minimal deterministic YAML-subset parser (stdlib only, fail-closed).
# Supports the exact constructs used by the TS-015 artifacts:
#   - top-level 'key: value' scalars (plain, quoted, null, flow list)
#   - 'key:' followed by a block list of mapping items
#   - block-list mapping items '- key: value' with a body of 'key2: value2'
#     pairs, nested block lists, and nested mappings
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


def _parse_block(lines, i, indent):
    line = lines[i]
    if line.strip().startswith("- "):
        return _parse_list(lines, i, indent)
    return _parse_mapping(lines, i, indent)


def _parse_list(lines, i, indent):
    items = []
    n = len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if _indent(line) != indent or not line.strip().startswith("- "):
            break
        rest = line.strip()[2:].strip()
        if not rest:
            raise ValueError("empty list item: %r" % line)
        if ":" in rest and not rest.startswith(("[", "{", "'", '"')):
            key, _, value = rest.partition(":")
            key = key.strip()
            value = value.strip()
            item = {}
            i += 1
            if value:
                item[key] = _scalar(value)
            else:
                j = i
                while j < n and not lines[j].strip():
                    j += 1
                if j < n and _indent(lines[j]) > indent:
                    sub, i = _parse_block(lines, j, _indent(lines[j]))
                    item[key] = sub
                else:
                    item[key] = None
            if i < n and lines[i].strip() and _indent(lines[i]) > indent:
                body, i = _parse_block(lines, i, _indent(lines[i]))
                if not isinstance(body, dict):
                    raise ValueError("unexpected list body: %r" % lines[i])
                item.update(body)
            items.append(item)
        else:
            items.append(_scalar(rest))
            i += 1
    return items, i


def _parse_mapping(lines, i, indent):
    data = {}
    n = len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if _indent(line) != indent or line.strip().startswith("- "):
            break
        key, rest = _split_key(line.strip())
        key = key.strip()
        rest = rest.strip()
        i += 1
        if rest:
            data[key] = _scalar(rest)
        else:
            j = i
            while j < n and not lines[j].strip():
                j += 1
            if j < n and _indent(lines[j]) > indent:
                data[key], i = _parse_block(lines, j, _indent(lines[j]))
            else:
                data[key] = None
    return data, i


def parse_yaml_subset(text):
    lines = [
        l
        for l in (_strip_comment(line).rstrip() for line in text.splitlines())
        if l.strip()
    ]
    if not lines:
        return {}
    data, i = _parse_mapping(lines, 0, 0)
    if i != len(lines):
        raise ValueError("trailing content at line %d: %r" % (i, lines[i]))
    return data


def read_text(path):
    with open(path, "r", encoding="utf-8-sig") as fh:
        return fh.read()


def load_yaml(path):
    return parse_yaml_subset(read_text(path))


def load_command_entries():
    return load_yaml(COMMAND_PACK_PATH)["entries"]


def load_execution_entries():
    return load_yaml(EXECUTION_PACKET_PATH)["entries"]


def parse_ack_entries(text):
    """Parse an NDJSON ACK ledger body; every line must be a JSON object."""
    entries = []
    for lineno, line in enumerate(text.splitlines(), 1):
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except ValueError:
            raise TS015Error("malformed ACK line %d" % lineno)
        if not isinstance(entry, dict):
            raise TS015Error("ACK line %d must be a JSON object" % lineno)
        entries.append(entry)
    return entries


# ---------------------------------------------------------------------------
# Fail-closed TS-015 closed-book handoff semantics.
# ---------------------------------------------------------------------------
class TS015Error(Exception):
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
        raise TS015Error("%s must be a mapping" % label)
    missing = [f for f in fields if f not in record]
    if missing:
        raise TS015Error(
            "%s missing required field(s): %s" % (label, ", ".join(missing))
        )


class CommandPack(object):
    """Fail-closed GPT B command pack (TS-015 / ART-15).

    Each entry carries task_id, a non-empty ordered list of command-contract
    strings and a non-empty allowlist of relative repo paths the external
    executor may write. Commands are contracts only - validation performs no
    execution, no broker write and no network access.
    """

    REQUIRED_FIELDS = REQUIRED_PACK_ENTRY_FIELDS

    def __init__(self, entries):
        if not isinstance(entries, list):
            raise TS015Error("command pack entries must be a list")
        seen = set()
        frozen = []
        for entry in entries:
            _require_fields(entry, self.REQUIRED_FIELDS, "command pack entry")
            for field in self.REQUIRED_FIELDS:
                if not _nonempty(entry.get(field)):
                    raise TS015Error(
                        "command pack entry field %r must be non-empty" % field
                    )
            if entry["task_id"] in seen:
                raise TS015Error(
                    "duplicate command pack task_id %r" % entry["task_id"]
                )
            seen.add(entry["task_id"])
            commands = entry["commands"]
            if not isinstance(commands, list) or not commands:
                raise TS015Error(
                    "command pack %r commands must be a non-empty list"
                    % entry["task_id"]
                )
            for command in commands:
                if not isinstance(command, str) or not command.strip():
                    raise TS015Error(
                        "command pack %r command must be a non-empty string"
                        % entry["task_id"]
                    )
            allowlist = entry["allowlist"]
            if not isinstance(allowlist, list) or not allowlist:
                raise TS015Error(
                    "command pack %r allowlist must be a non-empty list"
                    % entry["task_id"]
                )
            frozen_allow = []
            for path in allowlist:
                if not isinstance(path, str) or not path.strip():
                    raise TS015Error(
                        "command pack %r allowlist path must be a "
                        "non-empty string" % entry["task_id"]
                    )
                if path.startswith(("/", "\\")) or ".." in path.split("/"):
                    raise TS015Error(
                        "command pack %r allowlist path must be relative: %r"
                        % (entry["task_id"], path)
                    )
                frozen_allow.append(path)
            frozen.append(
                {
                    "task_id": entry["task_id"],
                    "commands": tuple(c.strip() for c in commands),
                    "allowlist": tuple(frozen_allow),
                }
            )
        self._entries = tuple(frozen)

    @property
    def entries(self):
        return tuple(dict(e) for e in self._entries)

    @property
    def task_ids(self):
        return tuple(e["task_id"] for e in self._entries)


class ExecutionPacket(object):
    """Fail-closed OROCHI execution packet (TS-015 / ART-15).

    Each entry carries task_id, a context mapping (work order, receiver,
    workspace policy, path/runtime status, closed-book rule) and a contract
    mapping (exact target set, required fields, fail-closed error, no broker
    write / no network, rollback). Instances are immutable tuples.
    """

    REQUIRED_FIELDS = REQUIRED_PACKET_ENTRY_FIELDS
    REQUIRED_CONTEXT_FIELDS = REQUIRED_CONTEXT_FIELDS
    REQUIRED_CONTRACT_FIELDS = REQUIRED_CONTRACT_FIELDS

    def __init__(self, entries):
        if not isinstance(entries, list):
            raise TS015Error("execution packet entries must be a list")
        seen = set()
        frozen = []
        for entry in entries:
            _require_fields(entry, self.REQUIRED_FIELDS, "execution packet entry")
            for field in self.REQUIRED_FIELDS:
                if not _nonempty(entry.get(field)):
                    raise TS015Error(
                        "execution packet entry field %r must be non-empty"
                        % field
                    )
            if entry["task_id"] in seen:
                raise TS015Error(
                    "duplicate execution packet task_id %r" % entry["task_id"]
                )
            seen.add(entry["task_id"])
            context = entry["context"]
            _require_fields(context, self.REQUIRED_CONTEXT_FIELDS, "execution context")
            for field in self.REQUIRED_CONTEXT_FIELDS:
                if not _nonempty(context.get(field)):
                    raise TS015Error(
                        "execution context field %r must be non-empty" % field
                    )
            contract = entry["contract"]
            _require_fields(contract, self.REQUIRED_CONTRACT_FIELDS, "execution contract")
            for field in self.REQUIRED_CONTRACT_FIELDS:
                if not _nonempty(contract.get(field)):
                    raise TS015Error(
                        "execution contract field %r must be non-empty" % field
                    )
            frozen.append(
                {
                    "task_id": entry["task_id"],
                    "context": dict(context),
                    "contract": dict(contract),
                }
            )
        self._entries = tuple(frozen)

    @property
    def entries(self):
        return tuple(dict(e) for e in self._entries)

    @property
    def task_ids(self):
        return tuple(e["task_id"] for e in self._entries)


class AckLedger(object):
    """Append-only consumer ACK ledger (TS-015 / ART-15).

    Every entry requires task_id, receiver, decision and timestamp. An ACK
    entry without receiver context - a missing or blank receiver - is
    rejected with ERR_RECEIVER_CONTEXT_MISSING. Appending returns a NEW
    ledger; the source ledger is never mutated (append-only). An empty
    ledger is a valid deterministic state (consumer ACK NOT_RUN).
    """

    REQUIRED_FIELDS = REQUIRED_ACK_FIELDS
    ALLOWED_DECISIONS = ALLOWED_DECISIONS

    def __init__(self, entries):
        if not isinstance(entries, list):
            raise TS015Error("ACK ledger entries must be a list")
        frozen = []
        for entry in entries:
            if not isinstance(entry, dict):
                raise TS015Error("ACK entry must be a mapping")
            if "receiver" not in entry:
                raise TS015Error(
                    "ACK entry missing receiver context (receiver field absent)",
                    code=ERR_RECEIVER_CONTEXT_MISSING,
                )
            missing = [f for f in self.REQUIRED_FIELDS if f not in entry]
            if missing:
                raise TS015Error(
                    "ACK entry missing required field(s): %s"
                    % ", ".join(missing)
                )
            for field in self.REQUIRED_FIELDS:
                if not _nonempty(entry.get(field)):
                    if field == "receiver":
                        raise TS015Error(
                            "ACK entry missing receiver context "
                            "(receiver field empty)",
                            code=ERR_RECEIVER_CONTEXT_MISSING,
                        )
                    raise TS015Error(
                        "ACK entry field %r must be non-empty" % field
                    )
            decision = entry["decision"]
            if decision not in self.ALLOWED_DECISIONS:
                raise TS015Error(
                    "ACK entry decision must be ACK or NACK, got %r"
                    % (decision,)
                )
            try:
                datetime.fromisoformat(entry["timestamp"])
            except (TypeError, ValueError):
                raise TS015Error(
                    "ACK entry timestamp must be ISO8601: %r"
                    % (entry.get("timestamp"),)
                )
            frozen.append(
                {
                    "task_id": entry["task_id"],
                    "receiver": entry["receiver"],
                    "decision": entry["decision"],
                    "timestamp": entry["timestamp"],
                }
            )
        self._entries = tuple(frozen)

    @property
    def entries(self):
        return tuple(dict(e) for e in self._entries)

    @property
    def count(self):
        return len(self._entries)

    def append(self, entry):
        """Return a new ledger with entry appended; never mutates self."""
        return AckLedger(list(self._entries) + [entry])


def make_ack_entry(**overrides):
    base = {
        "task_id": "TS-015",
        "receiver": "GPT B / OROCHI Handoff Lead",
        "decision": "ACK",
        "timestamp": "2026-08-11T00:00:00+08:00",
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------------------------
# Positive tests
# ---------------------------------------------------------------------------
class TS015PositiveTests(unittest.TestCase):
    def test_pos_001_all_target_files_exist(self):
        for path in (COMMAND_PACK_PATH, EXECUTION_PACKET_PATH, ACK_LEDGER_PATH):
            self.assertTrue(os.path.isfile(path), "missing target %s" % path)

    def test_pos_002_command_pack_complete(self):
        data = load_yaml(COMMAND_PACK_PATH)
        self.assertEqual(data["pack_id"], "gpt-b-command-pack-ts015")
        self.assertEqual(data["schema_version"], "1.0.0")
        self.assertEqual(data["spec_ref"], "TS-015/ART-15")
        self.assertEqual(data["receiver"], "GPT B / OROCHI Handoff Lead")
        # deterministic fail-closed declarations
        self.assertIs(data["fail_closed"], True)
        self.assertIs(data["no_broker_write"], True)
        self.assertIs(data["no_network"], True)
        pack = CommandPack(load_command_entries())
        self.assertEqual(pack.task_ids, ("TS-015",))
        entry = pack.entries[0]
        self.assertTrue(entry["commands"])
        for command in entry["commands"]:
            self.assertIsInstance(command, str)
            self.assertTrue(command.strip())
        # allowlist is exactly the canonical target set, and every target
        # actually exists on disk
        self.assertEqual(entry["allowlist"], EXPECTED_TARGETS_REL)
        for rel in entry["allowlist"]:
            self.assertTrue(
                os.path.isfile(os.path.join(ROOT, rel)), "missing %s" % rel
            )

    def test_pos_003_execution_packet_valid(self):
        data = load_yaml(EXECUTION_PACKET_PATH)
        self.assertEqual(data["execution_packet_id"], "orochi-execution-packet-ts015")
        self.assertEqual(data["schema_version"], "1.0.0")
        self.assertEqual(data["spec_ref"], "TS-015/ART-15")
        packet = ExecutionPacket(load_execution_entries())
        self.assertEqual(packet.task_ids, ("TS-015",))
        entry = packet.entries[0]
        context = entry["context"]
        self.assertEqual(context["work_order"], "WO-TS-REF-15")
        self.assertEqual(context["path_status"], "PROPOSED_NOT_MATERIALIZED")
        self.assertEqual(context["runtime_status"], "NOT_RUN")
        contract = entry["contract"]
        self.assertEqual(contract["target_files_exact_set"], list(EXPECTED_TARGETS_REL))
        self.assertEqual(
            contract["required_ack_fields"], list(REQUIRED_ACK_FIELDS)
        )
        self.assertEqual(
            contract["error_receiver_context_missing"],
            ERR_RECEIVER_CONTEXT_MISSING,
        )
        self.assertIs(contract["fail_closed"], True)
        self.assertIs(contract["no_broker_write"], True)
        self.assertIs(contract["no_network"], True)
        self.assertTrue(contract["rollback"].strip())

    def test_pos_004_ack_ledger_append_only(self):
        # canonical ledger exists and is a valid ledger; it is currently
        # empty because consumer ACK is NOT_RUN (no ACK recorded yet)
        self.assertTrue(os.path.isfile(ACK_LEDGER_PATH))
        canonical = AckLedger(parse_ack_entries(read_text(ACK_LEDGER_PATH)))
        self.assertEqual(canonical.count, 0)
        entry1 = make_ack_entry()
        entry2 = make_ack_entry(
            receiver="OROCHI external executor",
            decision="NACK",
            timestamp="2026-08-11T01:00:00+08:00",
        )
        ledger1 = canonical.append(entry1)
        self.assertEqual(ledger1.count, 1)
        self.assertEqual(ledger1.entries[0], entry1)
        # append-only: the source ledger is never mutated in place
        self.assertEqual(canonical.count, 0)
        ledger2 = ledger1.append(entry2)
        self.assertEqual(ledger2.count, 2)
        self.assertEqual(
            [e["task_id"] for e in ledger2.entries], ["TS-015", "TS-015"]
        )
        # existing entries are preserved in order
        self.assertEqual(ledger2.entries[0], entry1)
        self.assertEqual(ledger2.entries[1], entry2)
        # ledger1 is unchanged after ledger2 was derived from it
        self.assertEqual(ledger1.count, 1)
        self.assertEqual(ledger1.entries[0], entry1)


# ---------------------------------------------------------------------------
# Negative tests - a FRESH AckLedger is created per test case (setUp), so
# there is no cross-case contamination; rejected entries never mutate state.
# ---------------------------------------------------------------------------
class TS015NegativeTests(unittest.TestCase):
    def setUp(self):
        self.ledger = AckLedger([])

    def test_neg_001_ack_missing_receiver_raises_err_receiver_context_missing(self):
        entry = make_ack_entry()
        del entry["receiver"]
        with self.assertRaises(TS015Error) as ctx:
            self.ledger.append(entry)
        self.assertEqual(ctx.exception.code, ERR_RECEIVER_CONTEXT_MISSING)
        self.assertIn("receiver", str(ctx.exception))

    def test_neg_002_ack_blank_receiver_raises_err_receiver_context_missing(self):
        entry = make_ack_entry(receiver="   ")
        with self.assertRaises(TS015Error) as ctx:
            AckLedger([entry])
        self.assertEqual(ctx.exception.code, ERR_RECEIVER_CONTEXT_MISSING)
        self.assertIn("receiver", str(ctx.exception))

    def test_neg_003_rejected_ack_never_mutates_ledger(self):
        before = self.ledger.entries
        bad = make_ack_entry()
        del bad["receiver"]
        with self.assertRaises(TS015Error):
            self.ledger.append(bad)
        # fail-closed: the rejected entry produced no partial state
        self.assertEqual(self.ledger.entries, before)
        self.assertEqual(self.ledger.count, 0)
        # the same fresh ledger still accepts a clean entry afterwards
        ok = self.ledger.append(make_ack_entry())
        self.assertEqual(ok.count, 1)
        self.assertEqual(self.ledger.count, 0)

    def test_neg_004_ack_invalid_decision_rejected(self):
        entry = make_ack_entry(decision="MAYBE")
        with self.assertRaises(TS015Error) as ctx:
            AckLedger([entry])
        self.assertIn("decision", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)

    def test_neg_005_ack_invalid_timestamp_rejected(self):
        entry = make_ack_entry(timestamp="not-a-timestamp")
        with self.assertRaises(TS015Error) as ctx:
            AckLedger([entry])
        self.assertIn("timestamp", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)


# ---------------------------------------------------------------------------
# Edge tests
# ---------------------------------------------------------------------------
class TS015EdgeTests(unittest.TestCase):
    def test_edge_001_empty_ack_ledger_allowed(self):
        # the canonical ledger is empty: a valid deterministic state
        self.assertTrue(os.path.isfile(ACK_LEDGER_PATH))
        text = read_text(ACK_LEDGER_PATH)
        self.assertEqual(text.strip(), "")
        ledger = AckLedger(parse_ack_entries(text))
        self.assertEqual(ledger.count, 0)
        self.assertEqual(ledger.entries, ())
        # an empty ledger still accepts the first append
        appended = ledger.append(make_ack_entry())
        self.assertEqual(appended.count, 1)

    def test_edge_002_missing_required_field_rejected(self):
        for missing in ("task_id", "decision", "timestamp"):
            entry = make_ack_entry()
            del entry[missing]
            with self.assertRaises(TS015Error) as ctx:
                AckLedger([entry])
            # field-naming error (code None), distinct from
            # ERR_RECEIVER_CONTEXT_MISSING
            self.assertIn(missing, str(ctx.exception))
            self.assertIsNone(ctx.exception.code)

    def test_edge_003_command_pack_entry_missing_allowlist_rejected(self):
        entries = load_command_entries()
        del entries[0]["allowlist"]
        with self.assertRaises(TS015Error) as ctx:
            CommandPack(entries)
        self.assertIn("allowlist", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)

    def test_edge_004_execution_packet_entry_missing_contract_rejected(self):
        entries = load_execution_entries()
        del entries[0]["contract"]
        with self.assertRaises(TS015Error) as ctx:
            ExecutionPacket(entries)
        self.assertIn("contract", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)

    def test_edge_005_malformed_ack_line_rejected(self):
        with self.assertRaises(TS015Error) as ctx:
            parse_ack_entries('{"task_id": "TS-015", "receiver": broken}\n')
        self.assertIn("malformed", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)

    def test_edge_006_non_object_ack_line_rejected(self):
        with self.assertRaises(TS015Error) as ctx:
            parse_ack_entries("[1, 2, 3]\n")
        self.assertIn("JSON object", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)


if __name__ == "__main__":
    unittest.main()