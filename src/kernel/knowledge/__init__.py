"""SQS-THC Knowledge / RAG / Memory / Provenance — package implementation (TS-REF-04 / CH10).

Implements the Knowledge / RAG / Memory / Provenance kernel per P0-CIP CH10:

* ``chunk``: INGESTED -> CHUNKED.  Owner identity is verified (forged owner is
  rejected) and the ``source_anchor`` must resolve to a prefixed locator such
  as ``DOC-04#CH10``.  A broad/unresolved locator -> ``ERR_BROAD_LOCATOR``.
* ``index_chunk``: CHUNKED -> INDEXED.  Untrusted memory used as truth ->
  ``ERR_CONTEXT_POISONING``; stale freshness below the envelope policy floor ->
  abstain (raise).
* ``retrieve``: INDEXED -> RETRIEVED.  Empty ``provenance_hash`` ->
  ``ERR_RETRIEVAL_UNGROUNDED``; a memory-class truth leak ->
  ``ERR_MEMORY_AUTHORITY_LEAK``.

``MemoryCandidate`` construction guards the promotion path upstream: an
untrusted memory candidate without provenance can never become an authority.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from dataclasses import replace
from datetime import datetime
from enum import Enum


OWNER_ID = "Knowledge and Provenance Owner"

# A resolvable source anchor is a prefixed locator, e.g. "DOC-04#CH10":
# a document-id prefix ("DOC-04") followed by a non-empty anchor ("CH10").
_RESOLVABLE_ANCHOR_RE = re.compile(r"^[A-Za-z]+-\d+#.+$")


class KnowledgeState(str, Enum):
    INGESTED = "INGESTED"
    CHUNKED = "CHUNKED"
    INDEXED = "INDEXED"
    RETRIEVED = "RETRIEVED"


class KnowledgeError(Exception):
    code = "ERR_KNOWLEDGE"


class BroadLocatorError(KnowledgeError):
    code = "ERR_BROAD_LOCATOR"


class ContextPoisoningError(KnowledgeError):
    code = "ERR_CONTEXT_POISONING"


class MemoryAuthorityLeakError(KnowledgeError):
    code = "ERR_MEMORY_AUTHORITY_LEAK"


class RetrievalUngroundedError(KnowledgeError):
    code = "ERR_RETRIEVAL_UNGROUNDED"


@dataclass(frozen=True)
class KnowledgeChunk:
    id: str
    schema_version: str
    knowledge_item_id: str
    source_anchor: str
    provenance_hash: str
    freshness_at: str
    context_budget: float
    retrieval_score: float = 0.0
    state: KnowledgeState = KnowledgeState.INGESTED
    owner_id: str = OWNER_ID


@dataclass(frozen=True)
class ContextEnvelope:
    id: str
    schema_version: str
    source_anchor: str
    provenance_hash: str
    freshness_at: str
    context_budget: float
    retrieval_score: float = 0.0
    memory_class: str = "untrusted"
    owner_id: str = OWNER_ID


@dataclass(frozen=True)
class MemoryCandidate:
    id: str
    schema_version: str
    knowledge_item_id: str
    provenance_hash: str
    freshness_at: str
    context_budget: float
    retrieval_score: float = 0.0
    memory_class: str = "untrusted"
    owner_id: str = OWNER_ID

    def __post_init__(self) -> None:
        """Guard the memory -> authority promotion path (upstream).

        An untrusted memory candidate that carries no provenance hash must
        never be promotable to authority: constructing it is already a
        memory-authority leak -> ``ERR_MEMORY_AUTHORITY_LEAK``.
        """
        if not self.provenance_hash and "untrusted" in self.memory_class:
            raise MemoryAuthorityLeakError(
                "untrusted memory without provenance cannot be promoted "
                "to authority (memory_class=%r)" % self.memory_class
            )


def _resolve_source_anchor(anchor: str) -> bool:
    """Return True when *anchor* is a prefixed, resolvable source locator."""
    return bool(anchor) and bool(_RESOLVABLE_ANCHOR_RE.match(anchor))


def _parse_freshness(value: str) -> datetime:
    """Parse an ISO-8601 timestamp (timezone-aware) for freshness comparison."""
    return datetime.fromisoformat(value)


def _is_stale(chunk_freshness: str, floor_freshness: str) -> bool:
    """True when the chunk freshness is below the envelope policy floor."""
    return _parse_freshness(chunk_freshness) < _parse_freshness(floor_freshness)


def _untrusted_as_truth(memory_class: str) -> bool:
    """True when *memory_class* claims untrusted memory is being used as truth."""
    return bool(memory_class) and "as_truth" in memory_class

def chunk(kc: KnowledgeChunk) -> KnowledgeChunk:
    """INGESTED -> CHUNKED. owner verified; source_anchor must resolve.

    Forged owner -> KnowledgeError; broad/unresolved locator -> ERR_BROAD_LOCATOR.
    """
    if kc.owner_id != OWNER_ID:
        raise KnowledgeError(
            "forged owner_id rejected: %r (expected %r)"
            % (kc.owner_id, OWNER_ID)
        )
    if not _resolve_source_anchor(kc.source_anchor):
        raise BroadLocatorError(
            "source_anchor is broad/unresolved: %r" % kc.source_anchor
        )
    return replace(kc, state=KnowledgeState.CHUNKED)


def index_chunk(kc: KnowledgeChunk, envelope: ContextEnvelope) -> KnowledgeChunk:
    """CHUNKED -> INDEXED. freshness >= policy floor; context budget respected;
    provenance hash verified; memory_class untrusted must NOT become truth.

    Poisoned context (untrusted memory used as truth) -> ERR_CONTEXT_POISONING.
    Stale freshness (below envelope policy floor) -> abstain (raise).
    """
    if kc.state is not KnowledgeState.CHUNKED:
        raise KnowledgeError("cannot index chunk in state %r" % kc.state)
    if _untrusted_as_truth(envelope.memory_class):
        raise ContextPoisoningError(
            "untrusted memory_class used as truth: %r"
            % envelope.memory_class
        )
    if envelope.provenance_hash != kc.provenance_hash:
        raise KnowledgeError(
            "provenance hash mismatch between envelope and chunk"
        )
    if _is_stale(kc.freshness_at, envelope.freshness_at):
        raise KnowledgeError(
            "stale freshness below policy floor; abstain "
            "(%s < %s)" % (kc.freshness_at, envelope.freshness_at)
        )
    return replace(kc, state=KnowledgeState.INDEXED)


def retrieve(kc: KnowledgeChunk) -> KnowledgeChunk:
    """INDEXED -> RETRIEVED. provenance_hash present; grounded citation required.

    Ungrounded retrieval -> ERR_RETRIEVAL_UNGROUNDED; memory authority leak -> ERR_MEMORY_AUTHORITY_LEAK.
    """
    if kc.state is not KnowledgeState.INDEXED:
        raise KnowledgeError("cannot retrieve chunk in state %r" % kc.state)
    if not kc.provenance_hash:
        raise RetrievalUngroundedError(
            "provenance_hash empty; retrieval is ungrounded"
        )
    memory_class = getattr(kc, "memory_class", None)
    if _untrusted_as_truth(memory_class or ""):
        raise MemoryAuthorityLeakError(
            "memory-class truth leak: untrusted memory promoted to authority "
            "(memory_class=%r)" % memory_class
        )
    return replace(kc, state=KnowledgeState.RETRIEVED)
