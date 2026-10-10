---
name: sk-scheduled-ingest-lint
---

# Scheduled Ingest and Lint

This is the shared execution contract for a future daily, unsupervised Wiki run. It runs ingestion first and scheduled lint second. It is deliberately separate from `triage.md`, supervised ingestion, and the general maintenance sequence.

## Bootstrap

The scheduled agent reads, in order:

1. `AGENTS.md`
2. the root `index.md`
3. a bounded tail of the root `log.md`
4. `skills/index.md`
5. this skill
6. `skills/index-governance.md`
7. `raw/index.md`, `schema/index.md`, and `reports/index.md` only when the relevant stage needs them

The scheduled agent does not load `triage.md`.

The scheduler supplies a run date in Europe/London and the fixed budgets below. If the runtime supplies a run identifier, preserve it. If it does not, derive the deterministic identifier `YYYY-MM-DD-daily-ingest-lint` from the Europe/London run date, adding `-friday-index-drift` when the weekly pass is due. Missing runtime metadata therefore does not block an otherwise bounded run.

## Stage order

The stages are strictly ordered:

1. select and ingest Wiki raw material
2. verify the ingest result
3. select and run bounded structural and semantic lint
4. verify the lint result
5. write the reports

Human questions never pause either stage.

## Ingest scope and budget

The candidate pool is the Wiki `raw/` folder. The report ledger is the scheduling state. For each raw note, the agent compares the current source checksum with the checksum recorded for the latest successful or terminal ingestion:

- no prior ledger entry: un-ingested
- current checksum differs from the latest recorded checksum: changed and eligible
- current checksum matches: unchanged and normally skipped

Candidate priority is deterministic:

1. un-ingested raw notes, ordered by creation date and then permalink
2. changed raw notes, ordered by most recent change and then permalink
3. raw notes explicitly surfaced by the current Wiki context or project
4. unchanged raw notes with weak or missing links
5. one bounded contextual revisit of an older unchanged note, only when no backlog remains

The run is backlog-first and resource-bounded:

- with no backlog, it may process up to one contextual revisit
- with one to ten backlog notes, it processes the whole backlog unless the resource ceiling is reached
- with more than ten backlog notes, it processes the oldest ten eligible notes
- while any backlog remains, contextual revisits are suspended
- the ingest stage stops at the fixed resource ceiling of 30 minutes or eight substantive note mutations, whichever comes first

The report records each source checksum, selection reason, and any remaining backlog boundary. It does not use an `ingest_status` field. A source is eligible again when its content changes or when it is selected for a bounded contextual revisit.

For each selected source, the agent:

- preserves provenance and distinguishes source text, interpretation, and agent analysis
- searches the Wiki before creating or changing notes
- identifies and ranks the source theme
- applies the Idea Compass: where the theme comes from, where it can lead, what supports it, and what contradicts it
- produces at most one primary learning objective for that source
- makes only bounded, evidence-supported changes

The ingest stage permits at most eight substantive note mutations in one run, excluding report, index, and log writes. It stops at the limit and reports remaining candidates as deferred.

## Source boundary

The candidate pool is the mutable Wiki `raw/` ingestion inbox and literature-note layer. It is not the immutable source authority and it is not the canonical durable knowledge layer.

The immutable source authority is the approved Google Drive `raw/` folder or another explicitly identified upstream source. Agents ingest only material already represented by a Wiki raw note.

Only Syafiq captures external sources for ingestion. The exceptions are:

- an agent may capture a previous chat transcript verbatim as a Wiki raw note
- an ingest agent may mine Kensho only by first creating a provenance-preserving Wiki raw note, then ingesting that note

The agent may scan the approved Google Drive `raw/` folder and report possible sources, but it must not capture, download, or ingest them. Further-reading suggestions from search plugins are reported separately and are not inputs to the run. Verbatim source text or transcript content in a Wiki raw note must not be silently overwritten.

## Periodic lint scope

Every daily run uses the default lint scope below. On Friday, the scheduler supplies `index_drift_due: true`; lint then adds the policy-aware index-drift pass defined in `skills/scheduled-lint.md`. The weekly pass discovers all immediate child folders of the Wiki root, sorts them by folder path, and runs after ingest within the lint time, note and mutation budgets.

If `index_drift_due` is false or absent, the run does not infer a whole-Wiki index inventory. It records the periodic pass as skipped and continues with the daily scope.

## Lint scope and budget

Lint runs only after ingest reaches a terminal result. Its default scope is:

- notes created or mutated by the ingest stage
- directly linked notes needed to verify those changes
- up to five additional notes selected from the oldest unresolved structural or semantic concerns in prior reports

The lint scope is capped at twelve unique notes. If the ingest stage fails at control-plane level, lint is skipped and a blocked lint report is written. A source-level ingest failure does not block lint for other completed sources.

Lint performs:

- deterministic structural checks
- evidence-first semantic checks
- contradiction, duplication, stale-claim, provenance, authority, and misleading-relation checks
- resurfacing of interesting connections and enrichment opportunities

The lint stage permits at most eight substantive note mutations. It must not repeat a previously reported check unless the target changed or the report records a new reason to revisit it.

## Mutation boundaries

Scheduled runs may add or refine relations, enrich notes, create hub or successor notes, record supersession, replace obsolete bodies with stubs or redirects, and make straightforward structural or provenance repairs.

Scheduled runs must never delete notes. In production mode they may move notes only for deterministic filename or path normalisation, preserving content, permalinks and source history. They may append a clearly fitting concept or reference to an existing curated index section when the addition is bounded, reversible and logged. They must not change schemas, this skill, immediate control notes, or workflow contracts except where this explicit production contract permits the structural repair. Other control-plane changes require separate explicit approval.

Every mutation is recorded in the relevant report with the operation, exact target, reason or evidence, before and after checksums, and reversal method.

## Reports and human review

The ingest stage writes `reports/YYYY-MM-DD-ingest.md`. The lint stage writes `reports/YYYY-MM-DD-lint.md`. Both use:

- `type: report`
- `bm_parse_semantics: false`
- ordinary Markdown only
- no observations or relations

Each finding or question is one concise line. A request for Syafiq's input is followed by a new paragraph beginning:

Syafiq:

The agent records its recommendation or proposed disposition before that prompt. It never waits for a response and continues with independent work.

For every judgement-required item, also append a stable issue to `tasks/wiki-semantic-lint-review.md` with status `awaiting-response`, affected notes, evidence, recommendation, question and an empty `Response:` field. Review items are non-blocking by default; mark an item blocking only when proceeding would create a misleading or unsafe mutation. On each Friday run, report the counts of awaiting, answered and applied issues and surface blocking items for the weekly decision meeting.

The reports also record:

- run identifier and date
- selected scope and budgets
- completed, deferred, blocked, and failed items
- Google Drive candidates and further-reading suggestions separately from Wiki mutations
- checksums and verification outcomes

## Completion

A run is complete only when both stage reports are written, all permitted mutations have been reread and verified, and the run records whether lint ran, was skipped, or was blocked. No scheduler is configured by this note.