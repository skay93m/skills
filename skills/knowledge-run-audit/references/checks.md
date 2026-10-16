# Audit checks and note template (draft)

The audit note type and its field names are proposals in the SW run record specification. Use them as written until SW and the owner settle the type.

## Status
- `passed`: every check true, and nothing reported as not verifiable.
- `flagged`: at least one check false.
- `pending`: no check false, but at least one could not be completed.
A check that could not be completed is never set to true. Record it under "Not verifiable".

## Checks to fields
| Field | True when |
|---|---|
| `snapshot_verified` | The snapshot named `auto-daily-auto-YYYYMMDD-000000` exists and was created before the `-start` time |
| `manifest_verified` | The manifest and the independent diff list the same changes (V2) |
| `status_trust_check` | No stored status or trust field and no trust-asserting wording (V4) |
| `provenance_check` | Every written note has `authored_by`, `agent_model`, `run_id`, and compiled notes have provenance links (V4) |
| `non_absolute_wording_check` | No unhedged absolute wording in written notes (V4) |
| `deletion_allowlist_check` | Every deletion matches the allowlist with a complete manifest row (V3); true when there are no deletions |
| `out_of_scope_writes_check` | No write outside the scope for the first-run flag (V5) |

## Template
```
---
title: <run-id>-audit
type: operation-audit
run_id: audit-<YYYY-MM-DD>-<seq>
target_run_id: <run-id>
auditor: <auditor tool and model>
verified_at_utc: "<ISO-8601 UTC>"
status: passed | flagged | pending
snapshot_name: auto-daily-auto-<YYYYMMDD>-000000
snapshot_uuid: <uuid or "not found">
snapshot_verified: <true|false>
manifest_verified: <true|false>
status_trust_check: <true|false>
provenance_check: <true|false>
non_absolute_wording_check: <true|false>
deletion_allowlist_check: <true|false>
out_of_scope_writes_check: <true|false>
authored_by: <auditor model id>
agent_model: <auditor model id>
---

# <run-id>-audit

## Window and sources
Start time, snapshot time, first-run flag, tools and calls that timed out.

## Findings
One line each: check, permalink, short quote or count, observed not concluded.

## Not verifiable
Each check or item that could not be completed, with the reason.

## Notes
Authorship was not used (the account owner appears as author for ChatGPT writes).
```

Keep the body free of absolute and trust wording. Do not add a trust or confirmation field.
