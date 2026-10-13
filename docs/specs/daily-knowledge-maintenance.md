# Daily knowledge maintenance vertical slice

Status: draft implementation contract for review. Tracks issue #49.

## Objective
Replace the broken monolithic scheduled Wiki ingest/lint contract with three independently reviewable skills and a thin launcher. No Inbox Zero or task-assistant changes in this slice.

## Interface
The launcher supplies `approved_commit_sha`, `run_id`, `local_date`, `index_drift_due`, `wiki_project`, `budgets` and explicitly authorised tool capabilities. The orchestrator loads two deep modules. Each module returns verified mutations, checkpoints, deferrals, failures and review findings. No module may infer user approval from an agent's analysis.

## Persistent state to reconcile
Existing dated reports, raw source checksums, review queue, index policies and prior run state. Before a production run, designate one canonical rolling report, one review register and durable queue/ledger storage in the Wiki, with exact schema and write guards verified against available Basic Memory operations. Do not invent new Wiki paths merely because this draft names a conceptual store.

## Test matrix
- Missing/unapproved Git pin: no mutation.
- Incomplete Wiki search pagination: no false all-clear.
- Unchanged raw source: incremental skip but eventual historical rotation.
- New/changed raw source: provenance retained and checksum recorded.
- Novel semantic relation: review finding, no autonomous write.
- Task lifecycle proposal: human gate.
- Checksum conflict/uncertain response: reread and no duplicate write.
- Ingest item failure: independent lint continues.
- Friday index drift: policy-aware checks; unknown policy inspect-only.
- Missing Drive access: no external capture; report limitation.
- Historical reports unreconciled: read-only stop.
- Budget exhaustion: durable cursor and deferred queue.
- Repeat run: idempotent results and deduplicated findings.

## Deployment gates
1. Review this spec and skill contracts.
2. Confirm real tool support for pinned revision, guarded writes and durable state.
3. Add deterministic tests and run a read-only dry run.
4. Reconcile historical Wiki state and perform a controlled non-destructive test.
5. Obtain explicit owner approval before editing the disabled ChatGPT automation prompt or enabling it.

## Legacy migration
Do not delete `skills/sk-scheduled-ingest-lint` until the new contract passes gates. Avoid two simultaneously active entry points. Old Wiki-local bootstrap references are obsolete. No change to the separate supervised ingestion method or original-source capture authority.
