schema: SQS-TEAM/1
stack_id: SQS_FINANCIAL
project_id: HGK-REFERENCE-PROJECT-002

persistent_profiles:
  - sqs-orchestrator
  - sqs-data-analysis
  - sqs-risk

role_catalog_ref: SQS_MARCA_ROLE_CATALOG.yaml
topology_policy_ref: SQS_TASK_TOPOLOGY_POLICY.yaml
runtime_pack_ref: SQS/TWICT_RUNTIME_PACK_MANIFEST.yaml

coordination:
  engine: hermes
  mechanism: project_scoped_kanban
  worker_lifecycle: on_demand
  deterministic_join_required: true

review_join_points:
  - MARCA_CHECK
  - RISK_CHECK
  - FROZEN_CANDIDATE
  - FABRIC_L2_ACCEPTANCE

forbidden:
  - LIVE_BROKER_WRITE
  - PROFILE_OWNS_FINANCIAL_TRUTH
  - MAJORITY_VOTE_RISK_AUTHORIZATION
  - MAKER_EQUALS_FINAL_CHECKER
  - TWICT_PARALLEL_ORCHESTRATOR
