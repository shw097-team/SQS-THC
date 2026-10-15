# Negative fixture: sqs-data-analysis authority ceiling
- sqs-data-analysis MUST NOT issue Fabric AcceptanceReceipt
- sqs-data-analysis MUST NOT write live broker state
- sqs-data-analysis MUST NOT mutate FinancialSpec/Risk authority
- majority vote MUST NOT change risk authorization
