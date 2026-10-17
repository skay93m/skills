# Knowledge Report Template

## Metadata
- Run ID: {{RUN_ID}}
- Timestamp: {{TIMESTAMP}}
- Project: {{PROJECT}}
- Operator / Agent: {{OPERATOR}}
- Operation: {{OPERATION}}
- Status: {{STATUS}}

## Executive Summary
{{SUMMARY}}

## Ingest Queue
- Processed Sources: {{PROCESSED_COUNT}}
- Remaining Queue: {{REMAINING_COUNT}}
- Mutation Budget Used: {{BUDGET_USED}} / {{BUDGET_CAP}}

## Structural & Semantic Lint Findings
| Category | Note Identifier | Severity | Finding Details | Recommended Action |
|---|---|---|---|---|
{{LINT_FINDINGS_ROWS}}

## Applied Mutations
| Action | Note Identifier | Path | Checksum Before | Checksum After |
|---|---|---|---|---|
{{MUTATIONS_ROWS}}

## Ledger Audit Record
- Ledger Entry Appended: {{LEDGER_APPENDED}}
- Transaction Hash: {{TRANSACTION_HASH}}
