---
name: knowledge-ingest
description: Use when processing eligible Wiki raw notes and bounded historical enrichment under approved ingestion rules.
metadata:
  origin: original
  agent_involvement: partial
  category: knowledge
---

# Knowledge ingest

## Input
Receive loaded revision, canonical Wiki project, read/write permissions, source ledger, persistent queues, hard budgets and run ID from the orchestrator. The candidate pool is Wiki `raw/`, a mutable pre-canonical inbox, not the original-source authority.

## Selection
Completeness comes from `list_directory` totals, never from search. Reconcile ledger first. Prioritise previously unprocessed and changed source checksums, then rotate historical enrichment even for unchanged sources. Persist cursors and deferrals. Incomplete pagination or ambiguous provenance blocks the affected source. Search existing canonical notes before proposing a new note.

## Processing
Separate source-derived claims, user observations and agent inference. Use settled Wiki schema and provenance conventions; record exact source and evidence. Apply only deterministic, reversible, authorised structural/provenance updates. Surface novel relations, synthesis, supersession and consequential semantic proposals for human review; do not apply them automatically.

## Source authority
Original external sources remain in approved Google Drive or their explicitly authorised upstream. An agent may scan Drive for candidate reporting but must not independently capture, download or ingest external material. Preserve existing explicitly authorised transcript and legacy-Kensho raw-note exceptions; do not generalise them.

## Mutation protocol
Plan one bounded change, reread current target/schema, use checksum guards where supported, execute, reread and verify. After uncertain writes, inspect persisted state before any retry. Record before/after checksum, provenance, reversal and ledger outcome. Fail closed when safe guards are unavailable for a consequential write.

## Output
Return completed and deferred source IDs, checksum ledger updates, historical-enrichment cursor, verified mutations, evidence-backed review candidates, failures and remaining budget. Never change task lifecycle or control-plane notes.
