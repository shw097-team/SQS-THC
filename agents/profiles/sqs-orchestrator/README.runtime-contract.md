# sqs-orchestrator — Runtime Contract

- Engine: Hermes (project-scoped Kanban backbone).
- Effective load REQUIRED for every fresh session (distribution.yaml + SOUL.md + config.yaml).
- Authority ceiling: coordination only.
- Denied: live broker write, FinancialSpec mutation, Fabric AcceptanceReceipt, promotion, secrets.
- Rollback: restore prior distribution bytes; re-read hash.
