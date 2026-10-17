# Agent Handoff Template

## Handoff Metadata
- Handoff ID: {{HANDOFF_ID}}
- Timestamp: {{TIMESTAMP}}
- Source Runtime / Agent: {{SOURCE_AGENT}}
- Target Runtime / Agent: {{TARGET_AGENT}}
- Context Boundary / Task: {{TASK_DESCRIPTION}}

## Completed Objectives
{{COMPLETED_OBJECTIVES_LIST}}

## Verification Logs & Evidence
- Standard Checks (`check-standard.py`): {{STANDARD_CHECKS_STATUS}}
- Test Suite (`pytest`): {{TEST_SUITE_STATUS}}
- Artifact Verification: {{ARTIFACT_STATUS}}

## Residual Risks & Open Blockers
{{RISKS_AND_BLOCKERS}}

## Resumption Prompt
```text
{{RESUMPTION_PROMPT}}
```
