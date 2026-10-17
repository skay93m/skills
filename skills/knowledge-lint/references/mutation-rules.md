# Mutation rules for unattended runs

Applies to `sk-wiki` only. A value marked [proposal] or [prototype] is a working value, not a settled one.

## Write tiers
1. Exclusive-create: `write_note` with `overwrite=false` for every new note. A refusal means the note exists.
2. Guarded edit: read the note, presence check, then `edit_note` with the `expected_checksum` from that read, then read back.
3. `NOTE_REVISION_CONFLICT`, timeouts and unclear responses: re-read, re-decide, then act once. At most one guarded retry after a fresh read; never a blind repeat. A second failure stops that item and records it. An unrecoverable or tool failure halts the whole run (the orchestrator writes a terminal run note); the log entry is then not appended and "index/log pending" is recorded.

## Checksums in the manifest
`before_checksum` and `after_checksum` are the checksums the Basic Memory tool returns for the note (the revision checksum `read_note` reports). They are not the schema reference hashes, which are SHA-256 of note `content` and are a different value. Record exactly what the tool returned; never compute or estimate a substitute.

## Overwrite
- Compilation never overwrites. It appends sections, observations and relations.
- Structural lint may make narrow guarded edits: fix a broken link, remove an obsolete frontmatter field, normalise a heading, repair an existing relation. Each uses an exact anchor read in the same run and `expected_checksum` (or `find_replace` with one expected replacement).
- `write_note` with `overwrite=true` is allowed only for the stale-index rewrite of an existing index note (an index note listed under Index and log): guarded with `expected_checksum`, all still-valid entries preserved, recorded in the manifest as structural lint. It is refused for every other note.

## Index and log
- Notes: the index notes are the root `index.md`, `knowledge/index.md`, `source-notes/index.md` and `operations/issues/index.md`; the activity log is the root `log.md` beside the root index. Use each only if it exists. Never create an index or log note: if one is absent, record "index/log pending".
- Index: append-only for new entries, with presence check. The stale-index rewrite above is the only exception.
- Log: append-only, exactly one entry per run keyed by run ID, presence check, guarded edit. Lint and ingest only return their log lines; the orchestrator appends the single entry after both lanes finish.
- Orphan repair adds the typed relation, an index entry and (via the returned log line) a log entry.
- If an index or log edit fails after the content write, record "index/log pending" in the run note's deferred items. No retry; the next run or a person catches up.

## Deletion allowlist
Deletion is human-only unless one rule matches. Call `delete_note` only for an entry that passes the allowlist and has all fields below. Deletion targets only `knowledge/`, `source-notes/` and `scratch/` in `sk-wiki`; never `operations/` (including `issues/`), `schemas/`, index or log notes, and never any other project (including legacy `wiki`). No deletion happens under `first_run_limit`.
- `duplicate`: body at least 95% identical to a retained canonical note, same source, canonical note retained and linked, incoming relations preserved or pointed at it. The ratio (normalised body similarity, frontmatter excluded; measure [proposal]; threshold >= 0.95) must be computed by a real tool. If no tool can compute it, defer the deletion; never estimate a score.
- `scratch`: a note the same run created under `scratch/` (path starts with `scratch/`). A note from an earlier run, or outside `scratch/`, does not qualify.
- `fixture`: a note with no substantive body and zero-byte or unparseable frontmatter. A note with body content and bad frontmatter or a schema failure gets a structural repair or a finding, never a deletion.

Each deletion is a manifest entry holding `permalink`, `action: delete`, `allowlist_rule`, `before_checksum`, and `similarity_score` for `duplicate` only. Immediately before deleting, re-read the note and delete only if its checksum equals `before_checksum`. A small race remains between that read and the delete; the auditor catches it. Deletions are recoverable from the daily snapshot; restoring is by path, on the owner's instruction only.

## Human-only
Status or trust promotion (no such field exists); dismissing findings; any restore; deletion outside the allowlist; rewriting facts or claims in place; flipping or removing an `[issue]` observation; folder or architecture changes; schema edits; creating or editing the automation.

## Write scope
With `first_run_limit` true (or absent): write or delete nothing except creating `operations/<run-id>-start` and `operations/<run-id>`. Later runs may write only to these folders:
- `operations/`: only this run's `<run-id>-start` and `<run-id>` notes, never `-audit` or another run's records.
- `operations/issues/`: exclusive-create, then guarded appended lines.
- `knowledge/` and `source-notes/`: compiled notes and structural or additive-relation repairs.
- `scratch/`: temporary notes.
- The index notes and root `log.md` named above, only if they exist.
Any other path, including `schemas/`, is out of scope.

## Manifest entry
`{permalink, action: create|repair|supersede|delete, before_checksum, after_checksum, allowlist_rule (delete), similarity_score (duplicate delete)}`. `before_checksum` is null on create and `after_checksum` is null on delete. Never write `<workspace>` literally. Omit `permalink` from frontmatter and let the tool assign it from title and folder. For the manifest and `audit_result` use the prefix the tool returns for an existing sk-wiki note (for example `schemas/concept`); if none can be read, record the folder path.
