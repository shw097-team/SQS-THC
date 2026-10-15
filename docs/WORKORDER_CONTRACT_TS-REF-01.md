"""SQS-THC Product Constitution & DOC skeleton — WORK ORDER CONTRACT (TS-REF-01).

Source authority: SSOT/SQS-THC_P0-CIP-PACK_v2026.08.06-r2.md §17 TS-001
(Product constitution and DOC skeleton), owner F01-01. Target files exact
set from the TS-001 pack (canonical root layout per §16):

  docs/DOC-00.md            - product constitution (identity, namespace,
                              authority, non-goals; ERR_PRODUCT_ID_COLLISION)
  docs/DOC-01.md            - intent / requirement / financial change
  requirements/MC_REGISTRY.yaml - MC registry (unique IDs)
  architecture/DOC_CH_OWNER_MAP.yaml - chapter/owner map

Also expected (per §16 layout): contracts/product/PRODUCT_CONSTITUTION.yaml
materializing the TS-001 contract fields (product_id, formal_name, internal_name,
namespace, version, supersedes, aliases, non_goals) with the SPEC-01 state model.

Deliverables: ART-01. Tests: T-001/G00 positive + ERR_PRODUCT_ID_COLLISION
negative. Bounded worker writes ONLY the listed targets; canonical tree
C:\Projects\Agent_Workspace\SQS-THC (already materialized in Step 8).
"""
