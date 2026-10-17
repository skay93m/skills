# Schema checksums

Reference values for the v1 schema notes in `sk-wiki/schemas/`, as published by the wiki engine owners. The algorithm is SHA-256 of the exact `content` string that `read_note` returns for the note (Cloud may rewrite frontmatter, so a local file is never hashed). The slot and edge definitions live in the lint and ingest skills' `references/schemas.md`; skills always use their own copy.

| Type | Note | SHA-256 |
|---|---|---|
| source-note | `schemas/source-note` | `64a4eb0ebecca0a990d045b39309b535272ac63492e4a2730781892d3a6def6e` |
| concept | `schemas/concept` | `1c047e184bdfbebac0ab4b2643c769ed8bde75bc617131b17a16aeed39376859` |
| claim | `schemas/claim` | `94a9201cff206f2f89da4f1f5fda098ec1e5a00d547201fe4e05180f1d4c0181` |
| theory | `schemas/theory` | `bb9b0333f7a6876ffba8917e7a6d113177d67db0c97d45064a88bca76224b2b6` |

## Not the tool checksum
The checksum the Basic Memory tool returns for a note is a different value and is NOT this reference value. Do not compare them. Compute SHA-256 only with a real hashing tool; if none exists, record `unavailable` and compare slot names and required frontmatter keys. Never estimate or invent a hash. The manifest's `before_checksum` and `after_checksum` are the checksums the MCP tool returns, so the auditor should compare those against tool output, not against SHA-256 of content.

## Use in the run note
Record `schema_checksums` as a map of type to the hash observed in the live note during this run, for the four types above, or `unavailable`. `unavailable` is not drift by itself; only a different hash, or a mismatch in slots or required keys when comparing without a hash, is drift. The auditor recomputes the hash from the CLI. The lint lane alone writes the themed finding on `operations/issues/schema-drift`; during the first-run limit it is report-only in the run note. Drift never blocks the run and neither copy is edited by an agent.

Status of the reference: the schemas have not yet been validated against a real note.
