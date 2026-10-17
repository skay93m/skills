# Embedded schema reference (v1)

This is the skill's own copy. Skills always use this copy and work without access to the schema notes in `sk-wiki/schemas/`. The two may diverge. Checksums below are SHA-256 of the exact `content` string `read_note` returns for each schema note (not a local file). Untested: these schemas have not yet been validated against a real note, so treat the slot and edge rules as advisory.

| Type | Schema note | SHA-256 of live content (reference copy) |
|---|---|---|
| source-note | `schemas/source-note` | `64a4eb0ebecca0a990d045b39309b535272ac63492e4a2730781892d3a6def6e` |
| concept | `schemas/concept` | `1c047e184bdfbebac0ab4b2643c769ed8bde75bc617131b17a16aeed39376859` |
| claim | `schemas/claim` | `94a9201cff206f2f89da4f1f5fda098ec1e5a00d547201fe4e05180f1d4c0181` |
| theory | `schemas/theory` | `bb9b0333f7a6876ffba8917e7a6d113177d67db0c97d45064a88bca76224b2b6` |

## Checksum rules
The `checksum` or revision checksum that the Basic Memory tool returns (for example for `schemas/concept`) is a different value from the reference hash above and must never be compared with it. Compute SHA-256 only with a real hashing tool on the exact `content` string. If no such tool exists, record `unavailable` and compare slot names and required frontmatter keys instead. Never estimate or invent a hash. Manifest `before_checksum` and `after_checksum` are the checksums the MCP tool returns, not these hashes.

## Drift procedure
1. Read each `schemas/<type>` note read-only; hash its `content` per the rules above.
2. Report the observed values to the orchestrator, which records them in the run note as `schema_checksums: {type: sha256 or unavailable}`.
3. A mismatch or an unreadable note is a themed finding on `operations/issues/schema-drift`. Only the lint lane writes it (exclusive-create, later occurrences by guarded append); other lanes report the observation. It never blocks the run. No agent edits either copy; the copies are reconciled when the skills are updated.
4. Keep using this copy for the run whatever the live note says.

## Common rules (all types)
- Validation is advisory (`warn`); every slot is optional and never blocks.
- Required frontmatter: `title`, `type` (equals the type name), `authored_by`, `agent_model`, `run_id`; `permalink` optional.
- No status or trust field. Predicate set is open; a new predicate is a discovery, not an error.
- Relations are written under `## Relations` as `predicate [[Target]]`. Targets use the note title as written.

## source-note
Path `source-notes/`. Optional frontmatter: `source_title`, `source_url`, `drive_file_id`, `drive_modified_time`, `drive_size` (integer), `source_checksum`, `source_date`, `captured_at`, `ingest_profile` [proposal]. Slots: `central_claim`, `method`, `limitation` [proposal], `observation`. Edge: `relates_to` (source-note).

## concept
Path `knowledge/`. Slots: `definition`, `scope`, `limitation` [proposal]. Edges: `derived_from` (source-note or concept, origin), `supported_by` (claim, support), `leads_to` (concept, direction) [proposal], `supersedes` (concept). Contradiction is modelled as an incoming `challenges` edge from the opposing note; outward `challenges` and `contradicted_by` are [proposal].

## claim
Path `knowledge/`. Slots: `claim`, `grounds`, `confidence`, `evidence`, `epistemic_qualifier` [proposal]. Edges: `derived_from` (source-note), `supported_by` (claim), `challenges` (claim) [proposal], `supersedes` (claim). One independently attributable, challengeable proposition per note.

## theory
Path `knowledge/`. Slots: `thesis`, `explanatory_mechanism` [proposal]. Edges: `composed_of` (claim, expected two or more) [proposal], `explains` (concept) [proposal], `derived_from` (source-note), `supported_by` (theory), `challenges` (theory) [proposal], `supersedes` (theory).

## Not yet schematised
Run-record types (`operation-start`, `operation-run`, `operation-audit`) and the themed-issue type have no schema notes. Use the field lists in the orchestrator skill and treat the type names as proposals.
