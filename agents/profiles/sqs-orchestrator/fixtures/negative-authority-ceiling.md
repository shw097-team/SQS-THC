# Negative fixture: sqs-orchestrator authority ceiling
- sqs-orchestrator MUST NOT issue Fabric AcceptanceReceipt
- sqs-orchestrator MUST NOT write live broker state
- sqs-orchestrator MUST NOT mutate FinancialSpec/Risk authority
- majority vote MUST NOT change risk authorization
