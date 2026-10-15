# Negative fixture: sqs-risk authority ceiling
- sqs-risk MUST NOT issue Fabric AcceptanceReceipt
- sqs-risk MUST NOT write live broker state
- sqs-risk MUST NOT mutate FinancialSpec/Risk authority
- majority vote MUST NOT change risk authorization
