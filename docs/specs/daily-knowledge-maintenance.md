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
Do not delete `skills/sk-scheduled-ingest-lint` until the new contract passes gates. Avoid two simultaneously active entry points. Old Wiki-local bootstrap references are obsolete. No change to the separate supervised ingestion method or original-source capture authority.

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
- Executable reference and tests: `scripts/knowledge_maintenance.py`, `tests/test_knowledge_maintenance.py` (38 tests). It makes no Basic Memory calls; callers inject `process`, `lint`, a store with `read`/`write(expected_checksum)`, and a `checkpoint` callable. Drive access is a capability flag, and Friday folder discovery is a tool-level step whose result feeds `index_drift_plan`.

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
6. Owner approves editing and enabling the disabled automation; retire `sk-scheduled-ingest-lint` only afterwards.

### Unresolved design decisions (recorded, not decided)
1. Where the rolling report, review register and ledger live, and whether `KM-` IDs replace `SEM-`/`SCHED-`.
2. How the unattended agent obtains skill files at a pinned revision, and whether it can verify `loaded_commit_sha` itself.
3. Who owns the cursor and `lint_queue` seeding for the first run, and the first-run budgets.
4. Whether the settled operation list (`provenance_record`, `frontmatter_normalise`, `link_normalise`) matches the intended authority; any addition needs owner approval.
5. How a low-cost model is selected and verified at run time; this slice only guarantees that no escalation is requested.
