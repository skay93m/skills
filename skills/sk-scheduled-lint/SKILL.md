---
name: sk-scheduled-lint
description: Bounded non-blocking structural and semantic lint with reported reversible
  mutations and deferred human questions.
---

# Scheduled lint

## Purpose

Run bounded structural and semantic checks after scheduled ingestion without synchronous human interaction. The workflow identifies defects, contradictions, stale or misleading knowledge, useful connections and enrichment opportunities, makes reported reversible improvements and records every finding and deferred question in a dated report.

This skill is the scheduled counterpart to semantic-lint. It inherits evidence-first comparison, authority assessment, provenance awareness and preservation of knowledge evolution while replacing interactive review gates with report-based follow-up.

## Scope

The scheduler must provide a fixed scope and lint budget. The scope may include:

- notes changed by the preceding ingest run;
- notes affected by an ingest mutation;
- notes named by existing lint findings;
- notes in a bounded folder or project area;
- a bounded periodic whole-Wiki slice.

If no bounded scope is supplied, stop without mutation. Do not repeat completed whole-Wiki lint merely to reconstruct prior work.

## Cadence

Daily lint checks the supplied bounded scope and any indexes directly affected by that scope. A weekly index-drift pass is an additional bounded lint scope, not a second ingest stage.

The scheduler must mark whether the weekly index-drift pass is due. When due, the lint agent discovers all immediate child folders of the Wiki root, sorts them by folder path, and records the discovered scope in the report. If the weekly scope is absent or not due, do not infer a whole-Wiki inventory pass; record that the periodic check was skipped.

## Checks

### Structural checks

Check the applicable note and folder contracts, including:

- frontmatter presence and classification;
- active schema compliance;
- folder depth and naming;
- index and log metadata;
- relation syntax and target shape;
- malformed semantic markers;
- obvious duplicate or stale operational metadata.

Reuse completed structural-lint evidence. Recheck only changed notes or issues directly affected by the current scope.

### Index drift and folder structure

When the supplied scope includes an index-drift pass, or when the weekly pass is due, discover every immediate child folder of the Wiki root and sort the folder paths deterministically. Read each folder index policy before applying the appropriate check. The policy fields are `index_scope` and `scheduled_repair`, as defined by `skills/index-governance.md`. Do not recurse into subfolders.

- If either policy is absent or ambiguous, inspect and report only.
- For `exhaustive` indexes, compare immediate content notes with the entries listed in the index.
- For `curated` indexes, check dead or malformed links, but do not treat an unlisted note as drift.
- For `pointer` indexes, verify only the declared pointers and their targets.
- Check for a required `index.md` and `log.md` in the bounded folder; report a missing log rather than creating one.
- Apply an index repair when the folder policy explicitly permits scheduled repair and the fix is deterministic. An allowed append must use an obvious existing section and the note's own title or description.
- In production mode, a clearly fitting concept or reference may be appended to an existing curated index section when the addition is bounded, reversible and logged. Do not reorder, delete or rewrite existing curated entries.
- A stale-link replacement remains report-only unless the policy and evidence authorise a unique deterministic repair.
- Count index mutations against the lint mutation budget and record the folder policy, discrepancy, evidence, checksums and reversal method in the lint report.

### Semantic checks

Look for:

- contradictory claims;
- stale claims presented as current;
- materially divergent duplicate concepts;
- conclusions stronger than their evidence;
- proposals, history or agent analysis presented as settled decisions;
- misleading relations;
- unclear provenance;
- unclear boundaries between historical, provisional and current knowledge;
- interesting connections not currently represented;
- useful opportunities to enrich sparse or incomplete notes.

Use current Wiki evidence first. Record external verification needs rather than beginning open-ended research.

## Workflow

1. Read the current note or notes in scope.
2. Retrieve only the evidence needed to test each finding.
3. Classify each result as deterministic, judgement-required or verification-needed.
4. Make bounded, evidence-supported improvements where permitted.
5. Record every finding, question and mutation in the lint report.
6. Reread and verify every changed note.
7. Continue to the next independent item when one item is deferred or blocked.
8. Stop after the supplied scope and budget are complete.

## Mutation policy

The agent may make bounded mutations when supported by evidence and fully reported, including:

- adding or refining relations;
- enriching notes;
- creating hub notes;
- creating successor notes;
- recording supersession;
- replacing obsolete content with a stub or redirect;
- correcting straightforward structural or provenance errors;
- applying deterministic fixes within an existing approved contract.

The agent must never delete notes. In production mode it may move a note only for deterministic filename or path normalisation, preserving its content, permalink and source history. Every such move must record the exact source and destination, before and after checksums, evidence and reversal method.

The agent must not change schemas, immediate control notes or this scheduled lint skill during ordinary lint. Those changes require separate explicit approval.

## Human input and review queue

The scheduled run never waits for a response. When judgement is needed, write one concise report question followed by:

Syafiq:

Also append the issue to `tasks/wiki-semantic-lint-review.md` with a stable ID, status `awaiting-response`, affected notes, evidence, recommendation, question and an empty `Response:` field. Review items are non-blocking unless proceeding would create a misleading or unsafe mutation. Blocking items are explicitly marked `blocking` in the report and remain queued until Syafiq decides.

A later review workflow may accept, reject or amend the reported change. Rejected changes must be reversible from the report's recorded evidence. Resolved decisions remain in the review queue as an audit trail and may be reused when a materially similar issue recurs.

## Report contract

Write a dated report at reports/YYYY-MM-DD-lint.md.

Reports are ordinary Markdown records, not knowledge-bearing notes. They must use type report and bm_parse_semantics false, and must contain no observation or relation syntax.

Each item should use this compact form:

Finding: finding. Action: action or none. Question: question or None.

Syafiq:

For every mutation, also record:

- operation type;
- exact target;
- reason and supporting evidence;
- before checksum;
- after checksum;
- reversal method.

Report interesting insights, connections and enrichment prompts even when no mutation is made. Keep them separate from completed fixes.

## Stop conditions

Stop the individual item and report it as blocked when:

- the evidence is insufficient to support the proposed change;
- a required mutation would delete or move a note;
- the operation would change a schema, immediate control note or this skill;
- external verification is necessary to avoid a misleading conclusion;
- a tool or verification call fails under the current Wiki failure rules.

An item-level stop must not block other independent items.

## Definition of done

A lint item is complete when:

- the stated scope has been checked;
- relevant existing evidence has been reused;
- findings are classified;
- permitted mutations have been reread and verified;
- all mutations are recorded with reversal evidence;
- unresolved questions appear in the report;
- interesting connections and enrichment opportunities are surfaced;
- no note has been deleted or moved;
- the report contains the finding, action, question and review space.

## Relations

- extends [[semantic-lint]]
- informed_by [[wiki-maintenance]]
- pairs_with [[unsupervised-ingest]]