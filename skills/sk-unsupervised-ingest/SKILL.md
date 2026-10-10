---
name: sk-unsupervised-ingest
description: Bounded non-blocking ingestion of selected Wiki raw material with theme
  analysis, Idea Compass enrichment, reversible reported mutations and deferred human
  questions.
---

# Unsupervised ingest

## Purpose

Process selected source-facing material already available in the Wiki without synchronous human interaction. The workflow asks what the Wiki can learn from the material in its current context, preserves uncertainty, makes bounded reversible improvements and records every finding, mutation and deferred question in a dated report.

This skill is the scheduled counterpart to supervised ingestion. It inherits the Wiki-specific provenance, search, authorship and verification rules from supervised ingestion while replacing synchronous human gates with proceed, defer or block decisions.

## Source boundary

The normal input is a Wiki raw note already present in the mutable ingestion inbox.

The immutable source authority is the approved Google Drive `raw/` folder or another explicitly identified upstream source. Agents must not silently alter that source. Wiki raw notes preserve the source-facing literature note, provenance and interpretation while material is awaiting ingestion, being revisited or retained as provenance.

Agents must not independently capture external sources for ingestion. The permitted exceptions are:

- capture a previous chat transcript verbatim into a Wiki raw note with clear provenance;
- mine Kensho and first create a provenance-preserving Wiki raw note before ingesting it.

A scheduled agent may scan the Google Drive raw folder for possible sources and list suggestions in the report. It must not capture, download or ingest those Drive files automatically. Further-reading searches may suggest sources, but suggestions are not ingestion inputs.

A raw note may be enriched or structurally repaired under this skill, but verbatim source text or transcript content must not be silently overwritten. Ingestion state is tracked by report-ledger checksums, not by an `ingest_status` field.

## Candidate selection

Select a bounded set of Wiki raw notes using available evidence such as:

- newly created or changed raw material;
- orphaned or weakly connected notes identified by curation;
- possible duplicates or sparse notes identified by maintenance;
- notes relevant to current Wiki projects or questions;
- notes referenced by semantic-lint findings;
- older material selected for a periodic revisit.

The scheduler must provide a fixed source and theme budget. If no bounded scope is supplied, stop without mutation.

Do not use ingest_status as a prerequisite or source-selection mechanism. The dated ingest reports provide the operational ledger, including source identity, revision checksum, selection reason and prior review context.

## Workflow

1. Read the current source note and establish its provenance.
2. Search the Wiki for existing sources, entities, decisions and related knowledge before creating or changing anything.
3. Identify the source's main themes and rank them by likely value to the current Wiki.
4. Apply the Idea Compass to the highest-value themes:
   - Where does this theme come from?
   - Where can it lead?
   - What supports it?
   - What contradicts it?
5. Keep source claims, existing Wiki positions, agent analysis and Syafiq's position distinct.
6. Write or refine source-facing prose, retrieval-worthy observations and evidence-supported relations where justified.
7. Create or update bounded non-destructive Wiki improvements.
8. Record every finding, question and mutation in the ingest report.
9. Reread and verify every changed note before completing the item.
10. Continue to the next item when one item is deferred or blocked.

The Idea Compass is a provisional Wiki working protocol. The four prompts must not be presented as an established canonical framework until the Wiki defines and validates it.

## Human input

The scheduled run never waits for a response. When judgement is needed, preserve the uncertainty and add a concise report entry with one question followed by:

Syafiq:

A human response is processed later by a separate review workflow. It may accept, reject or amend the reported change.

## Mutation policy

The agent may make bounded mutations when they are supported by the evidence and fully reported, including:

- adding or refining relations;
- enriching source-facing or canonical notes;
- creating hub notes;
- creating successor notes;
- recording supersession;
- replacing an obsolete body with a stub or redirect;
- correcting straightforward structural or provenance errors.

The agent must never delete or move notes during this workflow. Preserve permalinks and source history. Use supersession, stubs or redirects when consolidation or reclassification is needed.

Changes to schemas, immediate control notes or this scheduled workflow contract require separate explicit approval and are outside ordinary ingest autonomy.

## Report contract

Write a dated report at reports/YYYY-MM-DD-ingest.md.

Reports are ordinary Markdown records, not knowledge-bearing notes. They must use type report and bm_parse_semantics false, and must contain no observation or relation syntax.

Each item should be concise:

Finding: finding. Action: action or none. Question: question or None.

Syafiq:

For each mutation, also record the operation, exact target, before checksum, after checksum and enough information to reverse the change if Syafiq rejects it.

Record Drive candidates and further-reading suggestions separately as suggestions. Do not represent them as completed ingestion.

## Stop conditions

Stop the individual item and report it as blocked when:

- the source identity cannot be established without guessing;
- the relevant source content is inaccessible;
- proceeding would attribute an interpretation to Syafiq;
- a required mutation would delete or move a note;
- the operation would change a schema, immediate control note or this skill;
- a tool or verification call fails under the current Wiki failure rules.

An item-level stop must not block other independent items in the same run.

## Definition of done

An item is complete when:

- the source-facing material is represented faithfully;
- provenance is preserved;
- search-before-create has been performed;
- themes have been identified and bounded;
- the Idea Compass has been applied where useful;
- observations and relations do not overstate the evidence;
- allowed mutations have been reread and verified;
- unresolved judgement is recorded in the report;
- no source was silently captured from Google Drive or another external service;
- the report contains the finding, action, question and review space.

