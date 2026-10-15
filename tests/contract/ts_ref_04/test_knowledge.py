"""Frozen acceptance tests for the Knowledge/RAG/Memory kernel (CH10).

Fixtures match P0-CIP CH10 frozen fixtures:
CH10-POS-001 / CH10-NEG-001 / CH10-EDGE-001 / CH10-ADV-001.
"""
import unittest

from kernel.knowledge import (
    BroadLocatorError,
    ContextEnvelope,
    ContextPoisoningError,
    KnowledgeChunk,
    KnowledgeState,
    MemoryAuthorityLeakError,
    MemoryCandidate,
    RetrievalUngroundedError,
    chunk,
    index_chunk,
    retrieve,
)

PROV = "sha256:7dc84addb3611dcb"
FRESH = "2026-08-06T12:00:00+08:00"


def make_chunk(**kw) -> KnowledgeChunk:
    base = dict(
        id="ch10-chunk-001", schema_version="1.0.0",
        knowledge_item_id="ch10-knowledge-item-id-001",
        source_anchor="DOC-04#CH10", provenance_hash=PROV,
        freshness_at=FRESH, context_budget=0.1,
    )
    base.update(kw)
    return KnowledgeChunk(**base)


class CH10PositiveTests(unittest.TestCase):
    def test_pos_001_full_pipeline(self):
        """CH10-POS-001: INGESTED -> CHUNKED -> INDEXED -> RETRIEVED."""
        kc = make_chunk()
        c = chunk(kc)
        self.assertEqual(c.state, KnowledgeState.CHUNKED)
        env = ContextEnvelope(
            id="ch10-env-001", schema_version="1.0.0",
            source_anchor="DOC-04#CH10", provenance_hash=PROV,
            freshness_at=FRESH, context_budget=0.1,
        )
        i = index_chunk(c, env)
        self.assertEqual(i.state, KnowledgeState.INDEXED)
        r = retrieve(i)
        self.assertEqual(r.state, KnowledgeState.RETRIEVED)

    def test_pos_002_grounded_citation(self):
        """Retrieved chunk carries resolvable provenance anchor."""
        kc = make_chunk()
        r = retrieve(index_chunk(chunk(kc), ContextEnvelope(
            id="e", schema_version="1.0.0", source_anchor="DOC-04#CH10",
            provenance_hash=PROV, freshness_at=FRESH, context_budget=0.1)))
        self.assertTrue(r.source_anchor.startswith("DOC-04"))


class CH10NegativeTests(unittest.TestCase):
    def test_neg_001_broad_locator(self):
        """CH10-NEG-001: unresolved/broad source locator -> ERR_BROAD_LOCATOR."""
        kc = make_chunk(source_anchor="")
        with self.assertRaises(BroadLocatorError):
            chunk(kc)

    def test_neg_002_context_poisoning(self):
        """untrusted memory used as truth -> ERR_CONTEXT_POISONING."""
        kc = make_chunk()
        c = chunk(kc)
        poisoned = ContextEnvelope(
            id="ch10-env-poison", schema_version="1.0.0",
            source_anchor="DOC-04#CH10", provenance_hash=PROV,
            freshness_at=FRESH, context_budget=0.1,
            memory_class="untrusted_memory_as_truth",
        )
        with self.assertRaises(ContextPoisoningError):
            index_chunk(c, poisoned)

    def test_neg_003_memory_authority_leak(self):
        """untrusted memory without provenance promoted to authority -> ERR_MEMORY_AUTHORITY_LEAK."""
        with self.assertRaises(MemoryAuthorityLeakError):
            MemoryCandidate(
                id="ch10-mem-001", schema_version="1.0.0",
                knowledge_item_id="ch10-knowledge-item-id-001",
                provenance_hash="",  # no provenance
                freshness_at=FRESH, context_budget=0.1,
                memory_class="untrusted",
            )


class CH10EdgeTests(unittest.TestCase):
    def test_edge_001_stale_high_score_conflict(self):
        """high-score stale chunk vs lower-score current clause -> ABSTAIN_OR_DEGRADED_WITH_TT."""
        kc = make_chunk(freshness_at="2026-01-01T00:00:00+08:00",  # stale
                        retrieval_score=0.95)
        c = chunk(kc)
        env = ContextEnvelope(
            id="ch10-env-stale", schema_version="1.0.0",
            source_anchor="DOC-04#CH10", provenance_hash=PROV,
            freshness_at="2026-08-06T12:00:00+08:00", context_budget=0.1,
        )
        # stale chunk must not silently index as current truth
        with self.assertRaises(Exception):
            index_chunk(c, env)


class CH10AdversarialTests(unittest.TestCase):
    def test_adv_001_forged_owner_rejected(self):
        """CH10-ADV-001: forged owner_id must be rejected."""
        kc = make_chunk(owner_id="attacker")
        with self.assertRaises(Exception):
            chunk(kc)


if __name__ == "__main__":
    unittest.main()
