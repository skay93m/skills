# Daily knowledge maintenance vertical slice

Status: draft implementation contract for review, with the 2026-10-13 audit and read-only dry run below. Tracks issue #49.

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
`skills/sk-scheduled-ingest-lint` and `skills/sk-scheduled-lint` were retired on 2026-10-13 (recoverable from Git history), so scheduled lint has one entry point: `daily-knowledge-maintenance`, which loads `knowledge-lint`. The interactive `sk-semantic-lint` is unchanged. `sk-unsupervised-ingest` is the older scheduled ingest counterpart of `knowledge-ingest`; its retirement is an open owner decision. Old Wiki-local bootstrap references are obsolete. No change to the separate supervised ingestion method or original-source capture authority.

## Audit and dry run (2026-10-13, read-only)

### Basic Memory capabilities (observed on the `wiki` project)
| Need | Support | Consequence |
|---|---|---|
| Revision checksum | `read_note` returns `checksum`; `include_content=false` is cheap | Guard source |
| Guarded overwrite / edit | `write_note(overwrite, expected_checksum)` and `edit_note(expected_checksum)` refuse a stale revision | Single-note compare-and-swap exists |
| Exclusive create | `write_note` without `overwrite` errors on an existing note | Safe first creation |
| Complete listing | `list_directory` returns `total`, `has_more` | Only proof of completeness |
| Search completeness | `search_notes` reports `total_is_exact: false` | Never use search for an all-clear |
| Version history | `list_note_versions` | Reversal source |
| Git pin, locks, multi-note transactions | Absent | Pin is launcher-verified; cross-note writes are not atomic |

### Persistence gaps (not resolved by this slice; owner designation needed)
1. No rolling operational report exists. Today's ledger is dated `reports/YYYY-MM-DD-ingest.md` and `-lint.md` notes with frontmatter `run_id`, `status`, `index_drift_due`. They record no per-source checksums, so no checksum ledger can be reconstructed from them.
2. The review register is `tasks/wiki-semantic-lint-review.md` (one note, `[status]` observations, IDs `SEM-`/`SCHED-`). A single large note is a contention point; the guard covers it but conflicts will block the item. Finding IDs from this slice are `KM-<hash>`; adopting them in the register is undecided.
3. The last ingest/lint report (2026-10-11) was a blocked bootstrap run; the Wiki-local `scheduled-ingest-lint` skill no longer exists. There is no report for 2026-10-12. Reconciliation of these is a precondition.
4. Index policy fields were found missing on at least one root folder (`SCHED-007`, awaiting response).

### Interface resolutions
- `request` fields: `approved_commit_sha`, `loaded_commit_sha`, `wiki_project`, `run_id`, `budgets.sources`. A pin that is absent, not a 40-character SHA, or different from the loaded revision blocks the run with no tool calls.
- Modes: `blocked` (no calls), `read_only` (evidence and reporting; mutations discarded and counted), `full`. Missing checksum, guarded-write, exclusive-create or listing-total support, an undesignated report, register or ledger, or unreconciled history all force `read_only`.
- Resume: the ledger note holds a `km-state` fenced JSON block (`run_id`, `ledger`, `cursor`, `deferred`, `lint_queue`, `done`), written through `checkpoint` after every item. `load_state` fails closed on anything unparseable. A crashed run with the same `run_id` skips `done` items; a new run skips unchanged checksums and advances only the rotation cursor.
- Verification: every write is checksum-guarded and reread; a conflict blocks that item only; an uncertain response is reread, never repeated. Items are ledgered only when all their applicable writes verified.
- Budgets: `sources`, `mutations` (default 8), `lint_notes` (12) and `lint_extra` (5). Over-budget work is deferred, never dropped.
- Proposals classify as `apply` only for `provenance_record`, `frontmatter_normalise`, `link_normalise` when reversible and non-semantic. Everything else, including unknown operations and task lifecycle, becomes a review finding.
- Executable reference and tests: `scripts/knowledge_maintenance.py`, `tests/test_knowledge_maintenance.py` (39 tests). It makes no Basic Memory calls; callers inject `process`, `lint`, a store with `read`/`write(expected_checksum)`, and a `checkpoint` callable. Drive access is a capability flag, and Friday folder discovery is a tool-level step whose result feeds `index_drift_plan`.

### Dry run result
The committed synthetic snapshot `tests/fixtures/dry_run_snapshot.json` runs the whole workflow read-only: `python3 scripts/knowledge_maintenance.py tests/fixtures/dry_run_snapshot.json` selects a changed, a new and a rotated source, lists the settled provenance write as would-apply, turns a novel relation and a task lifecycle proposal into review findings, caps lint scope, applies index policies (`repair_allowed`, `check_only`, `inspect_only`), reports missing Drive access, and writes nothing. `tests.test_knowledge_maintenance.DryRunFixture` asserts this output. Live observation:

Read-only inspection of the live Wiki, then the planner on a snapshot (109 `raw/` notes, no checksum ledger): with no pin the run is `blocked` and does nothing. With a placeholder pin it is `read_only`, selects 10 of 109 sources, defers 99, discards all mutations, and lists four reasons: no designated report, register or ledger, and unreconciled history. No Wiki write, scheduler change or Drive access occurred.

### Extended live evidence (read-only, 2026-10-13)
- `reports/` holds 21 notes (complete listing, `has_more` false). The latest ingest and lint reports are dated 2026-10-11 (blocked ingest); none exists for 2026-10-12. Confirms reconciliation is required.
- `find` with `meta` and `fields` returns each index note's `index_scope` and `scheduled_repair` cheaply with an exact total. Result: 18 root folders, 16 `type: index` notes (one is the root index), 15 folder indexes, 3 root folders with no index note found, and 1 folder index (`SCHED-007`) without policy fields. Per the contract these four are inspect-only. Policy values found: exhaustive/allowed 1, exhaustive/report-only 1, curated/report-only 8, pointer/report-only 4. So the only folder where a scheduled repair is permitted today is one exhaustive/allowed index.
- `read_note(include_content=false)` returns a note's checksum without its body, so the first-run ledger can be seeded for the 109 `raw/` notes at 109 cheap reads. Seeding is a Wiki write and needs owner approval of the ledger note first.
- Not performed: any write, a controlled non-destructive test, or a scheduler change (all forbidden for this slice).

### Remaining gates before any production run
1. Owner reviews this slice and merges to `develop` (not done here).
2. Owner designates the rolling report, review register and checksum ledger notes, and approves the schema (including `KM-` IDs).
3. Reconcile historical reports and the review register, including the missing 2026-10-12 run and the blocked 2026-10-11 run.
4. Launcher supplies a verified pinned release or commit; confirm how the ChatGPT automation obtains skill files at that revision.
5. Controlled non-destructive test on a copy or a single approved note, with checksum guard and reversal verified.
6. Owner approves editing and enabling the disabled automation; `sk-scheduled-ingest-lint` is already retired.

### Decisions taken on owner delegation (2026-10-13)
The owner asked for the architect's answer, derived from the approved architecture in #49 (Wiki owns state and review decisions, GitHub owns contracts, fail closed, one rolling report, no new authority). Paths are decided but the notes are **not yet created**; creating them is a Wiki write under gate 4.
1. **Report:** one rolling note, `reports/knowledge-maintenance`. Dated per-run ingest/lint reports stop once it exists; existing dated reports stay as history.
2. **Ledger:** a separate machine-state note, `reports/knowledge-maintenance-ledger`, holding only the `km-state` block. It is kept apart from the human-edited register so checkpoint writes do not contend with owner edits.
3. **Review register:** the existing `tasks/wiki-semantic-lint-review.md`. New findings use `KM-` IDs and `awaiting-response`; existing `SEM-`/`SCHED-` items are never renumbered or edited.
4. **Authority:** exactly `provenance_record`, `frontmatter_normalise`, `link_normalise`, reversible and non-semantic. The first production runs operate in report-only (`would_apply`) mode until the controlled test in gate 5 passes and the owner approves writes.
5. **Pinning:** the launcher passes the commit SHA of an owner-approved release tag as `approved_commit_sha`. The run fails closed on a missing, malformed or mismatched pin. Gemini has no role in the scheduled run.

### Owner mandate (2026-10-13): gates approved
- Merge to `develop`, creation of `reports/knowledge-maintenance` and the ledger note in the live Wiki: approved.
- First-run budgets are not throttled below the contract ceilings: 10 backlog sources plus 1 rotation slot, 8 mutations, 12 lint notes, 5 extra queued lint notes. Nothing above those ceilings is authorised.
- Strict no-deletion: no delete, move-to-delete or source overwrite is ever applied; each is a review finding. Rollback is by version history (`list_note_versions`) or Git, as the owner decides.
- `KM-` IDs sit beside `SEM-`/`SCHED-`; old IDs are neither migrated nor rewritten.
- Folders without an index note, or with absent policy (`SCHED-007`), are treated as curated/report-only: dead-link checks only, no repair, one `missing_index_policy` review finding each. No policy is inferred.
- The legacy `sk-scheduled-ingest-lint` automation is confirmed disabled by the owner. Retired on 2026-10-13 on owner instruction; the owner accepts Git as the backup. `sk-index-governance` lost its production repair override (and `sk-scheduled-lint` was removed for the same reason) (path moves and curated-index appends) with it, so those repairs are report-only.
- Ledger seed is empty on purpose: earlier reports recorded no checksums, so pre-filling current checksums would falsely mark the whole backlog as ingested.
- Not covered by the mandate: editing or enabling the ChatGPT automation prompt, which lives outside this repository and this session.

### Still unresolved
1. Creating the two Wiki notes and seeding the ledger (a live write).
2. Answering `SCHED-007` and reconciling the 2026-10-11 and 2026-10-12 gaps.
3. First-run budgets and the initial `lint_queue`.
4. How the run-time model is selected and verified; this slice only guarantees no escalation is requested.
5. Whether the automation can load skill files at the pinned tag and verify `loaded_commit_sha` itself.
