# Envelope reference

Draft seam 0.1.0. All values below are synthetic.

## Closed vocabularies

- `status`: `succeeded`, `partial`, `failed`, `refused`
- `disposition`: `reported`, `proposed`, `applied`, `skipped`
- `approval-state`: `not-required`, `pending`, `approved`, `denied`
- `error-category`: `invalid-request`, `not-permitted`, `conflict`, `backend-unavailable`, `internal`; the empty string when `status` is `succeeded`
- operation classes: `read`, `write-report`, `propose-change`, `apply-change`, `delete`
- modes for this capability: `report-only`, `propose-only`

## Which disposition to use

- Report-only run that reported findings: `reported`.
- Propose-only run that proposed changes: `proposed`.
- Run that did nothing because it was refused or skipped everything: `skipped`.
- `applied` is never used in 0.1.0.

## Mutation summary arithmetic

For each class: `applied <= granted <= requested`, and `granted + refused <= requested`.

## Reference formats

`run-reference` is `run-` plus 26 characters from `a-z2-7`. `grant-reference` is `grant-` plus 26 such characters, or `""`. Use the exact values from the task prompt.

## Example: report-only success

```json
{
  "seam-version": "0.1.0",
  "capability": "knowledge.ingest",
  "capability-version": "0.1.0",
  "run-reference": "run-abcdefghijklmnopqrstuvwxyz",
  "status": "succeeded",
  "disposition": "reported",
  "approval-state": "not-required",
  "error-category": "",
  "grant-reference": "grant-abcdefghijklmnopqrstuvwxyz",
  "counts": {"seen": 3, "reported": 3, "proposed": 0, "applied": 0, "skipped": 0, "failed": 0},
  "mutation-summary": {
    "read": {"requested": 3, "granted": 3, "applied": 3, "refused": 0},
    "write-report": {"requested": 1, "granted": 1, "applied": 1, "refused": 0},
    "propose-change": {"requested": 0, "granted": 0, "applied": 0, "refused": 0},
    "apply-change": {"requested": 0, "granted": 0, "applied": 0, "refused": 0},
    "delete": {"requested": 0, "granted": 0, "applied": 0, "refused": 0}
  },
  "extensions": {}
}
```

## Example: a request outside the grant set

The write-report class was requested but not granted.

```json
{
  "seam-version": "0.1.0",
  "capability": "knowledge.ingest",
  "capability-version": "0.1.0",
  "run-reference": "run-bcdefghijklmnopqrstuvwxyza",
  "status": "refused",
  "disposition": "skipped",
  "approval-state": "denied",
  "error-category": "not-permitted",
  "grant-reference": "grant-abcdefghijklmnopqrstuvwxyz",
  "counts": {"seen": 3, "reported": 0, "proposed": 0, "applied": 0, "skipped": 3, "failed": 0},
  "mutation-summary": {
    "read": {"requested": 3, "granted": 3, "applied": 3, "refused": 0},
    "write-report": {"requested": 1, "granted": 0, "applied": 0, "refused": 1},
    "propose-change": {"requested": 0, "granted": 0, "applied": 0, "refused": 0},
    "apply-change": {"requested": 0, "granted": 0, "applied": 0, "refused": 0},
    "delete": {"requested": 0, "granted": 0, "applied": 0, "refused": 0}
  },
  "extensions": {}
}
```
