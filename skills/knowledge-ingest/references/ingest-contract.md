# Ingest contract

Two stages: capture the source as a source-note, then compile knowledge notes from it. Both are append-only.

## Source selection and capacity
- Order: new Drive `Raw` files, changed files, then legacy migration (oldest first from `raw/` in the read-only legacy `wiki` project).
- Slugs contain only `[a-z0-9-]`; a Drive title never forms a path directly.
- Daily baseline: 5 compiled notes [prototype]. Legacy migration at most 20% of that [prototype]. The run note records both counts.
- Change key: `drive_file_id` + `drive_size` + `drive_modified_time`, plus `source_checksum` (SHA-256) when the connector exposes it. Google-native documents often expose no hash.
- Skip a source whose key matches an existing source-note or a prior run's recorded inputs (manifests do not hold Drive keys).
- Ambiguous provenance (no file id, conflicting keys, unknown origin): stop for that source and defer it.

## Source-note
Path `source-notes/YYYY-MM-DD-<slug>`, type `source-note`. Frontmatter: `title`, `type`, `authored_by`, `agent_model`, `run_id`; provenance where known: `source_title`, `source_url`, `drive_file_id`, `drive_modified_time`, `drive_size`, `source_checksum`, `source_date`, `captured_at`, `ingest_profile`. Prose keeps nuance; observations expose retrievable properties.
Profiles: `standard` (default); `quick` for short captures under about 1,000 words [proposal]; `academic` only when explicitly requested in a supervised session.

## Compiled notes
- Path `knowledge/<slug>`, types `concept`, `claim`, `theory` (see `references/schemas.md`).
- Search before create: exact-permalink `read_note`. Search results only hint at near-duplicates, which become an allowlist deletion or a deferred item.
- Relations under `## Relations`: origin `derived_from`, support `supported_by`, contradiction as an incoming `challenges` edge from the opposing note, direction `leads_to`, supersession `supersedes`. The predicate set is open.
- Observation slots (`[claim]`, `[grounds]`, `[confidence]`, `[evidence]`, `[epistemic_qualifier]`, `[thesis]`, `[explanatory_mechanism]`) are advisory proposals, never blocking.
- Compiled wording is attributed and hedged, with provenance links on every note.

## Never compile as
A stored status or trust label, a confirmation marker, or a claim worded as settled fact without attribution.

## Local-only
Drive binaries, OCR output, prompts, tool traces and token metrics stay out of the Wiki.
