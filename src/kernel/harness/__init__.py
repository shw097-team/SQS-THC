"""SQS-THC Harness / Loop / Multi-agent Handoff — package kernel (TS-REF-05 / CH15).

Implements the CH15 core acceptance predicate:
    iteration_count <= max_iterations AND stop_condition deterministic AND
    each handoff has ACK/NACK AND merge_policy='HUMAN_REVIEWED'
with owner verification against ``Harness and Multi-agent Workflow Owner``.
"""
from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass, replace
from enum import Enum


HARNESS_OWNER_ID = "Harness and Multi-agent Workflow Owner"
EXPECTED_SCHEMA_VERSION = "1.0.0"
DETERMINISTIC_STOP = "deterministic"
HUMAN_REVIEWED_POLICY = "HUMAN_REVIEWED"


class HarnessState(str, Enum):
    QUEUED = "QUEUED"
    DISPATCHED = "DISPATCHED"
    WAITING_ACK = "WAITING_ACK"
    COMPLETE = "COMPLETE"


class HarnessError(Exception):
    code = "ERR_HARNESS"


class HandoffSchemaError(HarnessError):
    code = "ERR_HANDOFF_SCHEMA"


class CircularDependencyError(HarnessError):
    code = "ERR_CIRCULAR_DEPENDENCY"


class RetryExhaustedError(HarnessError):
    code = "ERR_RETRY_EXHAUSTED"


class AckMissingError(HarnessError):
    code = "ERR_ACK_MISSING"


@dataclass(frozen=True)
class HarnessLoop:
    id: str
    schema_version: str
    loop_id: str
    task_graph_hash: str
    max_iterations: int
    handoff_contract: str
    stop_condition: str
    escalation_owner: str
    merge_policy: str = "HUMAN_REVIEWED"
    iteration_count: int = 0
    owner_id: str = "Harness and Multi-agent Workflow Owner"


@dataclass(frozen=True)
class WorkOrderGraph:
    id: str
    schema_version: str
    task_graph_hash: str
    max_iterations: int
    handoff_contract: str
    stop_condition: str
    escalation_owner: str
    merge_policy: str = "HUMAN_REVIEWED"
    edges: tuple[tuple[str, str], ...] = ()  # (from_task, to_task)
    owner_id: str = "Harness and Multi-agent Workflow Owner"


@dataclass(frozen=True)
class HandoffPacket:
    id: str
    schema_version: str
    loop_id: str
    task_graph_hash: str
    max_iterations: int
    stop_condition: str
    escalation_owner: str
    merge_policy: str = "HUMAN_REVIEWED"
    ack: str | None = None  # ACK / NACK:reason
    owner_id: str = "Harness and Multi-agent Workflow Owner"


def validate_graph(graph: WorkOrderGraph) -> WorkOrderGraph:
    """WorkOrderGraph must be acyclic (DAG) and owner-verified.

    Circular dependency -> ERR_CIRCULAR_DEPENDENCY.
    """
    _require_owner(graph.owner_id, "WorkOrderGraph")
    _require_schema_version(graph.schema_version, "WorkOrderGraph")
    if graph.stop_condition != DETERMINISTIC_STOP:
        raise HandoffSchemaError(
            f"stop_condition must be deterministic, got {graph.stop_condition!r}"
        )
    if graph.merge_policy != HUMAN_REVIEWED_POLICY:
        raise HandoffSchemaError(
            "agent loop self-extends or merges without independent review: "
            f"merge_policy={graph.merge_policy!r}, expected 'HUMAN_REVIEWED'"
        )
    if _graph_has_cycle(graph.edges):
        raise CircularDependencyError(
            f"circular dependency detected in task graph {graph.id!r}: edges={graph.edges!r}"
        )
    return graph


def dispatch(loop: HarnessLoop) -> HarnessLoop:
    """QUEUED -> DISPATCHED. iteration_count < max_iterations required.

    Budget exhausted -> ERR_RETRY_EXHAUSTED.
    """
    _require_owner(loop.owner_id, "HarnessLoop")
    _require_schema_version(loop.schema_version, "HarnessLoop")
    if loop.stop_condition != DETERMINISTIC_STOP:
        raise HandoffSchemaError(
            f"stop_condition must be deterministic, got {loop.stop_condition!r}"
        )
    if loop.iteration_count >= loop.max_iterations:
        raise RetryExhaustedError(
            f"retry budget exhausted: iteration_count={loop.iteration_count} "
            f">= max_iterations={loop.max_iterations}"
        )
    return loop


def handoff(packet: HandoffPacket) -> HandoffPacket:
    """DISPATCHED -> WAITING_ACK. Each handoff must carry ACK/NACK.

    Missing ack -> ERR_ACK_MISSING; schema drift -> ERR_HANDOFF_SCHEMA.
    """
    _require_owner(packet.owner_id, "HandoffPacket")
    _require_schema_version(packet.schema_version, "HandoffPacket")
    if packet.stop_condition != DETERMINISTIC_STOP:
        raise HandoffSchemaError(
            f"stop_condition must be deterministic, got {packet.stop_condition!r}"
        )
    if packet.merge_policy != HUMAN_REVIEWED_POLICY:
        raise HandoffSchemaError(
            "schema drift / self-merge without independent review: "
            f"merge_policy={packet.merge_policy!r}, expected 'HUMAN_REVIEWED'"
        )
    ack = packet.ack
    if ack is None or not str(ack).strip():
        raise AckMissingError(
            "handoff missing ACK/NACK: every handoff must carry an explicit ACK or NACK"
        )
    if not str(ack).startswith(("ACK", "NACK")):
        raise HandoffSchemaError(
            f"handoff ack malformed (schema drift): {ack!r} must start with ACK or NACK"
        )
    return packet


def merge_review(loop: HarnessLoop, merge_policy: str) -> HarnessLoop:
    """Merge requires HUMAN_REVIEWED policy (CH15 core predicate).

    Self-merge without independent review -> ERR_HANDOFF_SCHEMA.
    """
    _require_owner(loop.owner_id, "HarnessLoop")
    _require_schema_version(loop.schema_version, "HarnessLoop")
    if loop.stop_condition != DETERMINISTIC_STOP:
        raise HandoffSchemaError(
            f"stop_condition must be deterministic, got {loop.stop_condition!r}"
        )
    if merge_policy != HUMAN_REVIEWED_POLICY:
        raise HandoffSchemaError(
            "merge without independent review: "
            f"merge_policy={merge_policy!r}, expected 'HUMAN_REVIEWED'"
        )
    return replace(loop, merge_policy=merge_policy)


def _require_owner(owner_id: str, kind: str) -> None:
    """Reject forged/foreign owner_id (CH15-ADV-001: STOP_QUARANTINE_TT)."""
    if owner_id != HARNESS_OWNER_ID:
        raise HandoffSchemaError(
            f"forged {kind} owner rejected: expected {HARNESS_OWNER_ID!r}, got {owner_id!r}"
        )


def _require_schema_version(schema_version: str, kind: str) -> None:
    """Reject schema drift away from the CH15 contract schema (v1.0.0)."""
    if schema_version != EXPECTED_SCHEMA_VERSION:
        raise HandoffSchemaError(
            f"schema drift: {kind} schema_version={schema_version!r}, "
            f"expected {EXPECTED_SCHEMA_VERSION!r}"
        )


def _graph_has_cycle(edges: tuple[tuple[str, str], ...]) -> bool:
    """Kahn topological sort: returns True when the edge set contains a cycle."""
    adjacency: dict[str, list[str]] = defaultdict(list)
    indegree: dict[str, int] = defaultdict(int)
    nodes: set[str] = set()
    for from_task, to_task in edges:
        adjacency[from_task].append(to_task)
        indegree[to_task] += 1
        nodes.add(from_task)
        nodes.add(to_task)
    queue = deque(node for node in nodes if indegree[node] == 0)
    visited = 0
    while queue:
        node = queue.popleft()
        visited += 1
        for nxt in adjacency[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return visited != len(nodes)
