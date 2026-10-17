# Audit checks and note template (draft)

The audit note type and its field names are proposals in the SW run record specification. Use them as written until SW and the owner settle the type.

## Status
- `flagged`: at least one check is false, or `record_set_complete` is false. This includes `revision_pin_check` and `permalink_form_check`.
- `pending`: no check false, but at least one could not be completed.
- `passed`: every check true, the record set complete, nothing reported as not verifiable.
A check that could not be completed is never set to true. Record it under "Not verifiable". `manifest_verified` may be `pending` when the inventories cannot be matched or the window cannot be fixed.

## Checks to fields
| Field | True when |
|---|---|
| `record_set_complete` | The start marker and run note exist, ids are consistent, and no audit note existed before this one |
| `snapshot_verified` | False when the `-start` note is missing (the date cannot be fixed; list it under "Not verifiable"). Otherwise true when the snapshot named `auto-daily-auto-YYYYMMDD-000000` (date from `start_time_utc`) exists and was created before the `-start` time |
| `manifest_verified` | The manifest and the independent diff list the same changes (runbook V2); `pending` if not verifiable |
| `status_trust_check` | No stored status or trust field and no trust-asserting wording (V4) |
| `provenance_check` | Every written note has `authored_by`, `agent_model`, `run_id`, and compiled notes have provenance links (V4) |
| `non_absolute_wording_check` | No unhedged absolute wording in written notes (V4) |
| `deletion_allowlist_check` | Every deletion matches the allowlist with a complete manifest row (V3); true when there are no deletions |
| `out_of_scope_writes_check` | No write outside the scope for the first-run flag (V5) |
| `revision_pin_check` | Consistency of `supervised`, `loaded_revision` and `approved_revision` (V1b). Unattended (`supervised: false`, or not `true`): both present as full 40-hex SHAs in the start marker and run note, and equal; false on a missing or unequal `approved_revision`. Supervised: `approved_revision` may be `none`. `pending` if the notes or the `supervised` value cannot be read |
| `permalink_form_check` | Manifest and `audit_result` permalinks use the form the tool returns for the same note, not a hand-built prefix (V2) |

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
record_set_complete: <true|false>
snapshot_name: auto-daily-auto-<YYYYMMDD>-000000
snapshot_uuid: <uuid or "not found">
snapshot_verified: <true|false>
manifest_verified: <true|false|pending>
status_trust_check: <true|false>
provenance_check: <true|false>
non_absolute_wording_check: <true|false>
deletion_allowlist_check: <true|false>
out_of_scope_writes_check: <true|false>
revision_pin_check: <true|false|pending>
permalink_form_check: <true|false>
authored_by: <auditor model id>
agent_model: <auditor model id>
---

# <run-id>-audit

## Window and sources
Start time, snapshot time, duration (from `-start` `start_time_utc` and the run note timestamp, or "not available"), first-run flag, tools used, calls that timed out, flag adjustments.

## Findings
One line each: check, permalink, short quote or count, observed not concluded. Candidates missed by the activity listing are marked as candidates.

## Not verifiable
Each check or item that could not be completed, with the reason.

## Notes
Authorship was not used (the account owner appears as author for ChatGPT writes).
```

Field mapping: the SW run-record spec calls `loaded_revision` / `approved_revision` `approved_skill_sha`.

Do not write a `permalink` field: the tool assigns it from the title and folder, as the run records do. The SW spec lists `permalink` as required, so this is a conflict for the owner to settle. Keep the body free of absolute and trust wording. Do not add a trust or confirmation field.
