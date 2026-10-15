# TS-011 Maturity/SRE/security acceptance tests (WO-TS-REF-11).
#
# Pure stdlib unittest - no third-party dependencies. Deterministic and
# fail-closed: any missing file, malformed artifact, or unexpected construct
# raises and fails the suite. No broker write, no network.
#
# Positive: maturity levels are valid (id, name, evidence_required), each SLO
# is present with a resolvable runbook reference, security policies are
# present, privacy entries and supply chain pins are well-formed, and
# docs/DOC-11.md anchors the whole domain.
# Negative: ERR_PROMOTION_WITHOUT_EVIDENCE - promotion to a maturity level
# without the evidence required by that level AND every previous level. A
# FRESH MaturityModel and FRESH evidence set are created per test case
# (setUp), so there is no cross-case contamination; a rejected promotion
# never mutates model or evidence state.
# Edge: empty policies are allowed (valid state); a missing required field is
# rejected with a field-naming error (code None), distinct from
# ERR_PROMOTION_WITHOUT_EVIDENCE; dangling runbook references, mismatched SLO
# targets, orphan runbooks and resolved-before-qualification pins are
# rejected (fail-closed).
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DOC_11_PATH = os.path.join(ROOT, "docs", "DOC-11.md")
MATURITY_MODEL_PATH = os.path.join(ROOT, "maturity", "maturity-model.yaml")
SRE_SLOS_PATH = os.path.join(ROOT, "sre", "slos.yaml")
SRE_RUNBOOKS_PATH = os.path.join(ROOT, "sre", "runbooks.yaml")
SECURITY_POLICIES_PATH = os.path.join(ROOT, "security", "policies.yaml")
PRIVACY_REGISTER_PATH = os.path.join(ROOT, "privacy", "register.yaml")
SUPPLY_CHAIN_PINS_PATH = os.path.join(ROOT, "supply-chain", "pins.yaml")

ERR_PROMOTION_WITHOUT_EVIDENCE = "ERR_PROMOTION_WITHOUT_EVIDENCE"
CLAIM_CEILING_LOCAL_DELIVERY = "LOCAL_DELIVERY"

REQUIRED_LEVEL_FIELDS = ("id", "name", "evidence_required")
REQUIRED_SLO_FIELDS = ("id", "slo_target", "runbook_ref")
REQUIRED_RUNBOOK_FIELDS = ("id", "slo_target", "runbook_ref")
REQUIRED_POLICY_FIELDS = ("id", "policy")
REQUIRED_PRIVACY_FIELDS = ("id", "scope")
REQUIRED_PIN_FIELDS = ("id", "tool", "pin", "status")

PIN_UNRESOLVED_RE = re.compile(r"^UNRESOLVED::TOOL-\d{2}::PIN$")
ALLOWED_PIN_STATUSES = (
    "BLOCKED_PENDING_QUALIFICATION",
    "ROUTE_OUT_NOT_RUN",
    "DISABLED_DEFERRED",
)
PIN_BY_STATUS = {
    "BLOCKED_PENDING_QUALIFICATION": PIN_UNRESOLVED_RE,
    "ROUTE_OUT_NOT_RUN": "EXTERNAL_EXECUTOR_PIN_REQUIRED",
    "DISABLED_DEFERRED": "DEFERRED_UNTIL_TRIGGER",
}


# ---------------------------------------------------------------------------
# Minimal deterministic YAML-subset parser (stdlib only, fail-closed).
# Supports the exact constructs used by the TS-011 artifacts:
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
                    "nested mapping not used by TS-011 artifacts: %r" % nxt
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


def load_maturity_levels():
    return load_yaml(MATURITY_MODEL_PATH)["levels"]


def load_slos():
    return load_yaml(SRE_SLOS_PATH)["slos"]


def load_runbooks():
    return load_yaml(SRE_RUNBOOKS_PATH)["runbooks"]


def load_policies():
    return load_yaml(SECURITY_POLICIES_PATH)["policies"]


def load_privacy():
    return load_yaml(PRIVACY_REGISTER_PATH)["register"]


def load_pins():
    return load_yaml(SUPPLY_CHAIN_PINS_PATH)["pins"]


# ---------------------------------------------------------------------------
# Fail-closed TS-011 maturity/SRE/security semantics used by the
# negative/edge cases.
# ---------------------------------------------------------------------------
class MaturitySreSecurityError(Exception):
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


def _require_fields(record, fields, label):
    if not isinstance(record, dict):
        raise MaturitySreSecurityError("%s must be a mapping" % label)
    missing = [f for f in fields if f not in record]
    if missing:
        raise MaturitySreSecurityError(
            "%s missing required field(s): %s" % (label, ", ".join(missing))
        )


def _validate_slo_target(record, label):
    target = record.get("slo_target")
    if not _is_number(target) or target <= 0 or target > 1:
        raise MaturitySreSecurityError(
            "%s slo_target must be a number in (0, 1]" % label
        )


class MaturityModel(object):
    """Deterministic, fail-closed maturity model (CH30 / MC-26).

    Levels are ordered; promotion to a level requires the evidence required
    by that level AND every previous level (each maturity plane has
    independent evidence AND previous plane passed AND rollback rehearsal
    complete). Promotion without that evidence raises
    ERR_PROMOTION_WITHOUT_EVIDENCE and performs no mutation. A fresh instance
    is created per test case so failed promotions never leak state.
    """

    def __init__(self, levels):
        if not isinstance(levels, list) or not levels:
            raise MaturitySreSecurityError(
                "maturity levels must be a non-empty list"
            )
        seen_ids = set()
        seen_names = set()
        for level in levels:
            _require_fields(level, REQUIRED_LEVEL_FIELDS, "maturity level")
            if not _nonempty(level.get("id")) or not _nonempty(level.get("name")):
                raise MaturitySreSecurityError(
                    "maturity level id and name must be non-empty"
                )
            evidence = level.get("evidence_required")
            if not isinstance(evidence, list) or not evidence:
                raise MaturitySreSecurityError(
                    "maturity level %r evidence_required must be a non-empty "
                    "list" % (level.get("id"),)
                )
            for item in evidence:
                if not isinstance(item, str) or not item.strip():
                    raise MaturitySreSecurityError(
                        "maturity level %r evidence item must be a non-empty "
                        "string" % (level.get("id"),)
                    )
            if level["id"] in seen_ids:
                raise MaturitySreSecurityError(
                    "duplicate maturity level id %r" % level["id"]
                )
            if level["name"] in seen_names:
                raise MaturitySreSecurityError(
                    "duplicate maturity level name %r" % level["name"]
                )
            seen_ids.add(level["id"])
            seen_names.add(level["name"])
        self._levels = [dict(level) for level in levels]

    @property
    def levels(self):
        return tuple(dict(level) for level in self._levels)

    def index_of(self, level_id):
        for i, level in enumerate(self._levels):
            if level["id"] == level_id:
                return i
        raise MaturitySreSecurityError("unknown maturity level %r" % level_id)

    def evidence_for(self, level_id):
        """Cumulative evidence required to reach level_id (this level AND
        every previous level)."""
        idx = self.index_of(level_id)
        required = []
        for level in self._levels[: idx + 1]:
            required.extend(level["evidence_required"])
        return tuple(required)

    def promote(self, level_id, evidence):
        required = self.evidence_for(level_id)
        evidence_set = set(evidence)
        missing = [item for item in required if item not in evidence_set]
        if missing:
            raise MaturitySreSecurityError(
                "promotion to maturity level %r without evidence; missing: %s"
                % (level_id, ", ".join(missing)),
                code=ERR_PROMOTION_WITHOUT_EVIDENCE,
            )
        return True


def validate_slos(slos, runbooks):
    """Every SLO carries id/slo_target/runbook_ref; the runbook_ref resolves
    to a runbook id in sre/runbooks.yaml whose slo_target matches."""
    if not isinstance(slos, list) or not slos:
        raise MaturitySreSecurityError("slos must be a non-empty list")
    runbook_by_id = {}
    for runbook in runbooks:
        _require_fields(runbook, REQUIRED_RUNBOOK_FIELDS, "runbook")
        runbook_by_id[runbook["id"]] = runbook
    for slo in slos:
        _require_fields(slo, REQUIRED_SLO_FIELDS, "slo")
        _validate_slo_target(slo, "slo")
        ref = slo.get("runbook_ref")
        if not isinstance(ref, str) or not ref.startswith("sre/runbooks.yaml#"):
            raise MaturitySreSecurityError(
                "slo %r runbook_ref must anchor to sre/runbooks.yaml#<runbook-id>"
                % (slo.get("id"),)
            )
        runbook_id = ref.split("#", 1)[1]
        if runbook_id not in runbook_by_id:
            raise MaturitySreSecurityError(
                "slo %r runbook_ref is dangling: %r" % (slo.get("id"), ref)
            )
        if runbook_by_id[runbook_id]["slo_target"] != slo["slo_target"]:
            raise MaturitySreSecurityError(
                "slo %r runbook %r slo_target mismatch"
                % (slo.get("id"), runbook_id)
            )
    return True


def validate_runbooks(slos, runbooks):
    """Every runbook carries id/slo_target/runbook_ref and defends at least
    one SLO (no orphan runbooks)."""
    if not isinstance(runbooks, list) or not runbooks:
        raise MaturitySreSecurityError("runbooks must be a non-empty list")
    referenced = set()
    for slo in slos:
        ref = slo.get("runbook_ref")
        if isinstance(ref, str) and ref.startswith("sre/runbooks.yaml#"):
            referenced.add(ref.split("#", 1)[1])
    for runbook in runbooks:
        _require_fields(runbook, REQUIRED_RUNBOOK_FIELDS, "runbook")
        _validate_slo_target(runbook, "runbook")
        if not _nonempty(runbook.get("runbook_ref")):
            raise MaturitySreSecurityError(
                "runbook %r runbook_ref must be non-empty" % runbook.get("id")
            )
        if runbook["id"] not in referenced:
            raise MaturitySreSecurityError(
                "runbook %r has no defending SLO" % runbook["id"]
            )
    return True


def validate_policies(policies):
    """An empty policy list is a valid state; a policy missing id or policy
    is rejected (field-naming error)."""
    if not isinstance(policies, list):
        raise MaturitySreSecurityError("policies must be a list")
    for policy in policies:
        _require_fields(policy, REQUIRED_POLICY_FIELDS, "security policy")
        if not _nonempty(policy.get("id")) or not _nonempty(policy.get("policy")):
            raise MaturitySreSecurityError(
                "security policy id and policy must be non-empty"
            )
    return True


def validate_privacy(register):
    if not isinstance(register, list) or not register:
        raise MaturitySreSecurityError("privacy register must be a non-empty list")
    for entry in register:
        _require_fields(entry, REQUIRED_PRIVACY_FIELDS, "privacy entry")
        if not _nonempty(entry.get("id")) or not _nonempty(entry.get("scope")):
            raise MaturitySreSecurityError(
                "privacy entry id and scope must be non-empty"
            )
    return True


def validate_pins(pins):
    """Supply chain pins in TOOL card format. An ADOPT tool carries
    pin UNRESOLVED::TOOL-xx::PIN and status BLOCKED_PENDING_QUALIFICATION; a
    resolved-looking pin before qualification is rejected (fail-closed)."""
    if not isinstance(pins, list) or not pins:
        raise MaturitySreSecurityError("supply-chain pins must be a non-empty list")
    seen = set()
    for pin in pins:
        _require_fields(pin, REQUIRED_PIN_FIELDS, "supply-chain pin")
        for field in ("id", "tool", "pin", "status"):
            if not _nonempty(pin.get(field)):
                raise MaturitySreSecurityError(
                    "supply-chain pin field %r must be non-empty" % field
                )
        if pin["id"] in seen:
            raise MaturitySreSecurityError(
                "duplicate supply-chain pin id %r" % pin["id"]
            )
        seen.add(pin["id"])
        status = pin["status"]
        if status not in ALLOWED_PIN_STATUSES:
            raise MaturitySreSecurityError(
                "supply-chain pin %r unknown status %r" % (pin["id"], status)
            )
        expected = PIN_BY_STATUS[status]
        if hasattr(expected, "match"):
            if not expected.match(pin["pin"]):
                raise MaturitySreSecurityError(
                    "supply-chain pin %r must use TOOL card format "
                    "UNRESOLVED::TOOL-xx::PIN" % pin["id"]
                )
        elif pin["pin"] != expected:
            raise MaturitySreSecurityError(
                "supply-chain pin %r must use pin %r for status %r"
                % (pin["id"], expected, status)
            )
    return True


# ---------------------------------------------------------------------------
# Positive tests
# ---------------------------------------------------------------------------
class TS011PositiveTests(unittest.TestCase):
    def test_pos_001_all_target_files_exist(self):
        for path in (
            DOC_11_PATH,
            MATURITY_MODEL_PATH,
            SRE_SLOS_PATH,
            SRE_RUNBOOKS_PATH,
            SECURITY_POLICIES_PATH,
            PRIVACY_REGISTER_PATH,
            SUPPLY_CHAIN_PINS_PATH,
        ):
            self.assertTrue(os.path.isfile(path), "missing target %s" % path)

    def test_pos_002_maturity_levels_valid(self):
        data = load_yaml(MATURITY_MODEL_PATH)
        self.assertEqual(data["maturity_model_id"], "maturity-model-ts011")
        self.assertEqual(data["spec_ref"], "TS-011/CH30")
        model = MaturityModel(load_maturity_levels())
        self.assertGreaterEqual(len(model.levels), 2)
        for level in model.levels:
            for field in REQUIRED_LEVEL_FIELDS:
                self.assertIn(field, level, "level missing %r" % field)
            self.assertTrue(
                _nonempty(level["evidence_required"]),
                "level %r evidence_required empty" % level["id"],
            )
        # full cumulative evidence promotes for every level
        for level in model.levels:
            self.assertTrue(
                model.promote(level["id"], model.evidence_for(level["id"]))
            )
        # sequential promotion works
        evidence = set()
        for level in model.levels:
            evidence.update(level["evidence_required"])
            self.assertTrue(model.promote(level["id"], evidence))

    def test_pos_003_slo_present_and_cross_referenced(self):
        slos = load_slos()
        runbooks = load_runbooks()
        self.assertEqual(load_yaml(SRE_SLOS_PATH)["spec_ref"], "TS-011/CH31")
        self.assertEqual(load_yaml(SRE_RUNBOOKS_PATH)["spec_ref"], "TS-011/CH31")
        self.assertTrue(validate_slos(slos, runbooks))
        self.assertTrue(validate_runbooks(slos, runbooks))
        runbook_ids = {r["id"] for r in runbooks}
        self.assertGreaterEqual(len(slos), 1)
        for slo in slos:
            self.assertIn("id", slo)
            self.assertGreater(slo["slo_target"], 0)
            self.assertLessEqual(slo["slo_target"], 1)
            runbook_id = slo["runbook_ref"].split("#", 1)[1]
            self.assertIn(runbook_id, runbook_ids)

    def test_pos_004_security_policy_present(self):
        self.assertEqual(load_yaml(SECURITY_POLICIES_PATH)["spec_ref"], "TS-011/CH32")
        policies = load_policies()
        self.assertTrue(validate_policies(policies))
        self.assertGreaterEqual(len(policies), 1)
        for policy in policies:
            self.assertIn("id", policy)
            self.assertIn("policy", policy)
            self.assertTrue(_nonempty(policy["policy"]))

    def test_pos_005_privacy_register_well_formed(self):
        self.assertEqual(load_yaml(PRIVACY_REGISTER_PATH)["spec_ref"], "TS-011/CH32")
        register = load_privacy()
        self.assertTrue(validate_privacy(register))
        self.assertGreaterEqual(len(register), 1)
        for entry in register:
            self.assertIn("id", entry)
            self.assertIn("scope", entry)
            self.assertTrue(_nonempty(entry["scope"]))

    def test_pos_006_supply_chain_pins_tool_card_format(self):
        self.assertEqual(
            load_yaml(SUPPLY_CHAIN_PINS_PATH)["spec_ref"], "TS-011/CH32"
        )
        pins = load_pins()
        self.assertTrue(validate_pins(pins))
        adopt = [p for p in pins if p["status"] == "BLOCKED_PENDING_QUALIFICATION"]
        self.assertGreaterEqual(len(adopt), 1)
        for pin in adopt:
            self.assertIsNotNone(
                PIN_UNRESOLVED_RE.match(pin["pin"]),
                "ADOPT pin %r must be UNRESOLVED::TOOL-xx::PIN" % pin["id"],
            )
            self.assertIn("TOOL-", pin["pin"])

    def test_pos_007_doc11_maturity_sre_security_document(self):
        text = read_text(DOC_11_PATH)
        for token in (
            "SQS-THC",
            "WO-TS-REF-11",
            "TS-011",
            "ART-11",
            "MC-26",
            "CH30",
            "CH31",
            "CH32",
            "maturity/maturity-model.yaml",
            "sre/slos.yaml",
            "sre/runbooks.yaml",
            "security/policies.yaml",
            "privacy/register.yaml",
            "supply-chain/pins.yaml",
            "ERR_PROMOTION_WITHOUT_EVIDENCE",
            CLAIM_CEILING_LOCAL_DELIVERY,
            "F28-01",
            "F31-01",
            "SRE and Security Team",
        ):
            self.assertIn(token, text, "DOC-11 missing token %r" % token)


# ---------------------------------------------------------------------------
# Negative tests - a FRESH MaturityModel and a FRESH evidence set are created
# per test case (setUp), so there is no cross-case contamination.
# ---------------------------------------------------------------------------
class TS011NegativeTests(unittest.TestCase):
    def setUp(self):
        self.model = MaturityModel(load_maturity_levels())
        self.evidence = set()

    def test_neg_001_promote_to_paper_without_paper_evidence(self):
        self.evidence.update(
            ["candidate_version", "source_authority_ref", "version_permission_clock"]
        )
        with self.assertRaises(MaturitySreSecurityError) as ctx:
            self.model.promote("maturity-level-paper", self.evidence)
        self.assertEqual(ctx.exception.code, ERR_PROMOTION_WITHOUT_EVIDENCE)
        self.assertIn("paper_receipt", str(ctx.exception))

    def test_neg_002_promote_to_live_blocked_without_gate(self):
        self.evidence.update(self.model.evidence_for("maturity-level-paper"))
        with self.assertRaises(MaturitySreSecurityError) as ctx:
            self.model.promote("maturity-level-live-blocked", self.evidence)
        self.assertEqual(ctx.exception.code, ERR_PROMOTION_WITHOUT_EVIDENCE)
        self.assertIn("promotion_gate", str(ctx.exception))

    def test_neg_003_promote_to_shadow_skipping_paper_plane(self):
        self.evidence.update(
            ["candidate_version", "source_authority_ref", "version_permission_clock"]
        )
        with self.assertRaises(MaturitySreSecurityError) as ctx:
            self.model.promote("maturity-level-shadow", self.evidence)
        self.assertEqual(ctx.exception.code, ERR_PROMOTION_WITHOUT_EVIDENCE)
        self.assertIn("paper_receipt", str(ctx.exception))
        self.assertIn("shadow_receipt", str(ctx.exception))

    def test_neg_004_promote_with_empty_evidence(self):
        with self.assertRaises(MaturitySreSecurityError) as ctx:
            self.model.promote("maturity-level-design", self.evidence)
        self.assertEqual(ctx.exception.code, ERR_PROMOTION_WITHOUT_EVIDENCE)

    def test_neg_005_failed_promotion_never_mutates_state(self):
        before_levels = self.model.levels
        before_evidence = set(self.evidence)
        with self.assertRaises(MaturitySreSecurityError):
            self.model.promote("maturity-level-live-blocked", {})
        self.assertEqual(self.model.levels, before_levels)
        self.assertEqual(self.evidence, before_evidence)
        # fresh model accepts a fully evidenced promotion (no contamination)
        fresh = MaturityModel(load_maturity_levels())
        self.assertTrue(
            fresh.promote(
                "maturity-level-live-blocked",
                fresh.evidence_for("maturity-level-live-blocked"),
            )
        )


# ---------------------------------------------------------------------------
# Edge tests
# ---------------------------------------------------------------------------
class TS011EdgeTests(unittest.TestCase):
    def test_edge_001_empty_policies_allowed(self):
        # an empty policy list is a valid state (no policy ratified yet)
        self.assertTrue(validate_policies([]))
        self.assertTrue(validate_policies([dict(load_policies()[0])]))
        with self.assertRaises(MaturitySreSecurityError):
            validate_policies("not-a-list")

    def test_edge_002_missing_required_field_rejected(self):
        # SLO missing slo_target -> field-naming error, not promotion error
        slos = [dict(s) for s in load_slos()]
        del slos[0]["slo_target"]
        with self.assertRaises(MaturitySreSecurityError) as ctx:
            validate_slos(slos, load_runbooks())
        self.assertIn("slo_target", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)
        # maturity level missing name -> field-naming error
        levels = load_maturity_levels()
        broken = [dict(levels[0])]
        del broken[0]["name"]
        with self.assertRaises(MaturitySreSecurityError) as ctx:
            MaturityModel(broken)
        self.assertIn("name", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)

    def test_edge_003_dangling_runbook_ref_rejected(self):
        slos = [dict(s) for s in load_slos()]
        slos[0]["runbook_ref"] = "sre/runbooks.yaml#runbook-does-not-exist"
        with self.assertRaises(MaturitySreSecurityError) as ctx:
            validate_slos(slos, load_runbooks())
        self.assertIn("runbook-does-not-exist", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)

    def test_edge_004_resolved_pin_before_qualification_rejected(self):
        pins = [dict(p) for p in load_pins()]
        pins[0]["pin"] = "git@sha256:deadbeef"  # ADOPT must stay UNRESOLVED
        with self.assertRaises(MaturitySreSecurityError) as ctx:
            validate_pins(pins)
        self.assertIn("UNRESOLVED", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)

    def test_edge_005_slo_runbook_target_mismatch_rejected(self):
        slos = [dict(s) for s in load_slos()]
        slos[0]["slo_target"] = 0.5
        with self.assertRaises(MaturitySreSecurityError) as ctx:
            validate_slos(slos, load_runbooks())
        self.assertIn("mismatch", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)

    def test_edge_006_runbook_without_defending_slo_rejected(self):
        runbooks = [dict(r) for r in load_runbooks()]
        runbooks.append(
            {
                "id": "runbook-orphan",
                "slo_target": 0.9,
                "runbook_ref": "TS-011/CH31#observe-bound-contain-restore-reconcile",
            }
        )
        with self.assertRaises(MaturitySreSecurityError) as ctx:
            validate_runbooks(load_slos(), runbooks)
        self.assertIn("runbook-orphan", str(ctx.exception))
        self.assertIsNone(ctx.exception.code)


if __name__ == "__main__":
    unittest.main()
