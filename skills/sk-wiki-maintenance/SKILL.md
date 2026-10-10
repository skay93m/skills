---
name: sk-wiki-maintenance
description: Supervised, report-only Wiki maintenance that runs Basic Memory's memory-curate,
  memory-defrag, memory-schema and memory-reflect one at a time, with an orchestrator
  reviewing each report before Syafiq releases the next.
---

# Wiki maintenance

## Purpose

Keep the Wiki tidy and connected by running Basic Memory's four maintenance skills as a supervised sequence: `memory-curate`, then `memory-defrag`, then `memory-schema`, then `memory-reflect`. A maintenance agent finds and proposes. An orchestrator checks every claim against the Wiki. Syafiq decides what is applied.

This skill does not replace [[syafiq-kay/wiki/skill/semantic-lint]], which owns questions of meaning, truth and authority, or structural lint, which owns deterministic checks. Reuse their recorded evidence, never repeat completed work, and never propose a change that duplicates or contradicts a finding in their Tasks.

## Roles

- **Maintenance agent**: a fresh session that runs one operation in report-only mode, writes a report, updates the run Task and stops.
- **Orchestrator**: a separate session that reviews each report against current Wiki state, records the verdict, applies only what Syafiq approves, and prepares the next prompt.
- **Syafiq**: owns every judgement call and releases each next step.

## Run Task

Resumable state lives in one Task for the run, never in chat. It holds the purpose, the work already done that must not be repeated, the per-operation scope, the evidence rule, the verdicts and decisions, the current step and an exact next step. Prompts passed to agents stay short and point at the Task. Return any inter-agent prompt in a fenced code block.

A maintenance agent bootstraps from AGENTS.md, the root index and triage, states the revision checksums of AGENTS and triage, loads the named Basic Memory skill, and reads the Task. If the Task is missing or insufficient it reports a continuity failure instead of reconstructing state from memory. If the skill is unavailable it stops and reports.

## Protocol for every operation

1. Run the operation in report-only mode. Change no existing note.
2. Write the report as a new note named `tasks/wiki-run-<skill>-report.md`, with method, coverage, findings with note links, proposals ranked by risk, and what was deliberately not done. Mark every proposal unapproved.
3. Add one entry to the run Task with the report path and the line `[review] pending`, and read it back.
4. Stop. Do not start the next operation.
5. The next operation starts only after the orchestrator has recorded an approving review and Syafiq has asked for it.

## Evidence rule

- Name the exact tool call or query behind every finding, and list every read the report cites.
- Reconcile counts with stated baselines, or explain the difference.
- State coverage as exactly what was read. A sample is not a whole-Wiki pass, and a count of unread notes needs its own query.
- Check current Wiki state before proposing: existing relations, existing concepts, and existing findings in the lint Tasks.
- Quote what the notes say. Do not strengthen their wording or invent states, tags or categories.
- Verify the source of the skill being run rather than citing a path that matches nothing in the Wiki.

## Operation boundaries

Each operation keeps the Wiki's own rules above the upstream skill's defaults.

### memory-curate

- Do not create hub notes. Do not add observations or relations to `index.md` or `log.md`, which are graph-silent by contract, and do not propose relations that point at them.
- Unresolved forward links are not defects. A leaf note reached through an index is by design, not an orphan.
- Classification belongs in frontmatter. Do not invent tags Syafiq has not used.
- Confirm that a proposed duplicate really overlaps before proposing a merge or a `supersedes` relation.

### memory-defrag

- Logs are append-only, and superseded knowledge is kept as history.
- `raw/` is a pre-canonical lifecycle container, and folder location alone does not make a note immutable. Protect provenance-bearing source material, such as source captures, transcripts and imported documents, where the original source identity must survive. Editable raw working material, such as scratchpads, research reports, literature notes and working captures, may be proposed for defragmentation when it is bloated, duplicated or stale. Decide from the note's `type`, `ingest_status` and actual content, and say which kind each candidate is.
- Any proposed split lands exactly one folder below root with a lowercase kebab-case name. Hold a split on any note that has a pending semantic finding.
- Before proposing to retire or rename a note, check that skills and scheduled tasks do not read it.
- Measure files with a tool call rather than estimating. Do not invent lifecycle values. How a note is retired is Syafiq's decision.

### memory-schema

- Schema tools see only notes of `type: schema`. Run the existing schema's validation once as a confirming check, and spend the rest of the effort on note types that might earn a schema.
- Propose a schema only when a pattern recurs across many real notes. Slots that a skill marks as provisional are not ready to register.
- Do not mistake artefacts for fields: `links_to` is the implicit relation from plain wikilinks, and a `- [result] [[note]]` line parses as both an observation and a relation. Reports written to one template prove nothing about a pattern.
- Fix a wrong value on a note instead of widening an enum to accept it.
- Check how the upstream skill declares relation fields before proposing schema syntax.
- A schema is an enforced contract. Changing it needs Syafiq's approval in the session.

### memory-reflect

- `journal/` is Syafiq's own writing and is read-only. Material in `raw/` is pre-canonical, so do not treat its claims as settled; judge each note by its type and provenance, not its folder.
- A candidate gives the source notes, the insight and a proposed target. It must not rewrite meaning.
- A candidate must say something no single note or AGENTS.md already says. A causal claim needs support across notes, not one capture.

## Review

The orchestrator re-checks the report against the Wiki, appends a **Review verdict** section before the report's Observations (the agent's original text stays as audit trail), and records a one-line `[review]` in the run Task. A verdict is approved, approved as a partial pass with corrections, or rejected, and lists the surviving candidates for Syafiq's per-item approval. Nothing in a report is authorised for application as written. A mistake in an earlier review is corrected by a new dated entry, not by editing the old one.

## Applying approved changes

The orchestrator applies a change only after Syafiq's approval in the current session, reads the note immediately before editing, guards the edit with its checksum, and verifies by read-back. Changes to immediate notes follow AGENTS section 9. Append a log entry for a change that matters chronologically.

## Task status

Use the Task schema's statuses. The run Task is `doing` until every operation has an approved review and this procedure has been persisted, then `done`. Later work, such as scheduling, belongs in another Task or Project.

## Observations

- [description] Supervised, report-only Wiki maintenance across curate, defrag, schema and reflect, with orchestrator review between steps.
- [decision] The agent reports and proposes, Syafiq approves, and the orchestrator applies and verifies.
- [boundary] Maintenance reports never change knowledge notes and never repeat completed lint work.
- [boundary] This skill does not schedule or automate the run.

## Relations

- relates_to [[syafiq-kay/wiki/skill/semantic-lint]]
- relates_to [[syafiq-kay/wiki/skill/triage]]
- derived_from [[syafiq-kay/wiki/tasks/wiki-four-skill-maintenance-run]]