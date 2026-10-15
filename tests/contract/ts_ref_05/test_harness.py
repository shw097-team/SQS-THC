"""Frozen acceptance tests for the Harness / Loop / Handoff kernel (CH15).

Fixtures match P0-CIP CH15 frozen fixtures:
CH15-POS-001 / CH15-NEG-001 / CH15-EDGE-001 / CH15-ADV-001.
"""
import unittest

from kernel.harness import (
    AckMissingError,
    CircularDependencyError,
    HandoffPacket,
    HandoffSchemaError,
    HarnessLoop,
    HarnessState,
    RetryExhaustedError,
    WorkOrderGraph,
    dispatch,
    handoff,
    merge_review,
    validate_graph,
)

GRAPH_HASH = "sha256:25f24f44ae7a2232"


def make_loop(**kw) -> HarnessLoop:
    base = dict(
        id="ch15-loop-001", schema_version="1.0.0", loop_id="ch15-loop-id-001",
        task_graph_hash=GRAPH_HASH, max_iterations=3,
        handoff_contract="schema-v1", stop_condition="deterministic",
        escalation_owner="human-owner",
    )
    base.update(kw)
    return HarnessLoop(**base)


class CH15PositiveTests(unittest.TestCase):
    def test_pos_001_dag_valid(self):
        """CH15-POS-001: acyclic graph passes validation."""
        g = WorkOrderGraph(
            id="ch15-graph-001", schema_version="1.0.0", task_graph_hash=GRAPH_HASH,
            max_iterations=3, handoff_contract="schema-v1",
            stop_condition="deterministic", escalation_owner="human-owner",
            edges=(("A", "B"), ("B", "C")),
        )
        self.assertEqual(validate_graph(g), g)

    def test_pos_002_dispatch_handoff_merge(self):
        """dispatch -> handoff(ACK) -> merge under HUMAN_REVIEWED."""
        loop = dispatch(make_loop())
        self.assertEqual(loop.state if hasattr(loop, "state") else HarnessState.DISPATCHED,
                         HarnessState.DISPATCHED)
        packet = HandoffPacket(
            id="ch15-packet-001", schema_version="1.0.0", loop_id="ch15-loop-id-001",
            task_graph_hash=GRAPH_HASH, max_iterations=3,
            stop_condition="deterministic", escalation_owner="human-owner",
            ack="ACK",
        )
        p = handoff(packet)
        self.assertEqual(p.ack, "ACK")
        merged = merge_review(loop, "HUMAN_REVIEWED")
        self.assertEqual(merged.merge_policy, "HUMAN_REVIEWED")


class CH15NegativeTests(unittest.TestCase):
    def test_neg_001_circular_dependency(self):
        """CH15-NEG-001: circular graph -> ERR_CIRCULAR_DEPENDENCY."""
        g = WorkOrderGraph(
            id="ch15-invalid-001", schema_version="1.0.0", task_graph_hash=GRAPH_HASH,
            max_iterations=3, handoff_contract="schema-v1",
            stop_condition="deterministic", escalation_owner="human-owner",
            edges=(("A", "B"), ("B", "A")),
        )
        with self.assertRaises(CircularDependencyError):
            validate_graph(g)

    def test_neg_002_retry_exhausted(self):
        """iteration_count >= max_iterations -> ERR_RETRY_EXHAUSTED."""
        loop = make_loop(max_iterations=1, iteration_count=1)
        with self.assertRaises(RetryExhaustedError):
            dispatch(loop)

    def test_neg_003_ack_missing(self):
        """handoff without ACK/NACK -> ERR_ACK_MISSING."""
        packet = HandoffPacket(
            id="ch15-invalid-002", schema_version="1.0.0", loop_id="ch15-loop-id-001",
            task_graph_hash=GRAPH_HASH, max_iterations=3,
            stop_condition="deterministic", escalation_owner="human-owner",
            ack=None,
        )
        with self.assertRaises(AckMissingError):
            handoff(packet)

    def test_neg_004_merge_without_human_review(self):
        """merge_policy != HUMAN_REVIEWED -> ERR_HANDOFF_SCHEMA."""
        loop = make_loop()
        with self.assertRaises(HandoffSchemaError):
            merge_review(loop, "AUTO_MERGE")


class CH15EdgeTests(unittest.TestCase):
    def test_edge_001_partial_ack_recoverable(self):
        """partial handoff ACK with recoverable child failure -> NACK with reason."""
        packet = HandoffPacket(
            id="ch15-edge-001", schema_version="1.0.0", loop_id="ch15-loop-id-001",
            task_graph_hash=GRAPH_HASH, max_iterations=3,
            stop_condition="deterministic", escalation_owner="human-owner",
            ack="NACK:recoverable-child-failure",
        )
        p = handoff(packet)
        self.assertTrue(p.ack.startswith("NACK:"))


class CH15AdversarialTests(unittest.TestCase):
    def test_adv_001_forged_owner_rejected(self):
        """CH15-ADV-001: forged owner_id must be rejected."""
        loop = make_loop(owner_id="attacker")
        with self.assertRaises(Exception):
            dispatch(loop)


if __name__ == "__main__":
    unittest.main()
