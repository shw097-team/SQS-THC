# sqs-data-analysis — Runtime Contract

- Engine: Hermes (project-scoped Kanban backbone).
- Effective load REQUIRED for every fresh session (distribution.yaml + SOUL.md + config.yaml).
- Authority ceiling: candidate/advisory only.
- Denied: live broker write, FinancialSpec mutation, Fabric AcceptanceReceipt, promotion, secrets.
- Rollback: restore prior distribution bytes; re-read hash.
